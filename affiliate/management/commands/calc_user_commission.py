from django.core.management.base import BaseCommand
from affiliate.models import *


class Command(BaseCommand):
  def handle(self, *args, **options):
    for user in User.objects.all():
      calc_user_commission(user)


def calc_user_commission(user):
  last_winloss = 0
  for date in user.get_date_range():
    detail = user.get_winloss_detail(date)
    detail['last_winloss'] = last_winloss
    detail['date'] = date
    try:
      ucd = CommissionDetail.objects.get(user=user, date=date)
      ucd.num_customers = detail['num_customers']
      ucd.last_winloss = detail['last_winloss']
      ucd.winloss = detail['winloss']
      ucd.save()
    except CommissionDetail.DoesNotExist:
      ucd = CommissionDetail.objects.create(user=user, **detail)
    last_winloss = ucd.calc_winloss()
