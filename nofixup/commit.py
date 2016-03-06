import json

from .exceptions import BadData


class Commit(object):

    def __init__(self, data):
        """
        Build Commit instance from JSON received.

        Args:
            json (str): String of JSON as per GitHub v3 API.
        """
        self.data = json.loads(data)

    def validate(self):
        """
        Commit is valid if it does not start with the 'fixup! ' stop phrase.
        """
        try:
            message = self.data['commit']['message']
        except KeyError:
            raise BadData('commit.message not found in Commit.data')

        return not message.startswith('fixup! ')
