from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import *


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
  links = serializers.SerializerMethodField()
  shareable_link = serializers.URLField(source='get_shareable_link', read_only=True)

  class Meta:
    model = User
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    data = validated_data.copy()
    data.pop('password')
    user = User(**data)
    user.set_password(validated_data['password'])
    user.save()
    return user

  def get_links(self, obj):
    request = self.context['request']
    username = obj.get_username()
    return {
      'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username}, request=request),
      'commission_details': '{}?user={}'.format(reverse('commissiondetail-list', request=request), username)
    }


class CommissionDetailSerializer(serializers.ModelSerializer):
  links = serializers.SerializerMethodField()

  class Meta:
    model = CommissionDetail

  def get_links(self, obj):
    request = self.context['request']
    return {
      'self': reverse('commissiondetail', kwargs={'pk': obj.pk}, request=request),
    }
