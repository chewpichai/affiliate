from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets, filters
from .filters import *
from .models import *
from .serializers import *


User = get_user_model()


class DefaultsMixin(object):
  """Default settings for view authentication, permissions,
  filtering and pagination."""

  authentication_classes = (
    authentication.BasicAuthentication,
    authentication.TokenAuthentication,
  )
  permission_classes = (
    permissions.IsAuthenticated,
  )
  paginate_by = 25
  paginate_by_param = 'page_size'
  max_paginate_by = 100
  filter_backends = (
    filters.DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter,
  )


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
  lookup_field = User.USERNAME_FIELD
  lookup_url_kwarg = User.USERNAME_FIELD
  queryset = User.objects.order_by(User.USERNAME_FIELD)
  serializer_class = UserSerializer
  search_fields = (User.USERNAME_FIELD,)


class CustomerViewSet(DefaultsMixin, viewsets.ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
  filter_class = CustomerFilter
  search_fields = ('user', 'website')


class CustomerStatViewSet(DefaultsMixin, viewsets.ModelViewSet):
  queryset = CustomerStat.objects.all()
  serializer_class = CustomerStatSerializer
  filter_class = CustomerStatFilter
  search_fields = ('username',)
