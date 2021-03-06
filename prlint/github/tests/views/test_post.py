from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...factories import RepositoryFactory
from ...models import Repository
from ...views import GitHubView
from ..payload_factories import PayloadRequestFactory, PingEventFactory


class TestPost(APITestCase):

    url = reverse('api:github')


class TestPostCommon(TestPost):

    def test_url(self):
        """
        GitHub endpoint has a URL
        """
        self.assertEqual(self.url, '/api/github/')

    def test_non_json(self):
        """
        GitHub endpoint rejects non-json requests
        """
        result = self.client.post(self.url, {}, content_type='application/xml')

        self.assertEqual(result.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class TestPostUnregistered(TestPost):

    def test_ping_no_repo(self):
        """
        GitHub Ping webhook returns 401 UNAUTH when no matching Repository
        """
        request = PingEventFactory()

        result = GitHubView.as_view()(request)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('repository', result.data)
        self.assertIn('id', result.data['repository'])


class TestPostRegistered(TestPost):

    def setUp(self):
        super().setUp()
        RepositoryFactory(remote_id=123456)

    def test_set_up(self):
        """
        setUp: Repository is registered
        """
        self.assertEqual(Repository.objects.filter(remote_id=123456).count(), 1)

    def test_bad_event(self):
        """
        GitHub webhook rejects commit event with 403 forbidden response
        """
        request = PayloadRequestFactory(
            data={
                'repository': {
                    'id': 123456,
                },
            },
            event='commit',
        )

        result = GitHubView.as_view()(request)

        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(list(result.data), ['detail'])
        self.assertIn('\'commit\' event', result.data['detail'])
        self.assertIn('Please reconfigure.', result.data['detail'])

    # PING

    def test_all_events(self):
        """
        GitHub webhook returns BAD REQUEST to ping payload with all events
        """
        request = PingEventFactory(
            hook__events=['*'],
            repository__id=123456,
        )

        result = GitHubView.as_view()(request)

        self.assertEqual(result.status_code, 400)
        self.assertEqual(list(result.data['hook']), ['events'])
        self.assertIn('Events received were "[\'*\']"', result.data['hook']['events'][0])
