import requests
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

from sms_backends.base import BaseSMSBackend


class RayganSMSBackend(BaseSMSBackend):
    """
    ::Usage
        >>> #settings.py
        >>> SMS_SERVICE = {
        >>>     "ENGINE": "sms_backends.raygan_sms.RayganSMSBackend",
        >>>}
    """

    URL = 'https://smspanel.Trez.ir/SendMessageWithCode.ashx'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send(self, phone, message):
        data = {
            'Message': message,
            'Mobile': phone,
            'UserName': self.username,
            'Password': self.password,
        }
        response = requests.post(self.URL, data)
        if not response.ok:
            return self.on_error()
        return True

    @staticmethod
    def on_error():
        raise APIException(_("SMS system has been in trouble"))
