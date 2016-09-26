from django.test import RequestFactory
from factory import Dict, Factory, LazyFunction, SelfAttribute
from factory.fuzzy import FuzzyInteger
from faker.factory import Factory as FakerFactory


faker = FakerFactory.create('en_GB')


def PayloadRequestFactory():
    """
    Build a Request, configure it to look like a webhook payload from GitHub.
    """
    request_factory = RequestFactory()
    request = request_factory.post('/')
    request.META['HTTP_X_GITHUB_EVENT'] = 'pull_request'
    return request


class PingPayloadFactory(Factory):
    """
    Args:
        zen (str, optional): Random string of GitHub zen. Defaults to random
            words.
        hook_id (int, optional): ID of hook. Defaults to random int.

        hook_events (list (str), optional): List of events that hook has been
            configured for. Used to populate 'hook' dict. Defaults to
            `['pull_request']`.
    """
    class Meta:
        model = dict

    class Params:
        hook_events = ['pull_request']

    zen = LazyFunction(lambda: ' '.join(faker.words(nb=5)))
    hook_id = FuzzyInteger(low=1000, high=999999)
    hook = Dict({
        'type': 'Repository',
        'id': SelfAttribute('..hook_id'),
        'name': 'web',
        'active': True,
        'events': SelfAttribute('..hook_events'),
        'config': {
            'content_type': 'json',
            'insecure_ssl': '0',
            'url': 'http://testserver/api/github/',
        },
        'updated_at': '2016-07-31T13:32:47Z',
        'created_at': '2016-07-31T13:32:47Z',

        # TODO Generate these from a Respository and / or Webhook instance
        'url': 'https://api.github.com/repos/jamescooke/prlint/hooks/9328799',
        'test_url': 'https://api.github.com/repos/jamescooke/prlint/hooks/9328799/test',
        'ping_url': 'https://api.github.com/repos/jamescooke/prlint/hooks/9328799/pings',
        # end

        'last_response': {
            'code': None,
            'status': 'unused',
            'message': None,
        },
    })
