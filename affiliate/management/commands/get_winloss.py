from django.core.management.base import BaseCommand
from affiliate.models import CustomerStat
import json
import subprocess


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('start_date')
    parser.add_argument('end_date')

  def handle(self, *args, **options):
    username = options['username']
    password = options['password']
    start_date = options['start_date']
    end_date = options['end_date']
    winloss_list = get_winloss_list(username, password, start_date, end_date)
    for winloss in winloss_list:
      update_winloss(winloss)


def get_winloss_list(username, password, start_date, end_date):
  path = 'C:/Users/Chewpichai/Documents/GitHub/betaccount-nodejs/commands/fifa55.coffee'
  args = ['coffee', path, 'winloss', username, password, start_date, end_date]
  out = subprocess.check_output(args, shell=True)
  return json.loads(out)['data']


def update_winloss(winloss):
  try:
    cs = CustomerStat.objects.get(date=winloss['date'], username=winloss['username'])
    cs.winloss = winloss['winloss']
    cs.stake = winloss['stake']
    cs.comm = winloss['comm']
    cs.total = winloss['total']
    cs.save()
  except CustomerStat.DoesNotExist:
    CustomerStat.objects.create(**winloss)
