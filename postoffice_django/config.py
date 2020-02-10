import logging

import requests
from responses import Response

from . import settings
from postoffice_django.exceptions import BadTopicCreation


logger = logging.getLogger(__name__)


def configure_publishers() -> None:

    for consumer in settings.get_consumers():
        _create_publishers(consumer)


def configure_topics() -> None:
    uncreated_topics = []

    for topic in settings.get_topics():
        if not _create_topic(topic):
            uncreated_topics.append(topic)

    if uncreated_topics:
        raise BadTopicCreation(uncreated_topics)


def _create_publishers(consumer: dict) -> None:
    url = f'{settings.get_url()}/api/publishers/'
    payload = {
        'active': True,
        'topic': consumer.get('topic'),
        'target': consumer.get('target'),
        'type': consumer.get('type'),
        'from_now': True
    }

    response = requests.post(url, json=payload)
    _save_creation_result_log(response)


def _create_topic(topic_name: str) -> None:
    url = f'{settings.get_url()}/api/topics/'
    payload = {'name': topic_name, 'origin_host': settings.get_origin_host()}

    response = requests.post(url, json=payload)

    return response.status_code == 201


def _save_creation_result_log(response: Response) -> None:
    if response.status_code == 201:
        logger.info(f'{response.url} succesfully creation')
    else:
        # raise BadTopicCreation(response.json()['data']['errors'])
        logger.error(f'{response.url} bad creation', extra=response.json())
