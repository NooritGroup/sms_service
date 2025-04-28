from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from sms_backends.base import BaseSMSBackend

__version__ = '0.0.4'
VERSION = (0, 0, 4, 'release', 0)


def get_sms_backend() -> BaseSMSBackend:
    sms_backend = settings.SMS_SERVICE
    if sms_backend is None:
        raise ImproperlyConfigured("SMS_SERVICE is not defined")
    assert isinstance(sms_backend, dict)
    backend = sms_backend.get('ENGINE', None)
    if backend is None:
        raise ImproperlyConfigured("SMS_SERVICE['ENGINE'] is not defined")
    try:
        backend_class = import_string(backend)
    except ImportError as e:
        raise ImproperlyConfigured("ERROR Importing SMS_SERVICE['ENGINE']") from e

    options = sms_backend.get('OPTIONS', {})

    # Special case for DummyBackend
    if backend.endswith('DummyBackend'):
        return backend_class()

    return backend_class(**options)
