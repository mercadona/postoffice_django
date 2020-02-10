import logging

import requests

from . import settings

logger = logging.getLogger(__name__)


def configure_publishers():

    for consumer in settings.get_consumers():
        _create_publishers(consumer)


def configure_topics():
    for topic in settings.get_topics():
        _create_topic(topic)


def _create_publishers(consumer):
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


def _create_topic(topic_name):
    url = f'{settings.get_url()}/api/topics/'
    payload = {'name': topic_name, 'origin_host': settings.get_origin_host()}

    response = requests.post(url, json=payload)
    _save_creation_result_log(response)


def _save_creation_result_log(response):
    if response.status_code == 201:
        logger.info(f'{response.url} succesfully creation')
    else:
        logger.error(f'{response.url} bad creation', extra=response.json())
