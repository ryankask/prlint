from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from ...factories import WebhookPayloadFactory


class TestPost(APITestCase):

    url = reverse('api:github')

    def test_url(self):
        """
        GitHub endpoint has a URL
        """
        self.assertEqual(self.url, '/api/github/')

    def test_no_repo(self):
        """
        GitHub webhook returns FORBIDDEN when no matching Repository in DB
        """
        result = self.client.post(self.url, data=WebhookPayloadFactory())

        self.assertEqual(result.status_code, 403)
        self.assertEqual(list(result.data), ['detail'])
        self.assertIn('not registered', result.data['detail'])
