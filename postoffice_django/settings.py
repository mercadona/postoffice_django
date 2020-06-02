import logging
from typing import Any, List, Union

from django.conf import settings

from .exceptions import (
    OriginHostSettingNotDefined,
    UrlSettingNotDefined
)

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 0.5
DEFAULT_BULK_TIMEOUT = 5


def get_url() -> str:
    try:
        return settings.POSTOFFICE['URL']
    except KeyError:
        raise UrlSettingNotDefined


def get_consumers() -> List[dict]:
    try:
        return settings.POSTOFFICE['CONSUMERS']
    except KeyError:
        logger.warning('Consumers config key is missing')
        return []


def get_timeout() -> Union[float, Any]:
    try:
        timeout = settings.POSTOFFICE['TIMEOUT']
        return float(timeout)
    except KeyError:
        logger.info(
            f'Timeout not defined, using default value: {DEFAULT_TIMEOUT} (s)')
        return DEFAULT_TIMEOUT


def get_bulk_timeout() -> Union[float, Any]:
    try:
        timeout = settings.POSTOFFICE['BULK_TIMEOUT']
        return float(timeout)
    except KeyError:
        logger.info(
            'Bulk timeout not defined, '
            f'using default: {DEFAULT_BULK_TIMEOUT} (s)')
        return DEFAULT_BULK_TIMEOUT


def get_origin_host() -> str:
    try:
        return settings.POSTOFFICE['ORIGIN_HOST']
    except KeyError:
        raise OriginHostSettingNotDefined


def get_topics() -> List[str]:
    try:
        return settings.POSTOFFICE['TOPICS']
    except KeyError:
        logger.warning('Topics config key is missing')
        return []
