from typing import List, NoReturn

from celery import shared_task

from sandbox.settings import BEEM_API_KEY, BEEM_SECRET_KEY

from BeemAfrica import Authorize, SMS


@shared_task()
def send_sms(message: str, recipients: List[str]) -> NoReturn:
    """
    A utility function to send sms
    @params: message: str, recipients: List[str]
    @returns: NoReturn
    """

    api_key = BEEM_API_KEY
    secret_key = BEEM_SECRET_KEY

    Authorize(api_key, secret_key)

    try:
        SMS.send_sms(message, recipients, source_addr="ONECLICK SCHOOLS")
    except Exception as e:
        return None
