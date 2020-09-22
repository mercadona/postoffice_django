import json
from datetime import timedelta

import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from requests import Response
from requests.exceptions import ConnectionError, Timeout

from . import settings
from .models import PublishingError

CONNECTION_ERROR = 'Can not establish connection with postoffice'


def publish(topic: str, payload: dict, **attrs: dict) -> None:
    Publisher(topic, payload, **attrs).publish()


def bulk_publish(topic: str, payload: list, **attrs: dict) -> None:
    BulkPublisher(topic, payload, **attrs).publish()


def scheduled_publish(topic: str, payload: dict, schedule_in: int, **attrs: dict) -> None:
    ScheduledPublisher(topic, payload, schedule_in, **attrs).publish()


class Publisher:
    URL = 'api/messages/'
    TIMEOUT = settings.get_timeout()

    def __init__(self, topic, payload, bulk=False, **attributes):
        self.url = f'{settings.get_url()}/{self.URL}'
        self.topic = topic
        self.payload = payload
        self.attributes = self._stringify(attributes)
        self.timeout = self.TIMEOUT
        self.bulk = bulk
        self.message = self._create_message()

    def publish(self):
        try:
            message = json.dumps(self.message, cls=DjangoJSONEncoder)
            response = requests.post(
                self.url, data=message, headers={'Content-Type': 'application/json'}, timeout=self.timeout)
        except (ConnectionError, Timeout):
            self._save_connection_not_established()
            return

        if response.status_code != 201:
            self._save_publishing_error(response)

    def _create_message(self) -> dict:
        return {
            'topic': self.topic,
            'payload': self.payload,
            'attributes': self.attributes,
        }

    def _stringify(self, attributes) -> dict:
        return {key: str(attributes[key]) for key in attributes.keys()}

    def _save_connection_not_established(self) -> None:
        self._create_publishing_error(CONNECTION_ERROR)

    def _save_publishing_error(self, response: Response) -> None:
        error = 'Unknown error'

        if response.status_code == 500:
            error = 'Internal server error'

        if response.status_code == 400:
            error = response.json().get('data').get('errors')

        self._create_publishing_error(error)

    def _create_publishing_error(self, error: str) -> None:
        PublishingError.objects.create(
            topic=self.topic,
            payload=self._error_payload(),
            attributes=self.attributes,
            bulk=self.bulk,
            error=error,
        )

    def _error_payload(self):
        return self.payload


class BulkPublisher(Publisher):
    URL = 'api/bulk_messages/'
    TIMEOUT = settings.get_bulk_timeout()

    def __init__(self, topic, payload, **attributes):
        super().__init__(topic=topic, payload=payload, bulk=True, **attributes)

    def _create_publishing_error(self, error: str) -> None:
        PublishingError.objects.create(
            topic=self.topic,
            payload=self._create_failed_message(),
            attributes=self.attributes,
            bulk=self.bulk,
            error=error,
        )

    def _create_failed_message(self) -> list:
        return [{
            'topic': self.topic,
            'attributes': self.attributes,
            'payload': message_payload
        } for message_payload in self.payload]

    def _error_payload(self):
        return self.message


class ScheduledPublisher(Publisher):
    URL = 'api/schedule_messages/'

    def __init__(self, topic, payload, schedule_in, **attributes):
        self.schedule_in = schedule_in
        super().__init__(topic=topic, payload=payload, **attributes)

    def _create_message(self) -> dict:
        message = super()._create_message()
        message['schedule_at'] = timezone.now() + timedelta(minutes=self.schedule_in)
        return message
