import json
from unittest.mock import patch

import requests
import responses
from django.conf import settings

from postoffice_django import checks

POSTOFFICE_URL = settings.POSTOFFICE['URL']


class TestPostOfficeHealth:
    def test_returns_true_when_postoffice_is_ok(self):
        responses.add(responses.GET, f'{POSTOFFICE_URL}/api/health/',
                      body=json.dumps({'status': 'ok'}))

        assert checks.health() is True

    def test_returns_false_when_postoffice_is_ko(self):
        responses.add(responses.GET, f'{POSTOFFICE_URL}/api/health/',
                      body=json.dumps({'status': 'ko'}))

        assert checks.health() is False

    def test_returns_false_when_postoffice_returns_internal_server_error(self):
        responses.add(responses.GET, f'{POSTOFFICE_URL}/api/health/',
                      body=json.dumps({}), status=500)

        assert checks.health() is False

    @patch('requests.get')
    def test_returns_false_when_postoffice_raises_timeout(self, get_mock):
        get_mock.side_effect = requests.exceptions.ConnectTimeout()

        assert checks.health() is False

    @patch('requests.get')
    def test_returns_false_when_postoffice_raises_connection_error(
            self, get_mock):
        get_mock.side_effect = requests.exceptions.ConnectionError()

        assert checks.health() is False
