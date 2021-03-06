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
from postoffice_django.publishing import publish, bulk_publish, scheduled_publish

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
                payload={'key': 'value', 'occurred_at': datetime.datetime(2020, 8, 5, 12, 3, tzinfo=pytz.utc)},
                number=1,
                boolean=False)

        request = responses.calls[0].request

        assert json.loads(request.body) == {
            'topic': 'some_topic',
            'payload': {'key': 'value', 'occurred_at': '2020-08-05T12:03:00Z'},
            'attributes': {
                'number': '1',
                'boolean': 'False'
            }
        }
        assert request.headers['Content-Type'] == 'application/json'

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

        publish(topic='some_topic', payload='some_payload',
                hive='vlc1', published_at=12345.0)

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == 'Internal server error'
        assert publishing_error.created_at == datetime.datetime(
            2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)
        assert not publishing_error.bulk
        assert publishing_error.payload == 'some_payload'
        assert publishing_error.attributes == {
            'hive': 'vlc1', 'published_at': '12345.0'}

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
        assert publishing_error.payload == 'some_payload'

    @freeze_time('2019-06-19 20:59:59+02:00')
    @patch('postoffice_django.publishing.requests.post')
    def test_save_publishing_error_with_datetimes_when_postofice_raises_connection_error(
        self, post_mock
    ):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        custom_datetime = '2019-06-19 19:00:00+00:00'

        payload = {
            'what': 'something happened',
            'when': datetime.datetime.fromisoformat(custom_datetime)
        }

        publish(
            topic='some_topic',
            payload=payload,
            hive='vlc1',
            custom_published_at=datetime.datetime.fromisoformat(custom_datetime)
        )

        publishing_error = PublishingError.objects.first()
        assert PublishingError.objects.count() == 1
        assert publishing_error.error == 'Can not establish connection with postoffice'
        assert publishing_error.created_at == datetime.datetime(
            2019, 6, 19, 18, 59, 59, tzinfo=pytz.UTC)
        assert publishing_error.attributes['custom_published_at'] == custom_datetime
        assert publishing_error.payload == {
            'what': 'something happened',
            'when': '2019-06-19T19:00:00Z'
        }


@pytest.mark.django_db
class TestBulkPublishing:

    @patch('postoffice_django.publishing.requests.post')
    def test_bulk_messages_endpoint_called_when_calling_bulk_publish(
            self, post_mock):
        expected_data = (
            '{'
            '"topic": "some_topic", '
            '"payload": [{"key": "key_1"}, {"key": "key_2"}], '
            '"attributes": {"hive": "vlc1"}'
            '}'
        )
        bulk_publish(
            topic='some_topic',
            payload=[{'key': 'key_1'}, {'key': 'key_2'}],
            hive='vlc1',
        )

        post_mock.assert_called_with(
            'http://fake.service/api/bulk_messages/',
            data=expected_data,
            headers={'Content-Type': 'application/json'},
            timeout=1.2
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


@pytest.mark.django_db
class TestScheduledPublishing:

    @patch('postoffice_django.publishing.requests.post')
    @freeze_time('2020-09-22 07:00:00+00:00')
    def test_schedule_messages_endpoint_called_when_calling_schedule_publish(self, post_mock):
        expected_data = (
            '{'
            '"topic": "some_topic", '
            '"payload": {"key": "key_1"}, '
            '"attributes": {"hive": "vlc1"}, '
            '"schedule_at": "2020-09-22T07:15:00Z"'
            '}'
        )
        scheduled_publish(
            topic='some_topic',
            payload={'key': 'key_1'},
            schedule_in=15,
            **{'hive': 'vlc1'},
        )

        post_mock.assert_called_with(
            'http://fake.service/api/schedule_messages/',
            data=expected_data,
            headers={'Content-Type': 'application/json'},
            timeout=0.3,
        )

    @freeze_time('2020-09-22 07:00:00+00:00')
    @patch('postoffice_django.publishing.requests.post')
    def test_save_error_when_connection_error_raised(self, post_mock):
        post_mock.side_effect = requests.exceptions.ConnectionError()

        scheduled_publish(
            topic='some_topic',
            payload={'key': 'key_1'},
            schedule_in=15,
            **{'hive': 'vlc1'},
        )

        assert PublishingError.objects.count() == 1
        publishing_error = PublishingError.objects.first()
        assert not publishing_error.bulk
        assert publishing_error.payload == {'key': 'key_1'}
        assert publishing_error.topic == 'some_topic'
        assert publishing_error.attributes == {'hive': 'vlc1'}
        assert publishing_error.created_at == datetime.datetime(2020, 9, 22, 7, 0, 0, tzinfo=pytz.UTC)
