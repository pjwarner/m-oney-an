#!/usr/bin/python
'''
This was one of my first attempts at using unit testing in python
Please do not judge me :)
'''

import calcCost as cost
from decimal import Decimal

def test(got, expected):
  if got == expected:
    prefix = ' \033[1;32mOK\033[1;m'
  else:
    prefix = ' \033[1;31mX\033[1;m'
  print '%s \tgot: %s expected: %s' % (prefix, repr(got), repr(expected))

def main():
  print 'Testing costCalculator'
  tmp = cost.calcCost(91 * 617440)
  test(tmp.removeCost(), Decimal('55849917.76'))
  test(tmp.removeCost(), Decimal('55878011.28')) #reduced trading cost

if __name__ == '__main__':
  main()

