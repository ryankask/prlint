from django.core.urlresolvers import reverse
from factory import Factory, LazyFunction, SelfAttribute, SubFactory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from faker.factory import Factory as FakerFactory
from rest_framework.test import APIRequestFactory

faker = FakerFactory.create('en_GB')


def PingEventFactory(**kwargs):
    """
    Build a ping Request which is used by GitHub to ping webhooks. Event header
    is 'ping' and payload is built with the PingPayloadFactory.

    After generating the payload, hook ID is "synced" between the ``hook_id``
    and ``hook.id`` parameters - ``hook.id`` is disposed of and replaced with
    ``hook_id`.
    """
    uri = APIRequestFactory().get('/').build_absolute_uri(reverse('api:github'))

    data = PingPayloadFactory(hook__config__url=uri, **kwargs)
    data['hook']['id'] = data['hook_id']

    return PayloadRequestFactory(event='ping', data=data)


def PullRequestEventFactory(**kwargs):
    """
    Build a pull request Request generated when a Pull Request is created or
    updated.
    """
    data = PullRequestEventPayloadFactory()
    return PayloadRequestFactory(event='pull_request', data=data)


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


class PullRequestPayloadFactory(Factory):
    """
    Payload representation of the state of a pull request.

    https://developer.github.com/v3/pulls/#get-a-single-pull-request

    Args:
        id (int, optional): GitHub's internal ID for this PR.
        number (int, optional): GitHub's friendly number for the PR.
        state (str, optional): Either 'open' or 'closed'.
        commits_url (str, optional): URL on the GitHub API to collect the
            commits in this PR.
        commits (int, optional): Number of commits in this PR.
    """
    class Meta:
        model = dict

    id = FuzzyInteger(low=1000, high=999999999)
    number = FuzzyInteger(low=1, high=1000)
    state = FuzzyChoice(('open', 'closed'))
    commits_url = 'http://TODO'
    commits = FuzzyInteger(low=1, high=20)


class PullRequestEventPayloadFactory(Factory):
    """
    Generates pull request change event payload data. This is factory includes
    the "Event" name because this payload is generated when something happens
    to a PR - it in turn contains a pull request payload which contains all the
    latest data of the pull request.

    In addition to the fields in the github documentation, there are 'sender'
    and 'repository' objects included in the pull request event payload.

    https://developer.github.com/v3/activity/events/types/#pullrequestevent

    Args:
        action (str, optional): Action that just occurred to the Pull Request
            to cause the webhook to drop payload. The interestings ones are
            'opened', 'edited' and 'reopened' which will cause PRLint to check
            the pr.
        number (int, optional): GitHub's friendly number for the PR. Also
            passed dow to the child ``pull_request`` data so that both numbers
            match.
        pull_request (dict, optional): Pull Request's current status.
        repository (dict, optional): Repository status.
    """
    class Meta:
        model = dict

    action = FuzzyChoice((
        'assigned',
        'unassigned',
        'labeled',
        'unlabeled',
        'opened',       # queue check
        'edited',       # queue check
        'closed',
        'reopened',     # queue check
    ))
    number = FuzzyInteger(low=1, high=1000)
    pull_request = SubFactory(
        PullRequestPayloadFactory,
        number=SelfAttribute('..number'),
    )
    repository = SubFactory(RepositoryPayloadFactory)
