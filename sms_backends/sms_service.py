import requests
from typing import Dict, List, Optional, Union


class SMSService:
    """کلاسی برای مدیریت ارسال و دریافت وضعیت پیامک از طریق REST API"""

    def __init__(self, username: str, password: str, base_url: str = "https://sms.3300.ir/api"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.send_endpoint = f"{self.base_url}/wsSend.ashx"
        self.status_endpoint = f"{self.base_url}/wsStates.ashx"

    def _send_request(self, endpoint: str, data: Dict) -> Dict:
        """ارسال درخواست به سرور و مدیریت پاسخ"""
        try:
            response = requests.post(endpoint, data=data)
            response.raise_for_status()  # اگه خطایی بود، استثنا پرت می‌کنه
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


if __name__ == "__main__":
    # تنظیمات اولیه
    sms = SMSService(username="USERNAME", password="PASSWORD")

    # سناریوی ۱: ارسال پیامک تکی
    result = sms.send(
        phone="989395213300",
        message="سلام، این یک تست است",
        line="9830003300"
    )
    print("ارسال تکی:", result)

    # سناریوی ۲: ارسال با خط خدماتی نگین رایانه
    result = sms.send(
        phone="989395213300",
        message="تست خط خدماتی",
        sms_type=2
    )
    print("ارسال خدماتی:", result)

    # سناریوی ۳: ارسال با خط دوم
    result = sms.send(
        phone="989395213300",
        message="تست خط دوم",
        line="9830003300",
        line2="10003300"
    )
    print("ارسال با خط دوم:", result)

    # سناریوی ۴: ارسال با چلچله
    result = sms.send(
        phone="989395213300",
        message="تست چلچله",
        line="9830003300",
        sms_type=1
    )
    print("ارسال با چلچله:", result)

    # سناریوی ۵: ارسال با خط خدماتی نگین رایانه
    result = sms.send(
        phone="989395213300",
        message="تست نگین رایانه",
        line="9830003300",
        sms_type=2,
        template=0
    )
    print("ارسال با نگین رایانه:", result)

    # دریافت وضعیت پیامک
    status = sms.get_sms_status(["6062", "6063", "6064"])
    print("وضعیت پیامک‌ها:", status)