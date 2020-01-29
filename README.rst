=========================
Post office django client
=========================

What is post office django
==========================
`postoffice_django` is a django app to communicate with [postoffice](https://github.com/lonamiaec/postoffice/).

Features
========
- Set up server via django command `configure_post_office`
    - Create necessary `topics` on `postoffice` server
    - Create necessary `publishers` on `postoffice server`
- Send messages in a easy way to `post office server`

How to install it
=================

Prerequisites
-------------
To be able to run the application, you must have

- django
- requests

Obviously, you need a django project up and running

Installing postoffice_django
----------------------------
At the moment there are two ways to install the app:

.. code-block:: bash

   $ pip install git+https://github.com/mercadona/postoffice_django.git

or add

.. code-block:: txt

   git+https://github.com/mercadona/postoffice_django.git

to your requirements file

Once installed, you need to set `POSTOFFICE_URL`, `POSTOFFICE_CONSUMERS` and `POSTOFFICE_TIMEOUT` in your django settings file.

:POSTOFFICE_URL:
   Is the `url` where server is hosted.

   .. code-block:: python

      POSTOFFICE_URL = 'http://some_site.org/


:POSTOFFICE_CONSUMERS:
    Are the consumers which must been configured as publishers in postoffice server. With that, we create the necessary topics and publishers on postoffice

    .. code-block:: python

       POSTOFFICE_CONSUMERS = [{
           'topic': 'some_topic',
           'endpoint': 'http://www.some_url.com',
           'type': 'http',
           },
           {
           'topic': 'another_topic',
           'endpoint': 'http://www.another_url.com',
           'type': 'pubsub',
           }]

    :topic:
       Topic name to be created

    :endpoint:
       Url or pub/sub topic name

    :type:
       http/pubsub


:POSTOFFICE_TIMEOUT:
   Specific timeout to use on every communication with `postoffice`. If not specified the default value is 0.5 seconds.


How to setup postoffice via django command
==========================================
Now we ready to start sending messages to `postoffice`. But first, we must generate `topics` and `publishers` on postoffice. There is a django command to help on this

.. code-block:: bash

   $ ./manage.py configure_post_office


Sending messages to postoffice
============================
We have the `publish` method from the `publishing` module

.. code-block:: python

   publish(topic, message, **attributes)

:topic:
   Topic name. This topic **must** exists to postoffice can manage the message

:message:
   Message to sent. This **must** be a dict

:attributes:
   Additional attributes to the message

An example:

.. code-block:: python

   from postoffice_django import publishing

   message = {'key': 'value'}
   publishing.publish('some_topic', message)

we can also send extra attributes (those attributes will be headers on http requests or extra information on gcloud pubsub)

.. code-block:: python

   from postoffice_django import publishing

   message = {'key': 'value'}
   publishing.publish('some_topic', message, some_attribute=1, name='example')


The generated payload sent to postoffice looks like follows:

:without attributes:

    .. code-block:: python

        {
          "topic": "topic_name",
          "message": {
            "key": "value"
          },
        }

:with attributes:

   .. code-block:: python

        {
          "topic": "topic_name",
          "message": {
            "key": "value"
          },
        "attributes": {
          "some_attribute": 1,
          "name": "example"
          }
        }

In case communication with postoffice fails, we save those undelivered messages locally with all the related information


:Topic:
  The addresses topic for the message sent
:Payload:
  The message that we sent
:Attributes:
  Attributes of the message sent
:Errors:
  Errors that postoffice reports
