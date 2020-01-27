=========================
Post office django client
=========================

What is post office django
==========================
`postoffice_django` is a django app to communicate with `postoffice` server

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
To can run the application, you must have

- django
- requests

Obviously, you need a properly django project run and up

Installing postoffice_django
----------------------------
To can install our application, you can run:

.. code-block:: bash

   $ pip install git+https://github.com/jjponz/postoffice_django.git

or add

.. code-block:: txt

   git+https://github.com/jjponz/postoffice_django.git

to your requirements file

After install the app, you need set `POST_OFFICE_URL`, `POST_OFFICE_CONSUMERS` and `POST_OFFICE_TIMEOUT` in your django settings file

:POST_OFFICE_URL:
   Is the `url` where server is hosted.

   .. code-block:: python

      POST_OFFICE_URL = 'http://some_site.org/


:POST_OFFICE_CONSUMERS:
    Are the consumers which must been configured as publishers in postoffice server. With that, we create the necessary topics and publishers on postoffice 

    .. code-block:: python

       POST_OFFICE_CONSUMERS = [{
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
           

:POST_OFFICE_TIMEOUT:
   When requests raises a timeout. If you don't set this constant, by default is 0.5


How to setup postoffice via django command
==========================================
Once you installed and set the required variables in django settings, you can create the necessary structure of `topics` and `publishers` on postoffice server using a django command

.. code-block:: bash

   $ ./manage.py configure_post_office


Send messages to postoffice
============================
To send message to postoffice, we have the

.. code-block:: python

   publish(topic, message, **attributes)

method from `publishing` module.

:topic:
   Topic name. This topic **must** exists to postoffice can manage the message

:message:
   Message to sent. This **must** be a dict

:attributes:
   Additional attributes to the message

An example of use:

.. code-block:: python

   from postoffice_django import publishing

   message = {'key': 'value'}
   publishing.publish('some_topic', message)

or if we need send message attributes

.. code-block:: python

   from postoffice_django import publishing

   message = {'key': 'value'}
   publishing.publish('some_topic', message, some_attribute=1, name='example')


The method sends the message to postoffice using this payload:

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


In case that we can't send the message to the server, we has an admin view to see the errors. The information stored is:

:Topic:
  The addresses topic for the message sent
:Payload:
  The message that we sent
:Attributes:
  Attributes of the message sent
:Errors:
  Errors that postoffice reports 
