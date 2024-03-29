# Post office django client

[![image](https://circleci.com/gh/mercadona/postoffice_django/tree/master.svg?style=svg)](https://circleci.com/gh/mercadona/postoffice_django/tree/master) [![image](https://badge.fury.io/py/postoffice-django.svg)](https://badge.fury.io/py/postoffice-django)

## What is postoffice django

`postoffice_django` is a django app to communicate with [postoffice](<https://github.com/lonamiaec/postoffice/>).

## Features

- Set up server via django commands:
  - Create necessary `topics` in `postoffice` with `configure_postoffice_publishers` to be able to publish a message
  - Create necessary `publishers` in `postoffice` with `configure_postoffice_topics` to be able to consume messages
- Easily send messages to `postoffice server`

## How to install it

### Prerequisites

To be able to run the application, you must have

  - django
  - requests

Obviously, you need a django project up and running

### Installing postoffice_django

At the moment there are two ways to install the app:

```bash
$ pip install postoffice-django
```

or add

```txt
postoffice-django
```

to your requirements file

Add it to your Django installed apps:


```python
INSTALLED_APPS = [
    ...
    'postoffice_django'
]
```

Then, you need to set the required settings for your app:

```python
POSTOFFICE = {
    'URL': 'http://fake.service',
    'CONSUMERS': [{
            'topic': 'some_topic',
            'target': 'http://www.some_url.com',
            'type': 'http',
            'from_now': True
        },
        {
            'topic': 'another_topic',
            'target': 'http://www.another_url.com',
            'type': 'pubsub',
            'from_now': False
        }],
    'TIMEOUT': 0.3,
    'BULK_TIMEOUT': 5,
    'ORIGIN_HOST': 'example.com',
    'TOPICS': ['topic_to_create', 'another_topic_to_create'],
    'RECOVERY_ENABLED': True
}
```
- `URL`: Is the `url` where the Postoffice server is hosted.

- `CONSUMERS`: Are the consumers which must been configured as publishers in Postoffice server. With that, we create the necessary topics and publishers on Postoffice.

    - `topic`: Topic name to the consumer

    - `target`: Url or pub/sub topic name

    - `type`: http/pubsub
    
    - `timeout`: Seconds Postoffice should wait before cancelling the request. [Optional] 
    
- `TIMEOUT`: Specific timeout to use in every communication with Postoffice. If not specified, the default value is 0.5 seconds.

- `BULK_TIMEOUT`: Specific timeout to use when sending bulk messages to Postoffice. If not specified, the default value is 5 seconds.

- `ORIGIN_HOST`: The host from where the topic is created (your host).  It is necessary in order to `postoffice` know where the topic come from.

- `TOPICS`: Topics to be created in order to send messages to `postoffice`

- `RECOVERY_ENABLED`: Enables the recovery of failed messages on all new topics. If not specified, the default value is false.

Finally add `postoffice` path in your django urls file:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('service.health.urls')),
    path('postoffice/', include('postoffice_django.urls'))
]
```

## How to setup Postoffice via django commands

Now we are ready to start sending messages to `postoffice`. But first, we must generate `topics` and/or `publishers` in postoffice depending on the purpose of the project with postoffice.

If we need to create the topics to be able to publish, we should execute:

```bash
$ ./manage.py configure_postoffice_topics
```

and, if we need to create the publishers, we should execute:

```bash
$ ./manage.py configure_postoffice_publishers
```

## Sending messages to postoffice

We have three publishers in the `publishing` module

#### Publishing a single message

```python
from postoffice_django.publishing import publish

publish(topic: str, message: dict, **attributes: dict) -> None
```

- `topic`: Topic name. This topic **must** exist on postoffice to manage the message.

- `payload`: Message to be sent. This **must** be a dict.

- `attributes`: Additional attr. All attributes are cast to string when publishing a message.


##### Scheduling messages to be published in the future
In cases where you want to publish a message to PostOffice now, but would like to receive it in the future, you can schedule the message 
```python
from postoffice_django.publishing import scheduled_publish

scheduled_publish(topic: str, message: dict, schedule_in: int, **attributes: dict) -> None
```

The only difference with the `publish` method, is that it receives a new param:

- `schedule_in`: The amount of **minutes** in the future when you want to receive the message.

_Disclaimer: If the message cannot be published to PostOffice and is inserted as a PublishingError, it will not be scheduled as of right now. Please take this into consideration._

#### Publishing messages in batches

In case we want to send multiple messages to the same topic, the best way is sending them in batches.

```python
from postoffice_django.publishing import bulk_publish

def bulk_publish(topic: str, payload: list, **attrs: dict) -> None:
```

- `topic`: Topic name. This topic **must** exist on postoffice to manage the message.

- `payload`: Message's payloads to be sent. This **must** be a list.

- `attributes`: Additional attr. All attributes are cast to string when publishing a message.

An example:

```python
bulk_publish('test-topic', [{'message1': 'key1'}, {'message2': 'key2'}], {'additional_key': 1})
```

This will be handled on Postoffices and we'll actually receive two messages for the same topic
* `test_topic`, `{'message1': 'key1'}`, `{'additional_key', 1}}`
* `test_topic`, `{'message2': 'key2'}`, `{'additional_key', 1}}`


## How to contribute

### Implement

1. `make install-test-requirements`
1. `make env-start`
1. Write a test.
1. `make test`
1. Implement up to the test are green.
1. Repeat.

### Deploy

1. `make deploy VERSION=1.0.0`