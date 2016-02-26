from django.conf.urls import include, url
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from affiliate import viewsets

router = DefaultRouter(trailing_slash=False)
router.register(r'users', viewsets.UserViewSet)
router.register(r'commission-details', viewsets.CommissionDetailViewSet)


urlpatterns = [
  url(r'^captcha/', include('captcha.urls')),
  url(r'^v1-api/token/', obtain_auth_token, name='api-token'),
  url(r'^v1-api/', include(router.urls)),
  url(r'^$', TemplateView.as_view(template_name='affiliate/index.html')),
]
