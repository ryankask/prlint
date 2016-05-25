import uuid

from django.conf import settings
from django.db.models import (
    CharField,
    ForeignKey,
    Model,
    PROTECT,
    UUIDField,
    IntegerField,
)


class Repository(Model):

    creator = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
    )
    uuid = UUIDField(
        default=uuid.uuid4,
        editable=False,  # Field is locked via pre_save signal
    )

    # Github identifiers
    # Github username max len is 39 chars
    remote_id = IntegerField()              # GitHub's ID
    name = CharField(max_length=100)        # Max appears to be 99
    full_name = CharField(max_length=140)   # Full name is 'username/repo name'

    # TODO make better string output
