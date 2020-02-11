# Post office django client

[![image](https://circleci.com/gh/mercadona/postoffice_django/tree/master.svg?style=svg)](https://circleci.com/gh/mercadona/postoffice_django/tree/master) [![image](https://badge.fury.io/py/postoffice-django.svg)](https://badge.fury.io/py/postoffice-django)

## What is post office django

`postoffice_django` is a django app to communicate with [postoffice](<https://github.com/lonamiaec/postoffice/>).

## Features

- Set up server via django commands:
  - Create necessary `topics` on `postoffice` with `configure_postoffice_publishers` to can publish a message
  - Create necessary `publishers` on `postoffice` with `configure_postoffice_topics` to can consume messages
- Send messages in a easy way to `post office server`

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
    'ORIGIN_HOST': 'example.com',
    'TOPICS': ['topic_to_create', 'another_topic_to_create']
}
```
- `URL`: Is the `url` where the Postoffice server is hosted.

- `CONSUMERS`: Are the consumers which must been configured as publishers in Postoffice server. With that, we create the necessary topics and publishers on Postoffice.

    - `topic`: Topic name to the consumer

    - `target`: Url or pub/sub topic name

    - `type`: http/pubsub

- `TIMEOUT`: Specific timeout to use on every communication with Postoffice. If not specified, the default value is 0.5 seconds.

- `ORIGIN_HOST`: The host from where the topic is created (your host).  It is necessary in order to `postoffice` know where the topic come from.

- `TOPICS`: Topics to create to can send messages to `postoffice`

## How to setup Postoffice via django commands

Now we ready to start sending messages to `postoffice`. But first, we must generate `topics` and/or `publishers` on postoffice depending the purpose of the project with postoffice.

If we need create the topics to can publish, we should execute:

```bash
$ ./manage.py configure_postoffice_topics
```

and, if we need create the publishers, we should execute:

```bash
$ ./manage.py configure_postoffice_publishers
```

## Sending messages to postoffice

We have the `publish` method from the `publishing` module

```python
from postoffice_django.publishing import publish

publish(topic: str, message: dict, **attributes: dict) -> None
```

- `topic`: Topic name. This topic **must** exist on postoffice to manage the message.

- `message`: Message to sent. This **must** be a dict.

- `attributes`: Additional attr. All attributes are cast to string when publish a message
