# Base
## Conversion
`Base.convert(num, old_base, new_base)` returns a number converted from any base to any new base.
- num is the number in terms of the old_base's number system
- old_base is the base to convert from (ex. 2 for binary, 8 for octal, 10 for decimal)
- new_base is the base to convert to
```
print(Base.convert(52, 7, 4))
>>> 211
```

## Alternatives
### To Decimal
`Base.to_base_10(num, old_base)` returns a number converted from any base to base-10 (decimal). This is faster, but much less flexible, than `Base.convert()`.
```
print(Base.to_base_10(42, 5))
>>> 22
```

### From Decimal
`Base.from_base_10(decimal, new_base)` returns a number converted from base-10 (decimal) to any new base. This is faster, but much less flexible, than `Base.convert()`.
```
print(Base.from_base_10(42, 8))
>>> 52
```
