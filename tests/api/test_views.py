import json
from unittest.mock import patch

import pytest

from postoffice_django.models import PublishingError


@pytest.mark.django_db
class TestListMessagesView:

    def test_returns_empty_when_no_publishing_errors_exist(self, client):
        response = client.get('/messages/')

        assert response.status_code == 200
        assert json.loads(response.content) == []

    def test_returns_ordered_messages_when_publishing_errors_exist(
            self, client, publishing_error, older_publishing_error):
        response = client.get('/messages/')

        assert response.status_code == 200
        assert json.loads(response.content) == [{
            'id': older_publishing_error.id,
            'topic': 'test-topic',
            'attributes': None,
            'payload': {'approved': True},
            'bulk': False,
        }, {
            'id': publishing_error.id,
            'topic': 'test',
            'payload': {'key': 'value', 'num': '2.15', 'elements': [1, 2, 3]},
            'attributes': {'key': 'value'},
            'bulk': False,
        }]

    def test_returns_bulk_message_when_bulk_publishing_error_exists(
            self, client, bulk_publishing_error):
        response = client.get('/messages/')

        assert response.status_code == 200
        assert json.loads(response.content) == [{
            'id': bulk_publishing_error.id,
            'topic': 'test-topic',
            'attributes': None,
            'payload': [
                {'topic': 'test-topic', 'payload': {'approved': True}},
                {'topic': 'test-topic', 'payload': {'approved': False}},
            ],
            'bulk': True,
        }]

    @patch(
        'postoffice_django.api.views.ListMessagesView.DEFAULT_MAX_RESULTS', 1)
    def test_only_default_messages_quantity_returned_when_no_limit_received(
            self, client, publishing_error, older_publishing_error):
        response = client.get('/messages/')

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    @patch(
        'postoffice_django.api.views.ListMessagesView.DEFAULT_MAX_RESULTS', 1)
    def test_all_publishing_errors_returned_when_bigger_limit_received(
            self, client, publishing_error, older_publishing_error):
        response = client.get('/messages/?limit=10')

        assert response.status_code == 200
        publishing_errors_count = PublishingError.objects.count()
        assert len(json.loads(response.content)) == publishing_errors_count


@pytest.mark.django_db
class TestDeleteMessageView:

    def test_returns_no_content_when_message_is_deleted(
            self, client, publishing_error):
        response = client.delete(f'/messages/{publishing_error.id}/')

        assert response.status_code == 204
        assert response.content == b''

        assert PublishingError.objects.count() == 0

    def test_only_received_message_is_deleted_when_multiple_messages_exist(
            self, client, publishing_error, older_publishing_error):
        client.delete(f'/messages/{publishing_error.id}/')

        assert PublishingError.objects.count() == 1
        assert PublishingError.objects.first() == older_publishing_error

    def test_returns_not_found_when_id_does_not_exist(
            self, client, publishing_error):
        response = client.delete('/messages/0/')

        assert response.status_code == 404
