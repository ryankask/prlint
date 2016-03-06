import json


class Commit(object):

    def __init__(self, data):
        """
        Build Commit instance from JSON received.

        Args:
            json (str): String of JSON as per GitHub v3 API.
        """
        self.data = json.loads(data)
