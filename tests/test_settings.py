import pytest

from postoffice_django.exceptions import ConsumersSettingNotDefined, UrlSettingNotDefined

from postoffice_django.settings import get_consumers, get_timeout, get_url


class SettingsTest:
    def test_raise_exception_when_post_office_url_is_not_defined(self, settings):
        del(settings.POST_OFFICE_URL)

        with pytest.raises(UrlSettingNotDefined):
            get_url()

    def test_raise_exception_when_post_office_consumers_is_not_defined(self, settings):
        del(settings.POST_OFFICE_CONSUMERS)

        with pytest.raises(ConsumersSettingNotDefined):
            get_consumers()

    def test_returns_default_timeout_value_when_is_not_defined(self, settings):
        del(settings.POST_OFFICE_TIMEOUT)

        assert 0.5 == get_timeout()
