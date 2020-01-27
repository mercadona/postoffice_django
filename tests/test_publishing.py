import datetime
import json
import os

import pytest
import pytz
import responses
from freezegun import freeze_time

from postoffice_django.models import PublishingError
from postoffice_django.publishing import publish

POST_OFFICE_URL = os.environ.get('POST_OFFICE_URL', 'http://post_office_url')


@pytest.mark.django_db
class TestPublishing:
    POST_SERVICE_PUBLISH_MESSAGE_URL = f'{POST_OFFICE_URL}/api/messages/'
    @pytest.fixture
    def post_service_valid_response(self):
        return json.dumps({'public_id': '12345'})

    @pytest.fixture
    def post_service_unprocessable_entity_response(self):
        return json.dumps({
            "errors": {
                "detail": "Unprocessable Entity"
            }
        })

    def test_request_body_sent_is_correct_when_has_not_attributes(self, post_service_valid_response):
        responses.add(responses.POST, self.POST_SERVICE_PUBLISH_MESSAGE_URL, status=201,
                      body=post_service_valid_response, content_type='application/json')
        payload = {
            'key': 'key_1',
            'key_2': 2
        }

        publish(topic='some_topic', payload=payload)

        assert json.loads(responses.calls[0].request.body) == {
            'topic': 'some_topic',
            'payload': {
                'key': 'key_1',
                'key_2': 2,
            },
            'attributes': {}
        }

    def test_send_valid_payload_with_attributes_when_has_attributes(self, post_service_valid_response):
        responses.add(responses.POST, self.POST_SERVICE_PUBLISH_MESSAGE_URL, status=201,
                      body=post_service_valid_response, content_type='application/json')

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        assert json.loads(responses.calls[0].request.body) == {
            'topic': 'some_topic',
            'payload': 'some_payload',
            'attributes': {'hive': 'vlc1'}
        }

    def test_do_not_save_publishing_error_when_service_success(self, post_service_valid_response):
        responses.add(responses.POST, self.POST_SERVICE_PUBLISH_MESSAGE_URL, status=201,
                      body=post_service_valid_response, content_type='application/json')

        publish(topic='some_topic', payload='some_payload')

        assert PublishingError.objects.count() == 0

    @freeze_time('2019-06-19 20:59:59+02:00')
    def test_save_publishing_error_when_service_returns_500(self):
        responses.add(responses.POST, self.POST_SERVICE_PUBLISH_MESSAGE_URL, status=500, body=json.dumps(''),
                      content_type='application/json')

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == 'Internal server error'
        assert publishing_error.created_at == datetime.datetime(2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)

    @freeze_time('2019-06-19 20:59:59+02:00')
    def test_save_publishing_error_when_service_returns_422(self, post_service_unprocessable_entity_response):
        responses.add(responses.POST, self.POST_SERVICE_PUBLISH_MESSAGE_URL, status=422,
                      body=post_service_unprocessable_entity_response, content_type='application/json')

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == 'Unprocessable Entity'
        assert publishing_error.created_at == datetime.datetime(2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)
