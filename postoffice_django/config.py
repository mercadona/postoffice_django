import logging

import requests

from . import settings

logger = logging.getLogger(__name__)


def configure():

    for consumer in settings.get_consumers():
        _create_topic(consumer.get('topic'))
        _create_publishers(consumer)


def _create_topic(topic_name):
    url = f'{settings.get_url()}/api/topics/'
    payload = {'name': topic_name}

    response = requests.post(url, json=payload)
    _save_creation_result_log(response)


def _create_publishers(consumer):
    url = f'{settings.get_url()}/api/publishers/'
    payload = {
        'active': True,
        'topic': consumer.get('topic'),
        'endpoint': consumer.get('endpoint'),
        'type': consumer.get('type'),
        'from_now': True
    }

    response = requests.post(url, json=payload)
    _save_creation_result_log(response)


def _save_creation_result_log(response):
    if response.status_code == 201:
        logger.info(f'{response.url} succesfully creation')
    else:
        logger.error(f'{response.url} bad creation', extra=response.json())
