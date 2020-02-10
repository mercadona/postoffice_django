import json

import pytest
import responses
from django.conf import settings

from postoffice_django.config import configure_publishers

POSTOFFICE_URL = settings.POSTOFFICE['URL']


@pytest.mark.django_db
class TestConfigurePublishers:
    POSTOFFICE_TOPIC_CREATION_URL = f'{POSTOFFICE_URL}/api/topics/'
    POSTOFFICE_PUBLISHER_CREATION_URL = f'{POSTOFFICE_URL}/api/publishers/'

    def test_publishers(self, settings):
        responses.add(responses.POST, self.POSTOFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure_publishers()

        assert len(responses.calls) == 2

    # def test_request_body_sent_to_create_topic(self, settings):
    #     responses.add(responses.POST, self.POSTOFFICE_TOPIC_CREATION_URL, status=201,
    #                   body="", content_type='application/json')
    #     responses.add(responses.POST, self.POSTOFFICE_PUBLISHER_CREATION_URL, status=201,
    #                   body="", content_type='application/json')

    #     configure_publishers()

    #     assert json.loads(responses.calls[0].request.body) == {
    #         'name': 'some_topic', 'origin_host': 'example.com'
    #     }
    #     assert json.loads(responses.calls[2].request.body) == {
    #         'name': 'another_topic', 'origin_host': 'example.com'
    #     }

    def test_request_body_sent_to_create_publishers(self, settings):
        # responses.add(responses.POST, self.POSTOFFICE_TOPIC_CREATION_URL, status=201,
        #               body="", content_type='application/json')
        responses.add(responses.POST, self.POSTOFFICE_PUBLISHER_CREATION_URL, status=201,
                      body="", content_type='application/json')

        configure_publishers()

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
