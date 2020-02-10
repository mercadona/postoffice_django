from unittest.mock import patch

import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestConfigurePublishersCommand:
    @patch('postoffice_django.config.configure_publishers')
    def test_config_command(self, config_mock):
        call_command('configure_post_office_publishers')

        config_mock.assert_called()
