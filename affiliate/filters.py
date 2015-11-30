from django.contrib.auth import get_user_model
from .models import *
import django_filters


User = get_user_model()


class CustomerFilter(django_filters.FilterSet):
	class Meta:
		model = Customer
		fields = ('user', 'website')

	def __init__(self, *args, **kwargs):
		super(CustomerFilter, self).__init__(*args, **kwargs)
		self.filters['user'].extra.update({'to_field_name': User.USERNAME_FIELD})


class CustomerStatFilter(django_filters.FilterSet):
	class Meta:
		model = CustomerStat
		fields = ('username',)