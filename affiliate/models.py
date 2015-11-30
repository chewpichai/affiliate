from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible


class User(AbstractUser):
  bank_account_no = models.CharField(max_length=15)
  line_id         = models.CharField(max_length=255)
  phone_no        = models.CharField(max_length=15)


@python_2_unicode_compatible
class Customer(models.Model):
  user        = models.ForeignKey(User, related_name='customers')
  name        = models.CharField(max_length=255)
  line_id     = models.CharField(max_length=255)
  phone_no    = models.CharField(max_length=15)
  username    = models.CharField(max_length=15, null=True, blank=True)
  source      = models.CharField(max_length=2000)
  website     = models.URLField()
  registered  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


@python_2_unicode_compatible
class CustomerStat(models.Model):
  username  = models.CharField(max_length=15)
  stake     = models.DecimalField(max_digits=11, decimal_places=2)
  winloss   = models.DecimalField(max_digits=11, decimal_places=2)
  comm      = models.DecimalField(max_digits=11, decimal_places=2)
  total     = models.DecimalField(max_digits=11, decimal_places=2)
  created   = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return '%s (%s)' % (self.user_id, self.created)
