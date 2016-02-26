from django.core.management.base import BaseCommand
from affiliate.models import CustomerStat
import datetime
import json
import subprocess


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('date')
    parser.add_argument('numdays', type=int)

  def handle(self, *args, **options):
    username = options['username']
    password = options['password']
    date = datetime.datetime.strptime(options['date'], '%Y-%m-%d')
    numdays = options['numdays']
    for d in [date + datetime.timedelta(days=x) for x in range(0, numdays)]:
      print d
      winloss_list = get_winloss_list(username, password, d.strftime('%Y-%m-%d'))
      for winloss in winloss_list:
        update_winloss(winloss)


def get_winloss_list(username, password, date):
  path = 'C:/Users/Chewpichai/Documents/GitHub/node-betaccount/commands/fifa55.coffee'
  args = ['coffee', path, 'winloss', username, password, date, date]
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
