import requests
from requests.exceptions import ConnectionError, ConnectTimeout

from . import settings

OK_STATUS = {'status': 'ok'}


def health():
    url = f'{settings.get_url()}/api/health/'

    try:
        response = requests.get(url, timeout=settings.get_timeout())
    except (ConnectTimeout, ConnectionError):
        return False

    return response.json() == OK_STATUS
