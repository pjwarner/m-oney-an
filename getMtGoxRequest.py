#!/usr/bin/python

'''
This is the meat and potatoes of the program.  This is the part of the program
where you can initiate all the transactions that you would from the site.

Buy, Sell, Withdraw etc.  The general use of this is to do get_res(page, args)

An example of this is found in trade.py

In the initial upload of this code it is commented out
'''

import json
from urllib import urlencode
import urllib2
import time
from hashlib import sha512
from hmac import HMAC
import base64

def get_nonce():
    return int(time.time()*100000)

def sign_data(secret, data):
    return base64.b64encode(str(HMAC(secret, data, sha512).digest()))

class request:
    def __init__(self, auth_key, auth_secret):
        self.auth_key = auth_key
        self.auth_secret = base64.b64decode(auth_secret)
        
    def build_query(self, req={}):
        req["nonce"] = get_nonce()
        post_data = urlencode(req)
        headers = {}
        headers["User-Agent"] = "GoxApi"
        headers["Rest-Key"] = self.auth_key
        headers["Rest-Sign"] = sign_data(self.auth_secret, post_data)
        return (post_data, headers)
    
    def perform(self, path, args):
        data, headers = self.build_query(args)
        req = urllib2.Request("https://mtgox.com/api/"+path, data, headers)
        res = urllib2.urlopen(req, data)
        return json.load(res)
        
def get_res(page, args):
    result = request(
        '<Your-API-Key-Here>',
        '<Your-Secret-Here>'
        )
    data = result.perform(page, args)
    return data
