from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import PullRequest, Repository


@receiver(pre_save, sender=PullRequest)
@receiver(pre_save, sender=Repository)
def check_change_uuid(sender, instance, **kwargs):
    """
    Before model that entends UUIDModel is saved, ensure that its UUID has not
    changed.

    Raises:
        ValidationError: If uuid of the model has been found to change.
    """
    try:
        original = sender.objects.get(pk=instance.id)
    except sender.DoesNotExist:
        return

    if instance.uuid != original.uuid:
        message = '{instance} uuid found to have changed from {original} to {new}'.format(
            instance=instance,
            original=original.uuid,
            new=instance.uuid,
        )
        raise ValidationError(message)
