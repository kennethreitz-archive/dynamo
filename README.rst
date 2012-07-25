Dynamo: Simple DynamoDB API
===========================

This module allows you to interact with DynamoDB much like a native Python dictionary.


Usage
-----

::

    import dynamo

    ACCESS_KEY = 'XXXXXX'
    SECRET_ACCESS_KEY = 'XXXXXX/XXXXXXXXX+XXXXXXX'
    TABLE_NAME = 'XXXXX'

    table = dynamo.table(TABLE_NAME, (ACCESS_KEY, SECRET_ACCESS_KEY))

    # Or, if you have AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY defined as
    # environment variables, you can do:
    table = dynamo.table(TABLE_NAME)

Writing is simple::

    table['new-key']['attribute'] = ['value']

So is reading::

    >>> table['existing-key']['attribute']
    'value'


Installation
------------

Installing dynamo is simple with pip:

::

    $ pip install dynamo
