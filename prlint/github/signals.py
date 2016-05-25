from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Repository


@receiver(pre_save, sender=Repository)
def check_change_uuid(sender, instance, **kwargs):
    """
    Before Repository is saved, ensure that its UUID has not changed.

    Raises:
        ValidationError: If uuid of the Repository has been found to change.
    """
    try:
        original = Repository.objects.get(pk=instance.id)
    except Repository.DoesNotExist:
        return

    if instance.uuid != original.uuid:
        message = '{repo} uuid found to have changed from {original} to {new}'.format(
            repo=instance,
            original=original.uuid,
            new=instance.uuid,
        )
        raise ValidationError(message)
