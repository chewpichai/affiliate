from django.db.models.signals import pre_save
from affiliate.models import User, CommissionDetail
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def user_create(sender, instance, **kwargs):
  if instance.refid:
    return
  instance.refid = User.gen_refid()


@receiver(pre_save, sender=CommissionDetail)
def commission_detail_create(sender, instance, **kwargs):
  instance.comm = instance.calc_comm()
