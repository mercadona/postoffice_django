import requests
from requests import Response
from requests.exceptions import ConnectionError, Timeout

from . import settings
from .models import PublishingError

CONNECTION_ERROR = 'Can not establish connection with postoffice'


def publish(topic: str, payload: dict, **attrs: dict) -> None:
    Publisher(topic, payload, **attrs).publish()


def bulk_publish(topic: str, payload: list, **attrs: dict) -> None:
    BulkPublisher(topic, payload, **attrs).publish()


class Publisher:
    URL = 'api/messages/'
    TIMEOUT = settings.get_timeout()

    def __init__(self, topic, payload, bulk=False, **attributes):
        self.url = f'{settings.get_url()}/{self.URL}'
        self.topic = topic
        self.payload = payload
        self.attributes = attributes
        self.timeout = self.TIMEOUT
        self.bulk = bulk
        self.message = self._create_message()

    def publish(self):
        try:
            response = requests.post(
                self.url, json=self.message, timeout=self.timeout)
        except (ConnectionError, Timeout):
            self._save_connection_not_established()
            return

        if response.status_code != 201:
            self._save_publishing_error(response)

    def _create_message(self) -> dict:
        return {
            'topic': self.topic,
            'payload': self.payload,
            'attributes': self._stringify_attributes()
        }

    def _stringify_attributes(self) -> dict:
        attributes = self.attributes
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
            payload=self.message,
            attributes=self.attributes,
            bulk=self.bulk,
            error=error,
        )


class BulkPublisher(Publisher):
    URL = 'api/bulk_messages/'
    TIMEOUT = settings.get_bulk_timeout()

    def __init__(self, topic, payload, **attributes):
        super().__init__(topic=topic, payload=payload, bulk=True, **attributes)

    def _create_message(self) -> list:
        return [{
            'topic': self.topic,
            'payload': message,
            'attributes': self._stringify_attributes()
        } for message in self.payload]
