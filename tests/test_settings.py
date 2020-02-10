import pytest

from postoffice_django.exceptions import (
    ConsumersSettingNotDefined,
    OriginHostSettingNotDefined,
    UrlSettingNotDefined
)
from postoffice_django.settings import (
    get_consumers,
    get_origin_host,
    get_timeout,
    get_url
)


class TestSettings:
    def test_raise_exception_when_post_office_url_is_not_defined(self, settings):
        del(settings.POSTOFFICE['URL'])

        with pytest.raises(UrlSettingNotDefined):
            get_url()

    def test_raise_exception_when_post_office_consumers_is_not_defined(self, settings):
        del(settings.POSTOFFICE['CONSUMERS'])

        with pytest.raises(ConsumersSettingNotDefined):
            get_consumers()

    def test_returns_default_timeout_value_when_is_not_defined(self, settings):
        del(settings.POSTOFFICE['TIMEOUT'])

        assert 0.5 == get_timeout()

    def test_raise_exception_when_origin_host_is_not_defined(self, settings):
        del(settings.POSTOFFICE['ORIGIN_HOST'])

        with pytest.raises(OriginHostSettingNotDefined):
            get_origin_host()
