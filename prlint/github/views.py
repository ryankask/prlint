from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from .serializers import (
    HeaderSerializer,
    HookPayloadSerializer,
    PingPayloadSerializer,
    RepositoryPayloadSerializer,
)


class GitHubView(APIView):

    def post(self, request):
        """
        Process ping webhook payloads from GitHub.

        Order of processing:

        * Validate that repository is registered. If not 401 Unauthorized.
        * Validate passed event. If not 403 Forbidden.
        * Pass request to `pull_request` or `ping` handlers.

        # TODO

        * Process pull_request payloads.
        """
        repo_serializer = RepositoryPayloadSerializer(data=request.data)
        try:
            repo_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(repo_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        header_serializer = HeaderSerializer(request)
        try:
            header_serializer.is_valid(raise_exception=True)
        except ValidationError:
            # Event passed is invalid. Morph serializer error into something
            # more understandable.
            message = {
                'detail': (
                    'The \'{}\' event is not accepted by this webhook. Please '
                    'reconfigure.'.format(header_serializer.data['HTTP_X_GITHUB_EVENT'])
                ),
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        ping_serializer = PingPayloadSerializer(data=request.data)
        try:
            ping_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(ping_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)
