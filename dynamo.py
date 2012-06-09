# -*- coding: utf-8 -*-

import boto
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError


class Table(object):
    def __init__(self, conn=None, eager=True):
        self.conn = conn
        self.is_eager = eager

    def __repr__(self):
        return '<table \'{0}\'>'.format(self.name)

    @property
    def name(self):
        return self.conn.__dict__['_dict']['TableName']

    def __getitem__(self, key):
        try:
            return self.conn.get_item(key)
        except DynamoDBKeyNotFoundError:
            return self.__magic_get(key)

    def __setitem__(self, key, values):
        i = self.conn.new_item(key, attrs=values)
        i.put()
        return i

    def __delitem__(self, key):
        return self[key].delete()

    def __magic_get(self, key):
        if self.is_eager:
            self[key] = {}
            return self[key]

def table(name, auth, eager=True):

    dynamodb = boto.connect_dynamodb(*auth)
    conn = dynamodb.get_table(name)

    t = Table(conn=conn, eager=eager)

    return t