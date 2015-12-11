'''
Use: The purpose of this module is to identify how much the trade is going to
cost.  Primary purpose is to decide if the current price change is worth your
trade.  For instance if you are doing trades of bitcoin that are relatively
small in size and the swing in the price of the bitcoins has not gone high
enough to make you money then you should wait.  For the most part this is not
really a required module, but could be helpful in various trading algorithms
'''


import getMtGoxRequest as req
from decimal import *

class calcCost:
  def __init__ (self, amount):
    info = req.get_res('0/info.php', {})
    self.tradefee = info['Trade_Fee'] * .01
    self.tmp = amount

  def removeCost(self):
    result = Decimal(str(self.tmp - (self.tmp * self.tradefee)))
    return result

