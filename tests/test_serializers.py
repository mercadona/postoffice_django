import pytest

from postoffice_django.serializers import MessagesSerializer


@pytest.mark.django_db
class TestMessagesSerializer:

    def test_returns_message_when_valid_publishing_error_received(
            self, publishing_error):
        assert MessagesSerializer().serialize([publishing_error]) == [{
            'id': publishing_error.id,
            'topic': 'test',
            'payload': {'key': 'value', 'num': '2.15', 'elements': [1, 2, 3]},
            'attributes': {'key': 'value'},
            'bulk': False,
        }]

    def test_returns_message_when_bulk_publishing_error_received(
            self, bulk_publishing_error):
        assert MessagesSerializer().serialize([bulk_publishing_error]) == [{
            'id': bulk_publishing_error.id,
            'topic': 'test-topic',
            'payload': [
                {'topic': 'test-topic', 'payload': {'approved': True}},
                {'topic': 'test-topic', 'payload': {'approved': False}},
            ],
            'attributes': None,
            'bulk': True,
        }]
