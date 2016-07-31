from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse


class TestPost(APITestCase):

    url = reverse('api:github')

    def test_url(self):
        """
        GitHub endpoint has a URL
        """
        self.assertEqual(self.url, '/api/github/')
