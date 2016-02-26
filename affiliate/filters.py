from django.contrib.auth import get_user_model
from affiliate.models import *
import django_filters


User = get_user_model()


class CommissionDetailFilter(django_filters.FilterSet):
  class Meta:
    model = CommissionDetail
    fields = ('user',)

  def __init__(self, *args, **kwargs):
    super(CommissionDetailFilter, self).__init__(*args, **kwargs)
    self.filters['user'].extra.update({'to_field_name': User.USERNAME_FIELD})
