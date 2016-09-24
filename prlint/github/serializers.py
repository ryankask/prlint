from rest_framework import serializers

from .models import Repository


class RepositorySerializer(serializers.Serializer):
    """
    Serializes the chunk of repository data from "repository" down.

    TODO check on the max constraint on ID. This was done "by hand" to get
    large numbers to work with SQLITE at test time.
    """
    id = serializers.IntegerField(min_value=1000, max_value=2**32)

    def validate_id(self, value):
        """
        Repository ID is valid if it exists in the database
        """
        try:
            Repository.objects.get(remote_id=value)
        except Repository.DoesNotExist:
            message = 'not here'
            raise serializers.ValidationError(message)
        return value


class RepositoryPayloadSerializer(serializers.Serializer):
    """
    Serializes the repository information contained in incoming requests and
    ensures that the source repository is registered on the system.
    """
    repository = RepositorySerializer()


class HeaderSerializer(serializers.Serializer):
    """
    Serializes incoming request headers (Django stores them in the request.META
    dictionary). Only allows 'pull_request' and 'ping' events. After
    validation, a sneaky 'event' attribute is set in the serializer instance to
    facilitate external use.

    NOTE that HeaderSerializer does not trim incoming data: ' pull_request '
    event will be invalid.
    """
    HTTP_X_GITHUB_EVENT = serializers.ChoiceField(choices=['pull_request', 'ping'])

    def __init__(self, request):
        """
        Initialise HeaderSerializer using the passed `request`'s `META`.

        Args:
            request (Django Request)
        """
        super().__init__(data=request.META)

    @property
    def event(self):
        """
        If serializer is valid, then return the valid event
        """
        return self.validated_data['HTTP_X_GITHUB_EVENT']


class HookPayloadSerializer(serializers.Serializer):
    """
    Serializes incoming JSON from Github that matches the Payload spec

    See https://developer.github.com/webhooks/#payloads
    """

    events = serializers.ListField(child=serializers.CharField(
        min_length=1,
    ))

    def validate_events(self, value):
        """
        Events field must be ['pull_request'] and nothing else
        """
        if len(value) < 1:
            raise serializers.ValidationError('No events passed')
        if value != ['pull_request']:
            message = (
                'This webhook only accepts "pull_request" events, plus the '
                'default "ping". Events received were "{}". Please '
                'reconfigure.'
            ).format(value)
            raise serializers.ValidationError(message)
        return value
