from rest_framework import serializers


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
