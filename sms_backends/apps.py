from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SMSServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sms_backends"
    verbose_name = _('Sms service')
