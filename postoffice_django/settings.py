import logging
from typing import Union, Any, List

from django.conf import settings

from .exceptions import ConsumersSettingNotDefined, UrlSettingNotDefined, OriginHostSettingNotDefined

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 0.5


def get_url() -> str:
    try:
        return settings.POSTOFFICE['URL']
    except KeyError:
        raise UrlSettingNotDefined


def get_consumers() -> List[dict]:
    try:
        return settings.POSTOFFICE['CONSUMERS']
    except KeyError:
        raise ConsumersSettingNotDefined


def get_timeout() -> Union[float, Any]:
    try:
        return settings.POSTOFFICE['TIMEOUT']
    except KeyError:
        logger.info(
            f'Timeout not defined, using default value: {DEFAULT_TIMEOUT} (s)')
        return DEFAULT_TIMEOUT


def get_origin_host() -> str:
    try:
        return settings.POSTOFFICE['ORIGIN_HOST']
    except KeyError:
        raise OriginHostSettingNotDefined
