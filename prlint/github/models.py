import uuid

from django.conf import settings
from django.db.models import (
    PROTECT,
    CharField,
    ForeignKey,
    IntegerField,
    Model,
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


class Commit(Model):
    """
    A snapshot of a commit. Helps when commits fail and a link has to be
    generated to help the reviewer find the failing commit.

    Commits can be duplicated between Pull Requests, but don't care about that
    optimisation for now - the simplification is worth it.
    """
    pull_request = ForeignKey(PullRequest, on_delete=PROTECT)

    sha = CharField(max_length=40)

    # This could be manually constructed, but since GitHub gives it to us in
    # the API, then it's simpler to keep the provided URL.
    # Calculating max length:
    #     Head = https://github.com/ = 19
    #     User = octocat/ = max 40
    #     Repo = Hello-World/ = max 100
    #     Res  = commit/ = 7
    #     Sha  = 6dcb09b5b57875f334f61aebed695e2e4193db5e = 40 char
    html_url = CharField(max_length=210)

    message = TextField()
