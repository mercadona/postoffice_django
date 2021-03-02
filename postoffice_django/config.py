import logging
from collections import namedtuple
from http import HTTPStatus

import requests
from django.urls import reverse
from requests.exceptions import ConnectionError, ConnectTimeout

from . import settings

logger = logging.getLogger(__name__)

ConfigurationResponse = namedtuple('ConfigurationResponse', ['report_error'])


def configure_publishers() -> None:
    uncreated_publishers = []

    for consumer in settings.get_consumers():
        if _create_publishers(consumer).report_error:
            uncreated_publishers.append(consumer)

    if uncreated_publishers:
        logger.error('Publisher cannot be created',
                     extra={'uncreated_publishers': uncreated_publishers})


def configure_topics() -> None:
    uncreated_topics = []

    for topic in settings.get_topics():
        if _create_topic(topic).report_error:
            uncreated_topics.append(topic)

    if uncreated_topics:
        logger.error('Topic cannot be created',
                     extra={'uncreated_topics': uncreated_topics})


def _create_publishers(consumer: dict) -> ConfigurationResponse:
    url = f'{settings.get_url()}/api/publishers/'
    payload = {
        'active': True,
        'topic': consumer.get('topic'),
        'target': consumer.get('target'),
        'type': consumer.get('type'),
        'from_now': True
    }

    payload.update(_get_optional_args(consumer))

    return _execute_request(url, payload)


def _get_optional_args(consumer: dict) -> dict:
    return {**_get_publisher_retry(consumer), **_get_publisher_timeout(consumer)}


def _get_publisher_timeout(consumer: dict) -> dict:
    if not consumer.get('timeout'):
        return {}
    return {'seconds_timeout': consumer.get('timeout')}


def _get_publisher_retry(consumer: dict) -> dict:
    if not consumer.get('retry'):
        return {}
    return {'seconds_retry': consumer.get('retry')}


def _create_topic(topic_name: str) -> ConfigurationResponse:
    url = f'{settings.get_url()}/api/topics/'
    payload = {'name': topic_name, 'origin_host': _generate_origin_host()}

    return _execute_request(url, payload)


def _generate_origin_host() -> str:
    return settings.get_origin_host() + reverse('postoffice-messages-list')


def _execute_request(url: str, payload: dict) -> ConfigurationResponse:
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=settings.get_timeout()
        )
    except (ConnectTimeout, ConnectionError):
        return ConfigurationResponse(report_error=True)

    if response.status_code == HTTPStatus.CONFLICT:
        logger.warning('Existing resource',
                       extra={'url': url, 'payload': payload})
        return ConfigurationResponse(report_error=False)

    if response.status_code == HTTPStatus.CREATED:
        return ConfigurationResponse(report_error=False)

    return ConfigurationResponse(report_error=True)
