from django.contrib.auth import get_user_model
from factory import LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from faker.factory import Factory as FakerFactory


faker = FakerFactory.create('en_GB')


# Provide app's own version of UserFactory to maintain independence. Could be
# extracted to be independent.
class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = LazyFunction(faker.first_name)
    last_name = LazyFunction(faker.last_name)
    email = LazyFunction(faker.safe_email)
    username = LazyFunction(lambda: faker.profile()['username'])
