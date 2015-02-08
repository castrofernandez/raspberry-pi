#!/bin/sh

import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
	client = MongoClient()
except ConnectionFailure, e:
	print "ERROR"
