import random

from django.core.urlresolvers import reverse
from factory import (
    Factory,
    LazyAttribute,
    LazyFunction,
    SelfAttribute,
    SubFactory,
    lazy_attribute,
)
from factory.fuzzy import FuzzyInteger
from faker.factory import Factory as FakerFactory
from rest_framework.test import APIRequestFactory

faker = FakerFactory.create('en_GB')


def PingEventFactory(**kwargs):
    """
    Build a ping request which is used by GitHub to ping webhooks. Event header
    is 'ping' and payload is built with the PingPayloadFactory.

    After generating the payload, hook ID is "synced" between the ``hook_id``
    and ``hook.id`` parameters - ``hook.id`` is disposed of and replaced with
    ``hook_id`.
    """
    uri = APIRequestFactory().get('/').build_absolute_uri(reverse('api:github'))

    data = PingPayloadFactory(hook__config__url=uri, **kwargs)
    data['hook']['id'] = data['hook_id']

    return PayloadRequestFactory(event='ping', data=data)


def PayloadRequestFactory(data, event, url=None):
    """
    Accept a chunk of data and a required event name and stuff them into a
    Request object which will look like it originated from GitHub. The Request
    instance built is always the ``POST`` method, but the URL used can change -
    this is so that test URLs can be provided.

    Args:
        data (dict): Data to be POSTed in the Request.
        event (str): Name of the event to be sent as the `X-GitHub-Event`
            header.
        url (str, optional): URL of the built request. Defaults to the GitHub
            webhook URL.
    """
    if url is None:
        url = reverse('api:github')

    request_factory = APIRequestFactory()
    request = request_factory.post(url, data=data, format='json')
    request.META['HTTP_X_GITHUB_EVENT'] = event

    return request


class HookConfigPayloadFactory(Factory):
    """
    Generates config block of GitHub's configuration for Hook payloads.
    """
    class Meta:
        model = dict

    content_type = 'json'
    insecure_ssl = '0'
    url = 'http://noserver/__HOOK_URL__/'


class HookPayloadFactory(Factory):
    """
    Generate the hook part of the payload.

    Fields to add to this factory:

        * 'last_response': {
        * 'type': 'Repository',
        * 'code': None,
        * 'status': 'unused',
        * 'message': None,
    """
    class Meta:
        model = dict

    config = SubFactory(HookConfigPayloadFactory)

    id = 1
    name = 'web'
    active = True
    events = ['pull_request']
    updated_at = '2016-07-31T13:32:47Z'
    created_at = '2016-07-31T13:32:47Z'

    # TODO Generate these from a Respository and / or Webhook instance
    url = 'https://api.github.com/repos/jamescooke/prlint/hooks/9328799'
    test_url = 'https://api.github.com/repos/jamescooke/prlint/hooks/9328799/test'
    ping_url = 'https://api.github.com/repos/jamescooke/prlint/hooks/9328799/pings'
    # end


class RepositoryPayloadFactory(Factory):
    """
    Pings to webhooks contain repository info, even though the docs don't show
    them.

    Other fields for future reference:
        "full_name": "jamescooke/prlint",
        "owner": {
            "login": "jamescooke",
            "id": 781059,
            ...
        },
        "private": false,
        "html_url": "https://github.com/jamescooke/prlint",
        "description": "",
        "fork": false,
        "url": "https://api.github.com/repos/jamescooke/prlint",
    """
    class Meta:
        model = dict

    id = FuzzyInteger(low=1000, high=999999)
    name = LazyFunction(faker.word)


class PingPayloadFactory(Factory):
    """
    Generates Ping payload data for a Ping webhook request.

    Args:
        hook_id (int, optional): ID of hook. Defaults to random int.
        zen (str, optional): Random string of GitHub zen. Defaults to random
            words.
    """
    class Meta:
        model = dict

    hook = SubFactory(HookPayloadFactory)
    repository = SubFactory(RepositoryPayloadFactory)

    hook_id = FuzzyInteger(low=1000, high=999999)
    zen = LazyFunction(lambda: ' '.join(faker.words(nb=5)))
