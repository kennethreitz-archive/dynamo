# -*- coding: utf-8 -*-

import boto
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError


class Table(object):
    def __init__(self, conn=None):
        self.conn = conn

    def __repr__(self):
        return '<table \'{0}\'>'.format(self.name)

    @property
    def name(self):
        return self.conn.__dict__['_dict']['TableName']

    def __getitem__(self, key):
        try:
            return self.conn.get_item(key)
        except DynamoDBKeyNotFoundError:
            pass

    def __setitem__(self, key, values):
        i = self.conn.new_item(key, attrs=values)
        i.put()
        return i

    def __delitem__(self, key):
        return self[key].delete()


def table(name, auth):

    dynamodb = boto.connect_dynamodb(*auth)
    conn = dynamodb.get_table(name)

    t = Table(conn=conn)

    return t