import json

import pytest
import responses
from django.conf import settings

from postoffice_django.config import configure_publishers, configure_topics
from postoffice_django.exceptions import BadTopicCreation


POSTOFFICE_URL = settings.POSTOFFICE['URL']


@pytest.mark.django_db
class TestConfigurePublishers:
    POSTOFFICE_PUBLISHER_CREATION_URL = f'{POSTOFFICE_URL}/api/publishers/'

    def test_request_body_sent_to_create_publishers(self, settings):
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

    # def test_raise_exception_when_can_not_create_publishers(self, settings):
    #     responses.add(responses.POST,
    #                   self.POSTOFFICE_PUBLISHER_CREATION_URL,
    #                   status=400,
    #                   body="",
    #                   content_type='application/json')

    #     configure_publishers()


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

    def test_request_body_sent_to_create_topic(self, settings):
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=201,
                      body="",
                      content_type='application/json')

        configure_topics()

        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'name': 'topic_to_be_created', 'origin_host': 'example.com'
        }
        assert json.loads(responses.calls[1].request.body) == {
            'name': 'another_topic_to_be_created', 'origin_host': 'example.com'
        }

    def test_raise_exception_when_can_not_create_topics(
            self, settings, topic_already_exists):
        responses.add(responses.POST,
                      self.POSTOFFICE_TOPIC_CREATION_URL,
                      status=400,
                      body=topic_already_exists,
                      content_type='application/json')

        with pytest.raises(BadTopicCreation):
            configure_topics()

    def test_try_create_all_topics_when_some_topic_fails(
            self, settings, topic_already_exists):
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

        assert bad_topic_creation_exception.value.message == (
            'Can not create topic. Errors: [\'topic_to_be_created\']')
        assert len(responses.calls) == 2
        assert json.loads(responses.calls[0].request.body) == {
            'name': 'topic_to_be_created', 'origin_host': 'example.com'
        }
        assert json.loads(responses.calls[1].request.body) == {
            'name': 'another_topic_to_be_created', 'origin_host': 'example.com'
        }
