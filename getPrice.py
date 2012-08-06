#!/usr/bin/python
'''
This is used to download the mtgox price data every 10 seconds. This implementation
will save the data to a mongodb instance.  The mongodb instance information is stored
in dbConnection.  The connection used in this iteration does not use a user:pass
combo and is pretty insecure as is
'''

import getMtGoxRequest as req
import dbConnection as data
import time

##Testing getting the data from mtgox
x = 1
err = 0
while x > 0:
  try:
    info = req.get_res('1/BTCUSD/public/ticker', {})
    data.db.tradedata.save({'buy':info['return']['buy']['value_int'], 'sell':info['return']['sell']['value_int'], 'volume':info['return']['vol']['value_int']})
    print 'Added!', 'Sleeping...', 'Count at:', '\033[1;32m' + str(x) + '\033[1;m', 'Errors:', '\033[1;31m' + str(err) + '\033[1;m'
    time.sleep(10)
    x+=1
  except:
    time.sleep(10)
    err += 1

