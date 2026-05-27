# Example of obtaining the “tz” parameter

You can obtain the tz parameter using bitwise operations such as
mathematical AND (&) and mathematical OR (|).

## Example of obtaining “tz”

Below are the instructions to obtain the tz parameter for the Azores time
zone (-01:00) with no DST (0x08000000).

1. Apply a mathematical AND operation to the Azores time zone (-3600)
using the 0xf000ffff mask.

Convert the decimal signed value to binary using the two’s
complement method.

Perform the operation:

-3600 & 0xf000ffff
-268373520

2. Apply a mathematical OR operation to the result using the mask
corresponding to DST(0x08000000).

-268373520 | 0x8000000
-134155792

Thus, the final value for tz is -134155792.

## Reverse operation

To retrieve the original time zone (tz) value from tz = -134155792, follow
these steps:

1. Apply a mathematical AND operation to the tz parameter using the
0xffff mask:

-134155792 & 0xffff
61936

2. If the original tz value is negative (which it is in this case), apply a
mathematical OR operation to the result using the 0xffff0000 mask.

61936 | 0xffff0000
-3600

This confirms that the original time zone value is -3600 (UTC -01:00,
Azores).

## Additional information

The tz value -134155792 in hexadecimal is 0xf800f1f0.
Applying the 0x0fff0000 mask isolates the DST component.

A DST value of 0x08000000 indicates no DST adjustment.

Thus, the decoded time zone is UTC -01:00 (Azores) with no DST.
