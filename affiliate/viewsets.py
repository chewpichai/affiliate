from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, authentication_classes, list_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from affiliate.filters import *
from affiliate.models import *
from affiliate.serializers import *
from captcha import fields


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
  authentication_classes = ()
  permission_classes = ()

  def create(self, request):
    data = request.data
    field = fields.CaptchaField()
    try:
      field.clean([data['captcha_0'], data['captcha']])
    except fields.ValidationError:
      raise ValidationError({'captcha': 'Wrong captcha.'})
    return super(UserViewSet, self).create(request)

  @list_route(methods=['get'], permission_classes=[permissions.IsAuthenticated],
    authentication_classes=[authentication.TokenAuthentication], url_path='me')
  def get_me(self, request):
    serializer = self.get_serializer(instance=request.user)
    return Response(serializer.data)


class CommissionDetailViewSet(DefaultsMixin, viewsets.ModelViewSet):
  queryset = CommissionDetail.objects.all()
  serializer_class = CommissionDetailSerializer
  filter_class = CommissionDetailFilter
  search_fields = ('username',)
