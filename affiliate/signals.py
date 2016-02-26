from django.db.models.signals import pre_save
from affiliate.models import User
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def user_create(sender, instance, **kwargs):
  if instance.refid:
    return
  instance.refid = User.gen_refid()
