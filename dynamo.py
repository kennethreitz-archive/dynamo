# -*- coding: utf-8 -*-

import boto
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError


class Table(object):
    def __init__(self, conn=None, eager=False):
        self.conn = conn
        self.is_eager = eager

    def __repr__(self):
        return '<table \'{0}\'>'.format(self.name)

    @property
    def name(self):
        return self.conn.__dict__['_dict']['TableName']

    def item(self, item):
        return Item(item, self)

    def __getitem__(self, key):
        try:
            i = self.conn.get_item(key)
            i = self.item(i)
        except DynamoDBKeyNotFoundError:
            return self.__magic_get(key)
            # i = self.item(i)

        return i

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, values):
        i = self.conn.new_item(key, attrs=values)
        i = self.item(i)
        i.put()
        return i

    def __delitem__(self, key):
        return self[key].delete()

    def __magic_get(self, key):
        if self.is_eager:
            self[key] = {}
            return self.item(self[key])

    def __contains__(self, key):
        return not self.get(key) is None


class Item(object):
    def __init__(self, item, table):
        self.item = item
        self.table = table

    @property
    def is_eager(self):
        return self.table.is_eager

    def __getattr__(self, key):
        if not key in ['item']:
            try:
                return getattr(object, key)
            except AttributeError:
                return getattr(self.item, key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        return repr(self.item)

    def __getitem__(self, key):
        return self.item[key]

    def __setitem__(self, key, value):
        self.item[key] = value

        if self.is_eager:
            self.item.save()

    def __contains__(self, key):
        return key in self.item



def table(name, auth, eager=True):

    dynamodb = boto.connect_dynamodb(*auth)
    conn = dynamodb.get_table(name)

    t = Table(conn=conn, eager=eager)

    return t