import requests
from requests import Response
from requests.exceptions import ConnectionError, Timeout

from . import settings
from .models import PublishingError

CONNECTION_ERROR = 'Can not establish connection with postoffice'


def publish(topic: str, payload: dict, **attrs: dict) -> None:
    url = f'{settings.get_url()}/api/messages/'
    message = {
        'topic': topic,
        'payload': payload,
        'attributes': _stringify_attributes(attrs)
    }

    try:
        response = requests.post(url,
                                 json=message,
                                 timeout=settings.get_timeout()
                                 )
    except (ConnectionError, Timeout):
        _save_connection_not_established(message)
        return

    if response.status_code != 201:
        _save_publishing_error(response, message)


def _stringify_attributes(attributes: dict) -> dict:
    return {key: str(attributes[key]) for key in attributes.keys()}


def _save_connection_not_established(message: dict) -> None:
    _create_publishing_error(message, CONNECTION_ERROR)


def _save_publishing_error(response: Response, message: dict) -> None:
    error = 'Unknown error'

    if response.status_code == 500:
        error = 'Internal server error'

    if response.status_code == 400:
        error = response.json().get('data').get('errors')

    _create_publishing_error(message, error)


def _create_publishing_error(message: dict, error: str) -> None:
    PublishingError.objects.create(
        topic=message.get('topic'),
        payload=message.get('payload'),
        attributes=message.get('attributes'),
        error=error,
    )
