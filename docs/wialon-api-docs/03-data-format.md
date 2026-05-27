# Data format

This section describes the flags that can be used in various requests. The
result returned in JSON depends on the used flags.

If it is necessary to obtain several flag values in the returned result at the
same time, you need to specify the sum of these flags in the request. For
example, if you need to receive the values of general (DEC value is 1) and
custom properties (DEC value is 2) of a unit group, specify 3 in the request.
