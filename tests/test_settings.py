import logging
import pytest

from postoffice_django.exceptions import (
    OriginHostSettingNotDefined,
    UrlSettingNotDefined
)
from postoffice_django.settings import (
    get_consumers,
    get_origin_host,
    get_timeout,
    get_topics,
    get_url
)


class TestSettings:
    def test_raise_exception_when_post_office_url_is_not_defined(
            self, settings):
        del(settings.POSTOFFICE['URL'])

        with pytest.raises(UrlSettingNotDefined):
            get_url()

    def test_returns_empty_list_when_post_office_consumers_is_not_defined(
            self, settings, caplog):
        del(settings.POSTOFFICE['CONSUMERS'])

        assert get_consumers() == []
        assert (
            'postoffice_django.settings',
            logging.WARNING,
            'Consumers config key is missing'
        ) in caplog.record_tuples

    def test_returns_default_timeout_value_when_is_not_defined(
            self, settings):
        del(settings.POSTOFFICE['TIMEOUT'])

        assert 0.5 == get_timeout()

    def test_raise_exception_when_origin_host_is_not_defined(
            self, settings):
        del(settings.POSTOFFICE['ORIGIN_HOST'])

        with pytest.raises(OriginHostSettingNotDefined):
            get_origin_host()

    def test_raise_exception_when_topics_is_not_defined(
            self, settings, caplog):
        del(settings.POSTOFFICE['TOPICS'])

        assert get_topics() == []
        assert (
            'postoffice_django.settings',
            logging.WARNING,
            'Topics config key is missing'
        ) in caplog.record_tuples