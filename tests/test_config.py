import json
from unittest.mock import patch

import pytest
import requests
import responses
from django.conf import settings

from postoffice_django.config import configure_publishers, configure_topics
from postoffice_django.exceptions import BadPublisherCreation, BadTopicCreation

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
            'from_now': True
        }
        assert json.loads(responses.calls[1].request.body) == {
            'active': True,
            'target': 'http://www.another_url.com',
            'topic': 'another_topic',
            'type': 'pubsub',
            'from_now': True
        }

    def test_raise_exception_when_can_not_create_publisher(
            self, publisher_already_exists):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=400,
                      body=publisher_already_exists,
                      content_type='application/json')

        with pytest.raises(BadPublisherCreation):
            configure_publishers()

    @patch('postoffice_django.config.requests.post')
    def test_raise_exception_when_postoffice_raises_timeout(
            self, post_mock):
        post_mock.side_effect = requests.exceptions.ConnectTimeout()

        with pytest.raises(BadPublisherCreation):
            configure_publishers()

    @patch('postoffice_django.config.requests.post')
    def test_raise_exception_when_postoffice_raises_connection_error(
            self, post_mock):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(BadPublisherCreation):
            configure_publishers()

    def test_try_create_all_publishers_when_some_publisher_fails(
            self, publisher_already_exists):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=400,
                      body=publisher_already_exists,
                      content_type='application/json')
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISHER_CREATION_URL,
                      status=201,
                      body="",
                      content_type='application/json')

        with pytest.raises(
                BadPublisherCreation) as bad_publisher_creation_exception:
            configure_publishers()

        assert bad_publisher_creation_exception.value.message == (
            'Can not create publisher. Publisher not created: [{\'topic\': \'some_topic\', \'target\': \'http://www.some_url.com\', \'type\': \'http\', \'from_now\': True}]'  # noqa
        )
        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'active': True,
            'target': 'http://www.some_url.com',
            'topic': 'some_topic',
            'type': 'http',
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
            'origin_host': 'example.com/messages/'
        }
        assert json.loads(responses.calls[1].request.body) == {
            'name': 'another_topic_to_be_created',
            'origin_host': 'example.com/messages/'
        }

    def test_raise_exception_when_can_not_create_topics(
            self, topic_already_exists):
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=400,
                      body=topic_already_exists,
                      content_type='application/json')

        with pytest.raises(BadTopicCreation):
            configure_topics()

    @patch('postoffice_django.config.requests.post')
    def test_raise_exception_when_postoffice_raises_timeout(
            self, post_mock):
        post_mock.side_effect = requests.exceptions.ConnectTimeout()

        with pytest.raises(BadTopicCreation):
            configure_topics()

    @patch('postoffice_django.config.requests.post')
    def test_raise_exception_when_postoffice_raises_connection_error(
            self, post_mock):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(BadTopicCreation):
            configure_topics()

    def test_try_create_all_topics_when_some_topic_fails(
            self, topic_already_exists):
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

        with pytest.raises(BadTopicCreation) as bad_topic_creation_exception:
            configure_topics()

        assert bad_topic_creation_exception.value.message == 'Can not create topic. Topic no created: [\'topic_to_be_created\']'  # noqa
        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'name': 'topic_to_be_created',
            'origin_host': 'example.com/messages/'
        }
        assert json.loads(responses.calls[1].request.body) == {
            'name': 'another_topic_to_be_created',
            'origin_host': 'example.com/messages/'
        }
