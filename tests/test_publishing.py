import datetime
import json
from unittest.mock import patch

import pytest
import pytz
import requests
import responses
from django.conf import settings
from freezegun import freeze_time

from postoffice_django.models import PublishingError
from postoffice_django.publishing import publish, bulk_publish

POSTOFFICE_URL = settings.POSTOFFICE['URL']


@pytest.mark.django_db
class TestPublishing:
    POSTOFFICE_PUBLISH_MESSAGE_URL = f'{POSTOFFICE_URL}/api/messages/'

    @pytest.fixture
    def postoffice_valid_response(self):
        return json.dumps({'public_id': '12345'})

    @pytest.fixture
    def postoffice_publishing_error_response(self):
        return json.dumps({'data': {'errors': {'topic': ['is invalid']}}})

    def test_request_body_sent_is_correct_when_has_not_attributes(
            self, postoffice_valid_response):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISH_MESSAGE_URL,
                      status=201,
                      body=postoffice_valid_response,
                      content_type='application/json')
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

    def test_send_valid_payload_with_attributes_when_has_attributes(
            self, postoffice_valid_response):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISH_MESSAGE_URL,
                      status=201,
                      body=postoffice_valid_response,
                      content_type='application/json')

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        assert json.loads(responses.calls[0].request.body) == {
            'topic': 'some_topic',
            'payload': 'some_payload',
            'attributes': {'hive': 'vlc1'}
        }

    def test_send_all_attributes_as_string(self, postoffice_valid_response):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISH_MESSAGE_URL,
                      status=201,
                      body=postoffice_valid_response,
                      content_type='application/json')

        publish(topic='some_topic',
                payload={'key': 'value'},
                number=1,
                boolean=False)

        assert json.loads(responses.calls[0].request.body) == {
            'topic': 'some_topic',
            'payload': {'key': 'value'},
            'attributes': {
                'number': '1',
                'boolean': 'False'
            }
        }

    def test_do_not_save_publishing_error_when_service_success(
            self, postoffice_valid_response):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISH_MESSAGE_URL,
                      status=201,
                      body=postoffice_valid_response,
                      content_type='application/json')

        publish(topic='some_topic', payload='some_payload')

        assert PublishingError.objects.count() == 0

    @freeze_time('2019-06-19 20:59:59+02:00')
    def test_save_publishing_error_when_service_returns_500(self):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISH_MESSAGE_URL,
                      status=500,
                      body=json.dumps(''),
                      content_type='application/json')

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == 'Internal server error'
        assert publishing_error.created_at == datetime.datetime(
            2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)
        assert not publishing_error.bulk

    @freeze_time('2019-06-19 20:59:59+02:00')
    def test_save_publishing_error_when_service_returns_400(
            self, postoffice_publishing_error_response):
        responses.add(responses.POST,
                      self.POSTOFFICE_PUBLISH_MESSAGE_URL,
                      status=400,
                      body=postoffice_publishing_error_response,
                      content_type='application/json')

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == '{\'topic\': [\'is invalid\']}'
        assert publishing_error.created_at == datetime.datetime(
            2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)
        assert not publishing_error.bulk

    @freeze_time('2019-06-19 20:59:59+02:00')
    @patch('postoffice_django.publishing.requests.post')
    def test_save_publishing_error_when_postoffice_raises_timeout(
            self, post_mock):
        post_mock.side_effect = requests.exceptions.Timeout()

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == (
            'Can not establish connection with postoffice')
        assert publishing_error.created_at == datetime.datetime(
            2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)

    @freeze_time('2019-06-19 20:59:59+02:00')
    @patch('postoffice_django.publishing.requests.post')
    def test_save_publishing_error_when_postoffice_raises_connection_error(
            self, post_mock):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        publish(topic='some_topic', payload='some_payload', hive='vlc1')

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == (
            'Can not establish connection with postoffice')
        assert publishing_error.created_at == datetime.datetime(
            2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)


@pytest.mark.django_db
class TestBulkPublishing:

    @patch('postoffice_django.publishing.requests.post')
    def test_bulk_messages_endpoint_called_when_calling_bulk_publish(
            self, post_mock):
        bulk_publish(
            topic='some_topic',
            payload=[{'key': 'key_1'}, {'key': 'key_2'}],
            hive='vlc1',
        )

        post_mock.assert_called_with(
            'http://fake.service/api/bulk_messages/',
            json=[{
                'topic': 'some_topic',
                'payload': {'key': 'key_1'},
                'attributes': {'hive': 'vlc1'}
            }, {
                'topic': 'some_topic',
                'payload': {'key': 'key_2'},
                'attributes': {'hive': 'vlc1'}
            }],
            timeout=0.3
        )

    @freeze_time('2019-06-19 20:59:59+02:00')
    @patch('postoffice_django.publishing.requests.post')
    def test_save_error_when_connection_error_raised(self, post_mock):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        bulk_publish(
            topic='some_topic',
            payload=[{'key': 'key_1'}, {'key': 'key_2'}],
            hive='vlc1',
        )

        assert PublishingError.objects.count() == 1
        publishing_error = PublishingError.objects.first()
        assert publishing_error.bulk
        assert publishing_error.payload == [{
            'topic': 'some_topic',
            'payload': {'key': 'key_1'},
            'attributes': {'hive': 'vlc1'}
        }, {
            'topic': 'some_topic',
            'payload': {'key': 'key_2'},
            'attributes': {'hive': 'vlc1'}
        }]
