import pytest
from freezegun import freeze_time

from postoffice_django.models import PublishingError


@pytest.fixture
@freeze_time('2020-02-13')
def publishing_error():
    return PublishingError.objects.create(
        topic='test',
        payload={'key': 'value', 'elements': [1, 2, 3], 'num': '2.15'},
        attributes={'key': 'value'},
        error='Error message',
    )


@pytest.fixture
@freeze_time('2020-01-28')
def older_publishing_error():
    return PublishingError.objects.create(
        topic='test-topic',
        payload={'approved': True},
        error='Connection error',
    )


@pytest.fixture
@freeze_time('2020-01-28')
def bulk_publishing_error():
    return PublishingError.objects.create(
        topic='test-topic',
        payload=[
            {'topic': 'test-topic', 'payload': {'approved': True}},
            {'topic': 'test-topic', 'payload': {'approved': False}},
        ],
        error='Connection error',
        bulk=True,
    )
