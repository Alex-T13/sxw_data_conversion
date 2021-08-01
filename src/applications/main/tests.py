from django.test import TestCase
# import decimal as dc
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_HALF_DOWN
# decimal.getcontext().prec = 5

# x = dc.Decimal('1.00000')
#
# print(type(x))
# print(x)
# y = int(str(x).split('.')[1])
# print(y)

# if x.is_integer():
# if x.is:
#     quantity = str(x).split('.')[0]
# else:
#     quantity = str(x).split('.')[1]
#
# print(quantity)
# x = Decimal(Decimal('0.02') + Decimal('0.02')).quantize(Decimal('1.11'), rounding=ROUND_HALF_UP)
# y = Decimal('1.515').quantize(Decimal('1.00'), ROUND_HALF_DOWN)
# print(x)
# print(y)

# while True:
#     quantity = str(input("число:"))
#     x = Decimal('{:f}'.format(Decimal(quantity).normalize()))
#     # y = Decimal('{:f}'.format(x))
#     # x.normalize()
a = 'GGGGG'
b = 'HGHGHGHGKKL'
c = a / b

print(type(c))
print(c)
