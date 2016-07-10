from factory import (
    LazyAttribute,
    LazyFunction,
    SubFactory,
)
from factory.fuzzy import FuzzyInteger
from factory_djoy import CleanModelFactory, UserFactory
from faker.factory import Factory as FakerFactory


faker = FakerFactory.create('en_GB')


class RepositoryFactory(CleanModelFactory):
    """
    Args:
        creator (:obj:`User`, optional): Local owner of this repository.
        full_name (str, optional): The full name of the respository which
            includes the user or organisation name in GitHub.
            NOTES:
                * Should contain a single '/' (not validated)
                * Should end with the 'name' of the repository (not checked)
        name (str, optional): Name of repository.
        remote_id (int, optional): GitHub's internal ID for repo.
    """
    class Meta:
        model = 'github.Repository'

    creator = SubFactory(UserFactory)

    # Range is inclusive
    remote_id = FuzzyInteger(low=1000, high=999999)

    name = LazyFunction(lambda: '_'.join(faker.words(nb=2)))
    full_name = LazyAttribute(lambda o: '{}/{}'.format(faker.word(), o.name))


class PullRequestFactory(CleanModelFactory):
    class Meta:
        model = 'github.PullRequest'

    repository = SubFactory(RepositoryFactory)

    title = LazyFunction(lambda: ' '.join(faker.words(nb=3)))


class CommitFactory(CleanModelFactory):
    """
    Args:
        html_url (str, optional): URL for viewing commit in browser. E.g.
            https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e
        message (str, optional): Commit message in the traditional git sense.
        pull_request (:obj:`PullRequest, optional): Pull request that contains
            this commit.
        sha (str, optional)
    """
    class Meta:
        model = 'github.Commit'

    pull_request = SubFactory(PullRequestFactory)

    message = LazyFunction(faker.text)
    sha = LazyFunction(faker.sha1)

    html_url = LazyAttribute(lambda o: 'https://github.com/{full_name}/commit/{sha}'.format(
        full_name=o.pull_request.repository.full_name,
        sha=o.sha,
    ))
