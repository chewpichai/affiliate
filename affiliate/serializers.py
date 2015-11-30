from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import *


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
  links = serializers.SerializerMethodField()

  class Meta:
    model = User

  def get_links(self, obj):
    request = self.context['request']
    username = obj.get_username()
    return {
      'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username}, request=request),
      'customers': '{}?user={}'.format(reverse('customer-list', request=request), username)
    }


class CustomerSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, required=False, queryset=User.objects.all())
  links = serializers.SerializerMethodField()

  class Meta:
    model = Customer

  def get_links(self, obj):
    request = self.context['request']
    links = {
      'self': reverse('customer-detail', kwargs={'pk': obj.pk}, request=request),
      'user': None
    }
    if obj.user:
      links['assigned'] = reverse('user-detail', kwargs={User.USERNAME_FIELD: obj.user}, request=request)
    return links



class CustomerStatSerializer(serializers.ModelSerializer):
  links = serializers.SerializerMethodField()

  class Meta:
    model = CustomerStat

  def get_links(self, obj):
    request = self.context['request']
    return {
      'self': reverse('customerstat-detail', kwargs={'pk': obj.pk}, request=request),
    }
