import math

class Base:
  @staticmethod
  def convert(num, old_base, new_base):
    if(all(int(digit) < old_base for digit in str(num))):
      decimal = Base.base_to_decimal(num, old_base)
      output = Base.decimal_to_base(decimal, new_base)
      return output
  
  @staticmethod
  def base_to_decimal(num, base):
    digits = [int(digit) for digit in str(num)]
    decimal = 0
    for index, digit in enumerate(reversed(digits)):
      weighting_factor = base ** index
      decimal += weighting_factor * digit
    return decimal

  @staticmethod
  def decimal_to_base(decimal, base):
    digits = ""
    quotient = decimal
    while quotient != 0:
      digits = str(quotient % base) + digits
      quotient = math.floor(quotient / base)
    return int(digits)