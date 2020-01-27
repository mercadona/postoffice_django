import requests
from requests import Response

from . import settings
from .models import PublishingError


def publish(topic: str, payload: dict, **attrs: dict) -> None:
    url = f'{settings.get_url()}/api/messages/'

    message = {'topic': topic, 'payload': payload, 'attributes': attrs}

    response = requests.post(url, json=message, timeout=settings.get_timeout())

    if response.status_code != 201:
        _save_publishing_error(response, message)


def _save_publishing_error(response: Response, message: dict) -> None:
    error = 'Uknown error'

    if response.status_code == 500:
        error = 'Internal server error'

    if response.status_code == 422:
        error = response.json().get('errors').get('detail')

    PublishingError.objects.create(
        topic=message.get('topic'),
        payload=message.get('payload'),
        attributes=message.get('attributes'),
        error=error,
    )
