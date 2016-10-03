from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestGet(APITestCase):

    url = reverse('api:github')

    def test(self):
        """
        GitHub endpoint rejects GET requests
        """
        result = self.client.get(self.url)

        self.assertEqual(result.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
