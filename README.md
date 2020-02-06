# Post office django client

[![image](https://circleci.com/gh/mercadona/postoffice_django/tree/master.svg?style=svg)](https://circleci.com/gh/mercadona/postoffice_django/tree/master) [![image](https://badge.fury.io/py/postoffice-django.svg)](https://badge.fury.io/py/postoffice-django)

## What is post office django

`postoffice_django` is a django app to communicate with [postoffice](<https://github.com/lonamiaec/postoffice/>).

## Features

- Set up server via django command `configure_post_office`
  - Create necessary `topics` on `postoffice` server
  - Create necessary `publishers` on `postoffice`
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

Then, you need to set `POSTOFFICE_URL`, `POSTOFFICE_CONSUMERS`, `POSTOFFICE_TIMEOUT` and `ORIGIN_HOST` in your django settings file.

- `POSTOFFICE_URL`: Is the `url` where server is hosted.


```python
POSTOFFICE_URL = 'http://some_site.org/'
```

- `POSTOFFICE_CONSUMERS`: Are the consumers which must been configured as publishers in postoffice server. With that, we create the necessary topics and publishers on postoffice.


```python
POSTOFFICE_CONSUMERS = [{
    'topic': 'some_topic',
    'target': 'http://www.some_url.com',
    'type': 'http',
    },
    {
    'topic': 'another_topic',
    'target': 'a-topic-name',
    'type': 'pubsub',
    }]
```

- `topic`: Topic name to be created

- `target`: Url or pub/sub topic name

- `type`: http/pubsub

- `POSTOFFICE_TIMEOUT`: Specific timeout to use on every communication with `postoffice`. If not specified the default value is 0.5 seconds.

```python
POSTOFFICE_TIMEOUT = 1
```

- `ORIGIN_HOST`: The host from where the topic is created (your host).  It is necessary in order to `postoffice` know where the topic come from.

```python
ORIGIN_HOST = 'myserver.mydomain'
```

## How to setup postoffice via django command

Now we ready to start sending messages to
`postoffice`. But first, we must generate
`topics` and
`publishers` on postoffice. There is a
django command to help on this


```bash
$ ./manage.py configure_post_office
```


## Sending messages to postoffice

We have the
`publish` method from the
`publishing` module

```python
publish(topic, message, **attributes)
```

- `topic`: Topic name. This topic **must** exists to postoffice can manage the message.

- `message`: Message to sent. This **must** be a dict.

- `attributes`: Additional attr.
