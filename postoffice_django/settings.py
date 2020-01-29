import logging
from decimal import Decimal

from django.conf import settings

from .exceptions import ConsumersSettingNotDefined, UrlSettingNotDefined

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 0.5


def get_url() -> str:
    try:
        return settings.POSTOFFICE_URL
    except AttributeError:
        raise UrlSettingNotDefined


def get_consumers() -> str:
    try:
        return settings.POSTOFFICE_CONSUMERS
    except AttributeError:
        raise ConsumersSettingNotDefined


def get_timeout() -> Decimal:
    try:
        return settings.POSTOFFICE_TIMEOUT
    except AttributeError:
        logger.info(
            f'Timeout not defined, using default value: {DEFAULT_TIMEOUT} (s)')
        return DEFAULT_TIMEOUT
