from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .viewsets import *


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'customer-stats', CustomerStatViewSet)


urlpatterns = [
  url(r'^v1-api/token/', obtain_auth_token, name='api-token'),
  url(r'^v1-api/', include(router.urls)),
]
