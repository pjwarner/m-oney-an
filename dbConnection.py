#!/usr/bin/python

'''
This is used for storing data in a mongo database.
'''

import pymongo

conn = pymongo.Connection('localhost', 27017) #server and port
db = conn.bitcoin #database to use

    



