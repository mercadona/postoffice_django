from unittest.mock import patch

import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestConfigurePublishersCommand:
    @patch('postoffice_django.config.configure_publishers')
    def test_config_command(self, config_mock):
        call_command('configure_postoffice_publishers')

        config_mock.assert_called()


@pytest.mark.django_db
class TestConfigureTopicsCommand:
    @patch('postoffice_django.config.configure_topics')
    def test_config_command(self, config_mock):
        call_command('configure_postoffice_topics')

        config_mock.assert_called()


@pytest.mark.django_db
class TestConfigurePostofficeCommand:
    @patch('postoffice_django.config.configure_topics')
    @patch('postoffice_django.config.configure_publishers')
    def test_config_command(self, config_mock_topics, config_mock_publishers):
        call_command('configure_postoffice')

        config_mock_topics.assert_called()
        config_mock_publishers.assert_called()
