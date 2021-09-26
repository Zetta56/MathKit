import math

class Base:
  @staticmethod
  def convert(num, old_base, new_base):
    """
    Converts the number from its old base to base-10 and then to a new
    base using both weighted multiplication and successive division. This
    uses base-10 as an intermediary number system because that's how we
    normally represent numbers (digits ranging from 0 to 9).
    """
    # Check if all digits in num are valid (less than the old base)
    if(all(int(digit) < old_base for digit in str(num))):
      decimal = Base.to_base_10(num, old_base)
      output = Base.from_base_10(decimal, new_base)
      return output
  
  @staticmethod
  def to_base_10(num, old_base):
    """
    Returns the base-10 (decimal) equivalent of an input number using weighted
    multiplication. This is useful when you want to convert from a
    non-base-10 number system (ex. binary, hexadecimal) to base-10.
    """
    # Split num into a list of its digits
    digits = [int(digit) for digit in str(num)]
    # Decimal will be used as an output sum in base-10
    decimal = 0
    # Get each digit and its index in reverse order, since weighted
    # multiplication goes from right to left
    for index, digit in enumerate(reversed(digits)):
      # Find each digit's weighting factor by raising its base by its
      # position from the right (ex. 2 in octal 265 has a factor of 8^2, or 64)
      weighting_factor = old_base ** index
      # Adds the product between the digit and its weighting factor to sum
      # Ex. The 2 in 265 is two 64s, which is 128 in base-10
      decimal += weighting_factor * digit
    return decimal

  @staticmethod
  def from_base_10(decimal, new_base):
    """
    Returns the result of converting a base-10 (decimal) number to a specified
    number system using successive division. This is useful for converting
    from base-10 to non-base-10.
    """
    # Digits will be used to construct the output number
    digits = ""
    # Continue dividing until quotient goes from its full amount (the
    # input decimal) to 0
    quotient = decimal
    while quotient != 0:
      # Add the remainder to the left of any existing digits (basically
      # concatenating in reverse)
      digits = str(quotient % new_base) + digits
      # Update the quotient, rounded down
      quotient = math.floor(quotient / new_base)
    # Convert from string to integer
    return int(digits)