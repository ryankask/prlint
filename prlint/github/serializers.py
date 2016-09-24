from rest_framework import serializers


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
        Must be at least 1 event
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
