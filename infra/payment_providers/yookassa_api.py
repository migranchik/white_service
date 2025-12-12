# infra/payment_providers/yookassa_api.py
from yookassa import Configuration, Payment

from configs.settings import settings


class YooKassaClient:
    @staticmethod
    def setup():
        Configuration.account_id = settings.YOOKASSA_SHOP_ID
        Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    @staticmethod
    def create_payment(
        amount_rub: int,
        description: str,
        customer_email: str | None = None,
        metadata: dict | None = None,
    ):
        YooKassaClient.setup()

        amount_str = f"{amount_rub:.2f}"  # "190.00"

        data: dict = {
            "amount": {
                "value": amount_str,
                "currency": "RUB",
            },
            "capture": True,
            "description": "Premium подписка на WhiteVPN",
            "confirmation": {
                "type": "redirect",
                "return_url": settings.YOOKASSA_RETURN_URL,
            },
            "metadata": metadata or {},
        }

        # Чек — чтобы не было 'Receipt is missing or illegal'
        if customer_email:
            data["receipt"] = {
                "customer": {"email": customer_email},
                "items": [
                    {
                        "description": description[:128],
                        "quantity": "1.00",
                        "amount": {"value": amount_str, "currency": "RUB"},
                        "vat_code": 1,  # "Без НДС" (под это должен быть настроен магазин)
                    }
                ],
            }

        payment = Payment.create(data)
        return payment

    @staticmethod
    def get_payment(payment_id: str):
        YooKassaClient.setup()
        return Payment.find_one(payment_id)
