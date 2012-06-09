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

    db = dynamo.table(TABLE_NAME, (ACCESS_KEY, SECRET_ACCESS_KEY))

    item = db['key']
    item['key'] = 'value'
    item.save()