from django import template
from django.forms import ChoiceField
from captcha.fields import CaptchaField
from ..models import User


register = template.Library()


@register.simple_tag
def get_captcha_field():
  field = CaptchaField()
  attrs = {'id':'id-captcha'}
  return unicode(field.widget.render('captcha', '', attrs=attrs))


@register.simple_tag
def get_bank_field():
  choices = (('', '--------'),) + User.BANK_CHOICES
  attrs={'class':'form-control'}
  field = ChoiceField(choices=choices)
  return unicode(field.widget.render('bank', '', attrs=attrs))
