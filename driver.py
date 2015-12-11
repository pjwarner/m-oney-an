#!/usr/bin/env python
'''
Originally this was used as the main driver for the trading logic.  It's sole
purpose in life was to determine if you should buy or sell.  Currently that
logic has been removed while I  rework the algorithm.
'''

import getMtGoxRequest as req
import time
import dbConnection as db
from decimal import Decimal
from blessings import Terminal # for colors

def main():
    t = Terminal() # for colors
    memory = {}
    tmp = driver()
    data = tmp.getPrice()

    memory['my_usd'] = data['my_usd']
    memory['my_btc'] = data['my_btc']

    while True:
        if memory['my_usd'] == data['my_usd'] and memory['my_btc'] == data['my_btc']:
            print '{t.green}No Change{t.normal}:'.format(t=t),' My USD:', t.green(str(data['my_usd'])), ' My BTC:', t.green(str(data['my_btc']))
            pass
        else:
            if memory['my_usd'] > data['my_usd']:
                print t.green('Made Sale!')
                db.db.transhistory.insert({'previous':str(memory['my_usd']),
                                           'current':str(data['my_usd']),
                                           'action':'Sell'
                                           })
                                        
            else:
                print t.blue('Made Buy!')
                db.db.transhistory.insert({'previous':str(memory['my_usd']),
                                           'current':str(data['my_usd']),
                                           'action':'Buy'
                                           })
            
            memory['my_usd'] = data['my_usd']
            memory['my_btc'] = data['my_btc']

        print t.bold_blue('Current Price:'), t.bold_blue(str(data['buy']))
        time.sleep(10)

        try:
            data = tmp.getPrice()
        except:
            time.sleep(30)
            try:
                data = tmp.getPrice()
            except:
                pass
                
            
class driver:
    def __init__(self):
        self.info = req.get_res('0/info.php', {})
        self.USD = self.info['Wallets']['USD']['Balance']['value_int']
        self.BTC = self.info['Wallets']['BTC']['Balance']['value_int']
        pass
        
    def getPrice(self):
        data = req.get_res('1/BTCUSD/public/ticker', {})
        buyPrice = data['return']['buy']['value_int']
        sellPrice = data['return']['sell']['value_int']
        volume = data['return']['vol']['value_int']
        price = {
            'buy':Decimal(int(buyPrice) * .00001).quantize(Decimal('1.00000')),
            'sell':Decimal(int(sellPrice) * .00001).quantize(Decimal('1.00000')),
            'volume':Decimal(int(volume) * .00000001).quantize(Decimal('1.00000')),
            'my_btc':Decimal(int(self.BTC) * .00000001).quantize(Decimal('1.00000000')),
            'my_usd':Decimal(int(self.USD) * .00001).quantize(Decimal('1.00000'))
            }

        db.db.priceindex.insert({'buy':str(price['buy']),
                                 'sell':str(price['sell']),
                                 'volume':str(price['volume']),
                                 'exchange':'mtgox',
                                 'holdings':
                                     {'btc':str(price['my_btc']),
                                      'usd':str(price['my_usd'])
                                      }
                                 })
        return price
  
    def logic(self):
        last = db.db.transhistory.find().sort(-1).limit(1)
        if last['action'] == 'Buy':
            print 'Do selling logic'
        elif last['action'] == 'Sell':
            print 'Do buying logic'
        else:
            print t.red('No Transactions exist')

    def logic_buy(self, sell_price):
        cur = self.getPrice()
        if cur['buy'] < (sell_price - (sell_price * .1)):
            '''
            When the price drops 10% spend 10% of your cash
            '''
            print 'Buy with 10% of available cash'
        elif cur['buy'] < (sell_price - (sell_price * .2)):
            '''
            If sell price was 100 and we have gone down 20% from sell (80) buy
            2x the first buy of 10% or ($10) in this case.  So we are buying $20
            worth of bitcoin in this round on this algo if you started with $100
            you are now 22% of available cash in ($22 of $80)
            '''
            print 'Double down from original sell price'
        elif cur['buy'] < (sell_price - (sell_price * .3)):
            '''
            If the price drops 30% we are doubling down on the last buy. In this case
            we are going to buy $40 worth of btc. This is similar to betting in blackjack
            at this point we are 85% of available cash ($40 of $70)
            '''
            print 'Double down again'
        elif cur['buy'] > (sell_price * 1.05): #increase of 5% of 
            print 'Sell the house'
                                         
    def logic_sell(self, buy_prices):
        pass
    
if __name__ == '__main__':
    main()
    

