from django import template
from captcha.fields import CaptchaField


register = template.Library()


@register.simple_tag
def get_captcha_field():
  field = CaptchaField()
  attrs = {'id':'id-captcha'}
  return unicode(field.widget.render('captcha', '', attrs=attrs))
