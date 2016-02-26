from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from affiliate import helpers
import decimal


class User(AbstractUser):
  BANK_CHOICES = (
    ('bbl', 'Bangkok Bank'),
    ('kbank', 'Kasikorn Bank'),
    ('ktb', 'Krung Thai Bank'),
    ('scb', 'Siam Commercial Bank'),
  )

  bank            = models.CharField(choices=BANK_CHOICES, max_length=15)
  bank_account_no = models.CharField(max_length=15)
  line_id         = models.CharField(max_length=255)
  phone_no        = models.CharField(max_length=15)
  refid           = models.CharField(max_length=15, unique=True)

  @classmethod
  def gen_refid(cls):
    import random;
    import string;
    choices = string.digits + string.letters
    refid = ''.join([random.SystemRandom().choice(choices)
                    for i in range(15)])
    try:
      cls.objects.get(refid=refid)
      return cls.gen_refid()
    except cls.DoesNotExist:
      return refid

  def get_shareable_link(self):
    return 'http://www.fifa555.com/?ref=%s' % self.refid

  def get_date_range(self):
    usernames = self.customers.values_list('username', flat=True)
    stats = CustomerStat.objects.filter(username__in=usernames).order_by('date')
    start = stats[0].date.replace(day=1)
    stats = stats.order_by('-date')
    end = stats[0].date.replace(day=1)
    dates = [start]
    while start < end:
      start = helpers.add_months(start, 1)
      dates.append(start)
    return dates

  def get_winloss_detail(self, date):
    output = {}
    end = helpers.get_end_of_month(date)
    usernames = self.customers.values_list('username', flat=True)
    stats = CustomerStat.objects.filter(username__in=usernames,
              date__in=(date, end))
    output['num_customers'] = stats.values_list('username').distinct().count()
    winloss = stats.aggregate(models.Sum('total'))['total__sum']
    output['winloss'] = winloss
    return output


@python_2_unicode_compatible
class CommissionDetail(models.Model):
  user = models.ForeignKey(User, related_name='commission_details')
  date = models.DateField()
  num_customers = models.PositiveIntegerField()
  last_winloss = models.DecimalField(max_digits=12, decimal_places=2)
  winloss = models.DecimalField(max_digits=12, decimal_places=2)
  comm = models.DecimalField(max_digits=11, decimal_places=2)

  def __str__(self):
    return '%s %s %s' % (self.date, self.winloss, self.comm)


@python_2_unicode_compatible
class Customer(models.Model):
  user        = models.ForeignKey(User, related_name='customers')
  username    = models.CharField(max_length=15)
  name        = models.CharField(max_length=255, null=True)
  line_id     = models.CharField(max_length=255, null=True)
  phone_no    = models.CharField(max_length=15, null=True)
  source      = models.CharField(max_length=2000, null=True)
  website     = models.URLField(null=True)
  registered  = models.DateTimeField(null=True)

  def __str__(self):
    return self.username


@python_2_unicode_compatible
class CustomerStat(models.Model):
  date      = models.DateField()
  username  = models.CharField(max_length=15)
  stake     = models.DecimalField(max_digits=11, decimal_places=2)
  winloss   = models.DecimalField(max_digits=11, decimal_places=2)
  comm      = models.DecimalField(max_digits=11, decimal_places=2)
  total     = models.DecimalField(max_digits=11, decimal_places=2)
  created   = models.DateTimeField(auto_now_add=True)
  updated   = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ('date', 'username')

  def __str__(self):
    return '%s (%s)' % (self.username, self.date)


from affiliate.signals import *
