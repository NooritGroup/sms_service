from .base import BaseSMSBackend


class DummyBackend(BaseSMSBackend):
    def send(self, phone, message):
        print(f'Send SMS: {phone=} and {message=}'.encode('ascii', 'ignore').decode())
