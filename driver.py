#!/usr/bin/python
'''
Originally this was used as the main driver for the trading logic.  It's sole
purpose in life was to determine if you should buy or sell.  Currently that
logic has been removed while I  rework the algorithm.
'''

import getMtGoxRequest as req
import dbConnection as db

def main():
    print 'MAIN!!!'
    tmp = driver()
    tmp.logic()

class driver:
    def __init__(self):
        self.info = req.get_res('0/info.php', {})
        self.USD = self.info['Wallets']['USD']['Balance']['value_int']
        self.BTC = self.info['Wallets']['BTC']['Balance']['value_int']
        
    def getPrice(self):
        data = req.get_res('1/BTCUSD/public/ticker', {})
        buyPrice = data['return']['buy']['value_int']
        sellPrice = data['return']['sell']['value_int']
        volume = data['return']['vol']['value_int']

        return (buyPrice, sellPrice, volume)
  
    def logic(self):
        print 'I HAVE LOGIC!'
    
if __name__ == '__main__':
    main()
    

