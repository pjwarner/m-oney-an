import dbConnection as data
import calcCost as cost
from decimal import *
import getMtGoxRequest as req

class trade:
  def __init__(self):
    print 'Initialized...'
    self.info = req.get_res('0/info.php', {})
    self.priceInfo = req.get_res('1/BTCUSD/public/ticker', {})

  def buy(self):
    """
    Current implementation of this method buys ALL the bitcoins you can at market price
    TODO: Add a way to tell it how many you want to buy for hedging purposes
    """
    print 'Initiating a buy...'
    cashpool =  int(self.info['Wallets']['USD']['Balance']['value_int'])
    sellPrice = int(self.priceInfo['return']['sell']['value_int'])

    btcpool = Decimal(cashpool / sellPrice).quantize(Decimal('1.0'), rounding=ROUND_DOWN)
    print 'Buying:', btcpool, 'btc'

    #Actual Trade Code
#    trade = {'amount': 10, 'Currency':'USD'}
#    tmp = req.get_res('0/buyBTC.php', trade)
#    print tmp

    
    
    print 'Removing MtGoxCost...'
    tmp = cost.calcCost(int(btcpool))
    actual = tmp.removeCost()
    print 'ActualInPool:', actual

    return actual

  def sell(self):
    """
    Current implementation of this method sells ALL your bitcoins at the market price.
    """
    print 'Initiating a sell...'
    btcpool =  int(self.info['Wallets']['BTC']['Balance']['value_int'])
    sellPrice = int(self.priceInfo['return']['buy']['value_int'])

    print 'Selling:', btcpool, 'btc'

    print 'Removing MtGoxCost...'
    tmp = cost.calcCost(btcpool * sellPrice)
    actual = tmp.removeCost() * Decimal('.00001')
    print 'ActualInPool:', actual

    return actual


