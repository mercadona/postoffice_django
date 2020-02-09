import requests
from requests import Response

from . import settings
from .models import PublishingError
from requests.exceptions import ConnectTimeout, ConnectionError


def publish(topic: str, payload: dict, **attrs: dict) -> None:
    url = f'{settings.get_url()}/api/messages/'
    message = {'topic': topic, 'payload': payload, 'attributes': attrs}

    try:
        response = requests.post(url,
                                 json=message,
                                 timeout=settings.get_timeout()
                                 )
    except (ConnectTimeout, ConnectionError):
        _save_connection_not_stablished(message)
        return

    if response.status_code != 201:
        _save_publishing_error(response, message)


def _save_connection_not_stablished(message: dict) -> None:
    _create_publishing_error(message,
                             'Can not stablish connection with postoffice')


def _save_publishing_error(response: Response, message: dict) -> None:
    error = 'Uknown error'

    if response.status_code == 500:
        error = 'Internal server error'

    if response.status_code == 422:
        error = response.json().get('errors').get('detail')

    _create_publishing_error(message, error)


def _create_publishing_error(message: dict, error: str) -> None:
    PublishingError.objects.create(
        topic=message.get('topic'),
        payload=message.get('payload'),
        attributes=message.get('attributes'),
        error=error,
    )
