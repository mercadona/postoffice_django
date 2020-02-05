import json
import os

import pytest
import responses

from django.conf import settings

from postoffice_django.config import configure

POSTOFFICE_URL = settings.POSTOFFICE_URL


@pytest.mark.django_db
class TestConfig:
    POSTOFFICE_TOPIC_CREATION_URL = f'{POSTOFFICE_URL}/api/topics/'
    POSTOFFICE_PUBLISHER_CREATION_URL = f'{POSTOFFICE_URL}/api/publishers/'

    def test_create_topics_and_publishers(self, settings):
        responses.add(responses.POST, self.POSTOFFICE_TOPIC_CREATION_URL, status=201,
                      body="", content_type='application/json')
        responses.add(responses.POST, self.POSTOFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure()

        assert len(responses.calls) == 4

    def test_request_body_sent_to_create_topic(self, settings):
        responses.add(responses.POST, self.POSTOFFICE_TOPIC_CREATION_URL, status=201,
                      body="", content_type='application/json')
        responses.add(responses.POST, self.POSTOFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure()

        assert json.loads(responses.calls[0].request.body) == {
            'name': 'some_topic', 'origin_host': 'example.com'
        }
        assert json.loads(responses.calls[2].request.body) == {
            'name': 'another_topic', 'origin_host': 'example.com'
        }

    def test_request_body_sent_to_create_publishers(self, settings):
        responses.add(responses.POST, self.POSTOFFICE_TOPIC_CREATION_URL, status=201,
                      body="", content_type='application/json')
        responses.add(responses.POST, self.POSTOFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure()

        assert json.loads(responses.calls[1].request.body) == {
            'active': True,
            'endpoint': 'http://www.some_url.com',
            'topic': 'some_topic',
            'type': 'http',
            'from_now': True
        }
        assert json.loads(responses.calls[3].request.body) == {
            'active': True,
            'endpoint': 'http://www.another_url.com',
            'topic': 'another_topic',
            'type': 'pubsub',
            'from_now': True
        }
