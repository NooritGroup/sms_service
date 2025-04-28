import requests
from typing import Dict, List, Optional, Union

from sms_backends.base import BaseSMSBackend


class SMSService(BaseSMSBackend):

    def __init__(self, username: str, password: str, base_url: str = "https://sms.3300.ir/api"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.send_endpoint = f"{self.base_url}/wsSend.ashx"
        self.status_endpoint = f"{self.base_url}/wsStates.ashx"

    def _send_request(self, endpoint: str, data: Dict) -> Dict:
        try:
            response = requests.post(endpoint, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "msg": f"Request failed: {str(e)}"}

    def send(
            self,
            phone: str,
            message: str,
            line: Optional[str] = None,
            line2: Optional[str] = None,
            sms_type: int = 0,
            template: int = 0
    ) -> Dict:
        data = {
            "username": self.username,
            "password": self.password,
            "mobile": phone,
            "message": message,
            "type": sms_type,
            "template": template
        }

        if line:
            data["line"] = line
        else:
            data["line"] = "983000610330"
        if line2:
            data["line2"] = line2

        return self._send_request(self.send_endpoint, data)

    def get_sms_status(self, message_ids: Union[str, List[str]]) -> Dict:
        if isinstance(message_ids, list):
            message_ids = ",".join(map(str, message_ids))

        data = {
            "username": self.username,
            "password": self.password,
            "message_ids": message_ids
        }

        return self._send_request(self.status_endpoint, data)
