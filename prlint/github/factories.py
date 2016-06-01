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
    class Meta:
        model = 'github.Repository'

    creator = SubFactory(UserFactory)

    # Range is inclusive
    remote_id = FuzzyInteger(low=1000, high=999999)

    name = LazyFunction(lambda: '_'.join(faker.words(nb=2)))
    full_name = LazyAttribute(lambda o: '{}/{}'.format(faker.word(), o.name))
