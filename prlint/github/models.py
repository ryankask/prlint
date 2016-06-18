import uuid

from django.conf import settings
from django.db.models import (
    CharField,
    ForeignKey,
    IntegerField,
    Model,
    PROTECT,
    TextField,
    UUIDField,
)


class UUIDModel(Model):
    """
    Provides a UUID field is locked via pre_save signal. Ensure that the model
    is registered with `check_change_uuid` in signals.
    """
    class Meta:
        abstract = True

    uuid = UUIDField(
        default=uuid.uuid4,
        editable=False,
    )


class Repository(UUIDModel):
    creator = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
    )

    # Github identifiers
    # Github username max len is 39 chars
    remote_id = IntegerField()              # GitHub's ID
    name = CharField(max_length=100)        # Max appears to be 99
    full_name = CharField(max_length=140)   # Full name is 'username/repo name'

    # TODO make better string output


class PullRequest(UUIDModel):
    """
    A snapshot of a Pull Request.
    """
    repository = ForeignKey(Repository, on_delete=PROTECT)
    title = TextField()  # GitHub requires a title on PRs (post trimming)
    body = TextField(blank=True)
