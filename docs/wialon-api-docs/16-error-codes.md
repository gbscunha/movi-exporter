# Error codes

The server may return JSON with the following errors:

```json
{"error":<code>}
```

Error
Description                         Alternatives
code

Internal error (network
-100
timeout).

Internal error (wrong
-101
network response).

Successful operation (for
0       example, for logging out it
will be a successful exit).

1       Invalid session.

No messages for the
2       Invalid API service name.
selected interval.

Type library plugin not
enabled.
3       Invalid result.
AVL Server item not found.
File not found.

Invalid session.
Item not found.
4       Invalid input.
Unknown error.
Internal error.

5       Error performing request.

6       Unknown error.                      The authorization server is
unavailable, please try again
later.
Internal error.
Failed to parse the remote
response.

Error
Description                         Alternatives
code

Invalid session
(agro/convert_plots).

The user is disabled.
Invalid username or
password.
7       Access denied.                      Error checking the cluster of
the current user.
Internal server error.
Unknown error.

Invalid username or
8
password.

Authorization server
9
unavailable.

Limit of simultaneous
Reached the limit of
10                                          recalculations (5
concurrent requests.
recalculations) reached.

11      Password reset error.

Agro subsystem not
12
loaded.

14      Billing error.

No messages for the
1001
selected interval.

1002    Indicates either of the two
errors:

Error
Description                        Alternatives
code

An item with this unique
property already exists.
The item can’t be
created according to the
billing restrictions.

Locker service unavailable.
Limit exсeeded.
Limit of concurrent events
reached.
Failed to create a new
Only one request is
1003                                       session.
allowed at the moment.
Accept-encoding is not gzip.
Limit of message layers
reached.
LAYERS_MAX_COUNT(50)
exceeded.

The limit of messages has          The file size exceeds the
1004
been exceeded.                     maximum size of 1 GB.

The execution time has             Wrong hardware
1005
exceeded the limit.                configuration.

Exceeded the limit of
1006    attempts to enter a two-
factor authorization code.

Your IP has changed, or the
1011
session has expired.

Wrong item or
2001
target_resource.

Error
Description                          Alternatives
code

The target_resource is not
2002
an account.

2003    Wrong target plugin.

The target account is
2004
blocked.

Invalid creator of the
2005
target_resource.

No access to the item for
2006
the target_creator.

2007    Wrong source resource.

The item is already in the
2008
target_resource.

The target_resource is
2009    owned by a different top
user.

There is not enough item
2010    resource counter in the
target_resource.

2011    Wrong item plugin.

Error changing the billing
2012    account item to
target_resource.

Error
Description                        Alternatives
code

Error changing the item
2013
creator.

The selected user is the
creator of some system
2014      objects, therefore, this user
can’t be assigned to a new
account.

Deleting the sensor is
forbidden because it is
2015
used in another sensor or
advanced unit properties.
