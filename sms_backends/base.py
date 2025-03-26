from abc import ABC, abstractmethod


class BaseSMSBackend(ABC):
    @abstractmethod
    def send(self, phone, message):
        pass
