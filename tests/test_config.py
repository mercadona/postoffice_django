import json
import logging
from unittest.mock import patch

import pytest
import requests
import responses
from django.conf import settings

from postoffice_django.config import configure_publishers, configure_topics

POSTOFFICE_URL = settings.POSTOFFICE['URL']


@pytest.mark.django_db
class TestConfigurePublishers:
    @pytest.fixture
    def publisher_already_exists(self):
        return json.dumps({
            'data': {
                'errors': {
                    'target': [
                        'has already been taken'
                    ]
                }
            }
        })

    @pytest.fixture
    def publisher_with_validation_error(self):
        return json.dumps({
            'data': {
                'errors': {
                    'target': [
                        'This field is required'
                    ]
                }
            }
        })

    POSTOFFICE_PUBLISHER_CREATION_URL = f'{POSTOFFICE_URL}/api/publishers/'

    def test_request_body_sent_to_create_publishers(self):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=201,
                      body="",
                      content_type='application/json')

        configure_publishers()

        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'active': True,
            'target': 'http://www.some_url.com',
            'topic': 'some_topic',
            'type': 'http',
            'seconds_timeout': 20,
            'seconds_retry': 60,
            'from_now': True
        }
        assert json.loads(responses.calls[1].request.body) == {
            'active': True,
            'target': 'http://www.another_url.com',
            'topic': 'another_topic',
            'type': 'pubsub',
            'from_now': True
        }

    def test_do_not_raise_exception_when_can_not_create_publisher(
            self, publisher_with_validation_error, caplog):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=400,
                      body=publisher_with_validation_error,
                      content_type='application/json')

        configure_publishers()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Publisher cannot be created'
        ) in caplog.record_tuples

    def test_do_not_raise_exception_when_publisher_already_exists(
            self, publisher_already_exists, caplog):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=409,
                      body=publisher_already_exists,
                      content_type='application/json')

        configure_publishers()

        assert (
            'postoffice_django.config',
            logging.WARNING,
            'Existing resource'
        ) in caplog.record_tuples

    @patch('postoffice_django.config.requests.post')
    def test_do_not_raise_exception_when_postoffice_raises_timeout(
            self, post_mock, caplog):
        post_mock.side_effect = requests.exceptions.ConnectTimeout()

        configure_publishers()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Publisher cannot be created'
        ) in caplog.record_tuples

    @patch('postoffice_django.config.requests.post')
    def test_do_not_raise_exception_when_postoffice_raises_connection_error(
            self, post_mock, caplog):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        configure_publishers()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Publisher cannot be created'
        ) in caplog.record_tuples

    def test_try_create_all_publishers_when_some_publisher_fails(
            self, publisher_with_validation_error, caplog):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=400,
                      body=publisher_with_validation_error,
                      content_type='application/json')
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=201,
                      body="",
                      content_type='application/json')

        configure_publishers()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Publisher cannot be created'
        ) in caplog.record_tuples

        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'active': True,
            'target': 'http://www.some_url.com',
            'topic': 'some_topic',
            'type': 'http',
            'seconds_timeout': 20,
            'seconds_retry': 60,
            'from_now': True
        }
        assert json.loads(responses.calls[1].request.body) == {
            'active': True,
            'target': 'http://www.another_url.com',
            'topic': 'another_topic',
            'type': 'pubsub',
            'from_now': True
        }


@pytest.mark.django_db
class TestConfigureTopics:
    POSTOFFICE_TOPIC_CREATION_URL = f'{POSTOFFICE_URL}/api/topics/'

    @pytest.fixture
    def topic_already_exists(self):
        return json.dumps({
            'data': {
                'errors': {
                    'name': [
                        'has already been taken'
                    ]
                }
            }
        })

    @pytest.fixture
    def topic_with_error_validation(self):
        return json.dumps({
            'data': {
                'errors': {
                    'name': [
                        'This field is required'
                    ]
                }
            }
        })

    @pytest.fixture
    def settings_with_recovery_enabled(self, settings):
        postoffice = dict(settings.POSTOFFICE)
        postoffice['RECOVERY_ENABLED'] = True
        settings.POSTOFFICE = postoffice

    def test_request_body_sent_to_create_topic(self):
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=201,
                      body="",
                      content_type='application/json')

        configure_topics()

        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'name': 'topic_to_be_created',
            'origin_host': 'example.com/messages/',
            'recovery_enabled': False
        }
        assert json.loads(responses.calls[1].request.body) == {
            'name': 'another_topic_to_be_created',
            'origin_host': 'example.com/messages/',
            'recovery_enabled': False
        }

    @pytest.mark.usefixtures('settings_with_recovery_enabled')
    def test_recovery_enabled_sent_when_default_recovery_param_is_true(self):

        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=201,
                      body="",
                      content_type='application/json')

        configure_topics()

        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'name': 'topic_to_be_created',
            'origin_host': 'example.com/messages/',
            'recovery_enabled': True,
        }
        assert json.loads(responses.calls[1].request.body) == {
            'name': 'another_topic_to_be_created',
            'origin_host': 'example.com/messages/',
            'recovery_enabled': True,
        }

    def test_do_not_raise_exception_when_can_not_create_topics(
            self, topic_with_error_validation, caplog):
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=400,
                      body=topic_with_error_validation,
                      content_type='application/json')

        configure_topics()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Topic cannot be created'
        ) in caplog.record_tuples

    @patch('postoffice_django.config.requests.post')
    def test_raise_exception_when_postoffice_raises_timeout(
            self, post_mock, caplog):
        post_mock.side_effect = requests.exceptions.ConnectTimeout()

        configure_topics()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Topic cannot be created'
        ) in caplog.record_tuples

    @patch('postoffice_django.config.requests.post')
    def test_raise_exception_when_postoffice_raises_connection_error(
            self, post_mock, caplog):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        configure_topics()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Topic cannot be created'
        ) in caplog.record_tuples

    def test_try_create_all_topics_when_some_topic_fails(
            self, topic_already_exists, caplog):
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=400,
                      body=topic_already_exists,
                      content_type='application/json')
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=201,
                      body="",
                      content_type='application/json')

        configure_topics()

        assert (
            'postoffice_django.config',
            logging.ERROR,
            'Topic cannot be created'
        ) in caplog.record_tuples

        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'name': 'topic_to_be_created',
            'origin_host': 'example.com/messages/',
            'recovery_enabled': False
        }
        assert json.loads(responses.calls[1].request.body) == {
            'name': 'another_topic_to_be_created',
            'origin_host': 'example.com/messages/',
            'recovery_enabled': False
        }

    def test_do_not_raise_exception_when_topic_already_exists(
            self, topic_already_exists, caplog):
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=409,
                      body=topic_already_exists,
                      content_type='application/json')

        configure_topics()

        assert (
            'postoffice_django.config',
            logging.WARNING,
            'Existing resource'
        ) in caplog.record_tuples
