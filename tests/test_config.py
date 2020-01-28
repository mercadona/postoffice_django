import json
import os

import pytest
import responses

from postoffice_django.config import configure

POST_OFFICE_URL = os.environ.get('POST_OFFICE_URL', 'http://post_office_url')


@pytest.mark.django_db
class TestConfig:
    POST_OFFICE_TOPIC_CREATION_URL = f'{POST_OFFICE_URL}/api/topics/'
    POST_OFFICE_PUBLISHER_CREATION_URL = f'{POST_OFFICE_URL}/api/publishers/'

    @pytest.fixture
    def consumers(self):
        return [
            {
                'topic': 'some_topic',
                'endpoint': 'http://www.some_url.com',
                'type': 'http'
            },
            {
                'topic': 'another_topic',
                'endpoint': 'http://www.another_url.com',
                'type': 'http'
            }
        ]

    def test_create_topics_and_publishers(self, settings, consumers):
        settings.POST_OFFICE_CONSUMERS = consumers
        responses.add(responses.POST, self.POST_OFFICE_TOPIC_CREATION_URL, status=201,
                      body="", content_type='application/json')
        responses.add(responses.POST, self.POST_OFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure()

        assert len(responses.calls) == 4

    def test_request_body_sent_to_create_topic(self, settings, consumers):
        settings.POST_OFFICE_CONSUMERS = consumers
        responses.add(responses.POST, self.POST_OFFICE_TOPIC_CREATION_URL, status=201,
                      body="", content_type='application/json')
        responses.add(responses.POST, self.POST_OFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure()

        assert json.loads(responses.calls[0].request.body) == {
            'name': 'some_topic'
        }
        assert json.loads(responses.calls[2].request.body) == {
            'name': 'another_topic'
        }

    def test_request_body_sent_to_create_publishers(self, settings, consumers):
        settings.POST_OFFICE_CONSUMERS = consumers
        responses.add(responses.POST, self.POST_OFFICE_TOPIC_CREATION_URL, status=201,
                      body="", content_type='application/json')
        responses.add(responses.POST, self.POST_OFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure()

        assert json.loads(responses.calls[1].request.body) == {
            'active': True,
            'endpoint': 'http://www.some_url.com',
            'topic': 'some_topic',
            'type': 'http',
            'initial_message': 0,
            'from_now': True
        }
        assert json.loads(responses.calls[3].request.body) == {
            'active': True,
            'endpoint': 'http://www.another_url.com',
            'topic': 'another_topic',
            'type': 'http',
            'initial_message': 0,
            'from_now': True
        }
