#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""
import logging

from samantha import config
from pymongo import MongoClient
from bson.objectid import ObjectId


__all__ = ['MongoRepository', 'MongoDBConnection']

logger = logging.getLogger(__name__)


class MongoDBConnection(object):
    """
    MongoDB Connection
    """
    def __init__(self, host, port, user, password, auth_db):
        self.host = host
        self.port = port
        self.username = user
        self.password = password
        self.auth_database = auth_db
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(host=self.host, port=self.port,
            username=self.username, password=self.password,
            authSource=self.auth_database)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class MongoRepository(object):
    """
    MongoDB Client Module
    """

    def __init__(self):
        super(MongoRepository, self).__init__()
        opts = config.get_mongo_config()
        self.client = MongoDBConnection(
            host=opts.host, port=opts.port,
            user=opts.username, password=opts.password,
            auth_db=opts.auth_database
        )

    def insert_record(self, record, db='samantha', collection='ansible_run'):
        """
        Insert single record
        """
        with self.client as client:
            db = client.connection[db]
            collection = db[collection]
            doc_id = collection.insert_one(record).inserted_id
            logger.info("Successfully entered record with id %s" % (str(doc_id)))
        return doc_id

    def get_record(self, doc_id, db='samantha', collection='ansible_run'):
        """
        Fetch the record by document id
        """
        with self.client as client:
            document = client.connection[db][collection].find_one(
                {'_id': ObjectId(doc_id)}
            )
        return document
