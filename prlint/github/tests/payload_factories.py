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


default_url = reverse('api:github')


def PayloadRequestFactory(header__event='ping', hook_url=None, repository_id=None, hook_events=None):
    """
    Build a Request, configure it to look like a webhook payload from GitHub.
    Request built is always `post`, but the URL used can change - this is so
    that test URLs can be provided.

    Args:
        header__event (str, optional): Name of the event to be sent as the
            `X-GitHub-Event` header. Defaults to 'ping'.
        hook_url (str, optional): URL of the built request. Defaults to the
            GitHub webhook URL.
    """
    if hook_url is None:
        hook_url = default_url

    request_factory = APIRequestFactory()
    request = request_factory.post(
        hook_url,
        data=PingPayloadFactory(
            hook_url=hook_url,
            request=request_factory.get('/'),
            repository_id=repository_id,
        ),
        format='json',
    )
    request.META['HTTP_X_GITHUB_EVENT'] = header__event
    return request


class HookConfigPayloadFactory(Factory):
    """
    Generates config block of GitHub's configuration for Hook payloads. Will
    attempt to build a fully qualified URL if a request is passed.

    Probably should not be called standalone - see HookPayloadFactory for Args.
    """
    class Meta:
        model = dict

    class Params:
        hook_url = '/__HOOK_URL__/'
        request = None

    content_type = 'json'
    insecure_ssl = '0'
    url = LazyAttribute(lambda o: (
        'http://noserver{}'.format(o.hook_url)
        if o.request is None else
        o.request.build_absolute_uri(o.hook_url)
    ))


class HookPayloadFactory(Factory):
    """
    Args:
        hook_url (str, optional): URL of the webhook that would receive this
            built payload.
        request (django HttpRequest, optional): Optional request, can be
            provided if full URIs are required.

    Fields to add to this factory:

        * 'last_response': {
        * 'type': 'Repository',
        * 'code': None,
        * 'status': 'unused',
        * 'message': None,
    """
    class Meta:
        model = dict

    class Params:
        hook_url = '/__HOOK_URL__/'
        request = None

    id = 1
    name = 'web'
    active = True
    events = ['pull_request']
    config = SubFactory(
        HookConfigPayloadFactory,
        hook_url=SelfAttribute('..hook_url'),
        request=SelfAttribute('..request'),
    )
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

    Args:
        repository_id (int, optional): Remote ID of the repository on
            GitHub. When generated, uses `random.randint` and not
            `factory.fuzzy.FuzzyInteger`.
        name (str, optional): Name of the repository.

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

    class Params:
        repository_id = None

    name = LazyFunction(faker.word)

    @lazy_attribute
    def id(self):
        if self.repository_id is None:
            return random.randint(1000, 999999)
        else:
            return self.repository_id


class PingPayloadFactory(Factory):
    """
    Args:
        hook_events (list (str), optional): List of events that hook has been
            configured for. Used to populate 'hook' dict. Defaults to
            `['pull_request']`.
        hook_id (int, optional): ID of hook. Defaults to random int.
        hook_url (str, optional): URL of the webhook that would receive this
            built payload.
        repository_id (int, optional): GitHub's ID of the respository.
        request (django HttpRequest, optional): Optional request, can be
            provided if full URIs are required.
        zen (str, optional): Random string of GitHub zen. Defaults to random
            words.
    """
    class Meta:
        model = dict

    class Params:
        hook_events = ['pull_request']
        hook_url = '/__HOOK_URL__/'
        request = None
        repository_id = None

    zen = LazyFunction(lambda: ' '.join(faker.words(nb=5)))
    hook_id = FuzzyInteger(low=1000, high=999999)
    hook = SubFactory(
        HookPayloadFactory,
        events=SelfAttribute('..hook_events'),
        hook_url=SelfAttribute('..hook_url'),
        request=SelfAttribute('..request'),
    )
    repository = SubFactory(
        RepositoryPayloadFactory,
        repository_id=SelfAttribute('..repository_id'),
    )
