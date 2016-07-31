from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GitHubView(APIView):

    def post(self, request):
        """
        Process pull_request and ping webhook payloads from GitHub.
        """
        # TODO fix URL to be generated dynamically
        data = {
            'detail': 'Repository is not registered with prlint. Please visit https://prlint.com/ to register.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)
