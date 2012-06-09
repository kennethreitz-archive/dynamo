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


Writing is simple::

    item = table['new-key'] = ['key']

So is reading::

    >>> table['existing-key']['attribute']
    'value'


Installation
------------

(not yet)

Installing dynamo is simple with pip:

::

    $ pip install dynamo
