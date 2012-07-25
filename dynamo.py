# -*- coding: utf-8 -*-

import boto
from numbers import Number
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError


class Table(object):
    def __init__(self, table=None, eager=False):
        self.table = table
        self.is_eager = eager

    def __repr__(self):
        return '<table \'{0}\'>'.format(self.name)

    @property
    def name(self):
        return self.table.__dict__['_dict']['TableName']

    def item(self, item):
        return Item(item, self)

    def delete(self):
        return self.table.delete()

    def scale(self, read=None, write=None):
        read = read or self.table.read_units
        write = write or self.table.read_units
        return self.table.update_throughput(read_units=read, write_units=write)

    def __getitem__(self, key):
        try:
            if isinstance(key, (basestring, Number)):
                key = [key]
            i = self.table.get_item(*key)
            i = self.item(i)
        except DynamoDBKeyNotFoundError:
            return self.__magic_get(key)
        return i

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, values):
        if isinstance(key, (basestring, Number)):
            key = [key]
        i = self.table.new_item(*key, attrs=values)
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

    def new(self, name):
        table = self.table.layer2.create_table(
            name=name,
            schema=self.table._schema,
            read_units=self.table.read_units,
            write_units=self.table.write_units
        )
        return Table(table=table, eager=self.is_eager)


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


def table(name, auth=None, eager=True):
    """Returns a given table for the given user."""
    auth = auth or []
    dynamodb = boto.connect_dynamodb(*auth)

    table = dynamodb.get_table(name)
    return Table(table=table, eager=eager)


def tables(auth=None, eager=True):
    """Returns a list of tables for the given user."""
    auth = auth or []
    dynamodb = boto.connect_dynamodb(*auth)

    return [table(t, auth, eager=eager) for t in dynamodb.list_tables()]
