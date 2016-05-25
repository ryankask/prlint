from django.contrib.auth import get_user_model
from factory import (
    LazyAttribute,
    LazyFunction,
    PostGenerationMethodCall,
    SubFactory,
    post_generation,
)
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger
from faker.factory import Factory as FakerFactory


faker = FakerFactory.create('en_GB')


class FullCleanDjangoModelFactory(DjangoModelFactory):
    """
    Ensures that created instances pass Django's `full_clean` checks.

    NOTE: does not work with `get_or_create`.
    """
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Call `full_clean` on any created instance before saving
        """
        obj = model_class(*args, **kwargs)
        obj.full_clean()
        obj.save()
        return obj


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = LazyFunction(faker.safe_email)
    first_name = LazyFunction(faker.first_name)
    last_name = LazyFunction(faker.last_name)
    password = PostGenerationMethodCall('set_password', 'password')
    username = LazyFunction(lambda: faker.profile()['username'])

    @post_generation
    def z_full_clean(self, create, extracted, **kwargs):
        """
        Assert that created User is "clean" in Django's opinion.

        NOTE: function name is prefixed with 'z_' so that it runs after the
        'password' post generation function.

        Raises:
            ValidationError: If there are any invalid fields in the final User
                object.
        """
        self.full_clean()


class RepositoryFactory(FullCleanDjangoModelFactory):
    class Meta:
        model = 'github.Repository'

    creator = SubFactory(UserFactory)

    # Range is inclusive
    remote_id = FuzzyInteger(low=1000, high=999999)

    name = LazyFunction(lambda: '_'.join(faker.words(nb=2)))
    full_name = LazyAttribute(lambda o: '{}/{}'.format(faker.word(), o.name))
