# Tokens

This page describes token flags and the ACL flags (bits) to which they
correspond.

Each token has a combined flag (fl) that limits which access rights the
token can use. A token flag combines several individual access right bits
into a single category (for example, online tracking or data editing). A token
can’t exceed the user’s access rights.

In API requests the token flag (fl) is usually specified as a
decimal number. In the tables below ACL bits are shown in
both HEX and DEC for convenience.

Token flag         Token flag
Description
(HEX)              (DEC)

0x100              256                   Online tracking

0x200              512                   Viewing data

0x400              1024                  Editing non-sensitive data

0x800              2048                  Editing sensitive data

Editing critical data and deleting
0x1000             4096
messages

0x2000             8192                  Sending commands

-1                 -1                    Unlimited access

To grant multiple access levels to a token, sum the token flag values. For
example, to grant both online tracking (256) and viewing data (512) access,
use fl = 768.

To grant unrestricted access, use fl = -1.

## Online tracking

The token flag 0x100 (256) grants access rights related to online tracking.

Applies       Access right
ACL bit (HEX)         ACL bit (DEC)
to            name

View object
Any
and its basic      0x1                   1
object
properties

View detailed
Any
object             0x2                   2
object
properties

Any           View custom
0x20                  32
object        fields

Request
Any
reports and        0x200                 512
object
messages

View and
Any
download           0x4000                16384
object
files

Unit, unit    View
0x400000000           17179869184
group         commands

Resource
View POIs          0x400000              4194304
(Account)

Resource      View
0x1000000             16777216
(Account)     geofences

Applies       Access right
ACL bit (HEX)          ACL bit (DEC)
to            name

Resource      View report
0x10000000             268435456
(Account)     templates

View drivers
Resource
and driver        0x40000000             1073741824
(Account)
groups

Resource
View orders       0x200000000            8589934592
(Account)

Resource      View tags
0x800000000            34359738368
(Account)     (passengers)

View trailers
Resource
and trailer       0x100000000000         17592186044416
(Account)
groups

## Viewing data

The token flag 0x200 (512) grants access rights related to viewing data.

Applies                                      ACL bit         ACL bit
Access right name
to                                           (HEX)           (DEC)

Unit, unit   View service intervals
0x10000000      268435456
group        (maintenance)

View connectivity settings
Unit, unit
(HW/UID/phone/password,         0x4000000       67108864
group
and so on)

Applies                                           ACL bit          ACL bit
Access right name
to                                                (HEX)            (DEC)

Act on behalf of this user
User          (create objects, log in,            0x200000         2097152
and so on)

Resource
View notifications                  0x100000         1048576
(Account)

Resource
View jobs                           0x4000000        67108864
(Account)

## Editing non-sensitive data

The token flag 0x400 (1024) grants access rights related to editing non-
sensitive data.

Access right                  ACL bit        ACL bit
Applies to
name                          (HEX)          (DEC)

Any object       Rename object                 0x10           16

Manage custom
Any object                                     0x40           64
fields

Change image
Any object                                     0x100          256
(icon)

Any object       Edit attached files           0x8000         32768

Unit, unit
Register events               0x2000000      33554432
group

Access right                 ACL bit           ACL bit
Applies to
name                         (HEX)             (DEC)

Unit, unit       Create, edit, and
0x800000000       34359738368
group            delete commands

Add or remove
units from the
Retranslator     retranslator,                0x200000          2097152
change their
unique IDs

Resource         Create, edit, and
0x800000          8388608
(Account)        delete POIs

Resource         Create, edit, and
0x2000000         33554432
(Account)        delete geofences

## Editing sensitive data

The token flag 0x800 (2048) grants access rights related to editing sensitive
data.

Access
Applies to                        ACL bit (HEX)             ACL bit (DEC)
right name

Manage
Any object      access to         0x4                       4
this object

Create, edit,
Unit, unit      and delete
0x20000000                536870912
group           service
intervals

Access
Applies to                     ACL bit (HEX)   ACL bit (DEC)
right name

Edit trip,
Unit, unit     driving and
0x4000000000    274877906944
group          health check
settings

Manage
user’s
User                           0x100000        1048576
access
rights

Change
user’s
User                           0x400000        4194304
general
properties

Edit
retranslator
Retranslator   settings        0x100000        1048576
including
start/stop

Create, edit,
Resource
and delete      0x200000        2097152
(Account)
notifications

Create, edit,
Resource
and delete      0x8000000       134217728
(Account)
jobs

Create, edit,
Resource       and delete
0x20000000      536870912
(Account)      report
templates

Access
Applies to                        ACL bit (HEX)          ACL bit (DEC)
right name

Create, edit,
Resource
and delete       0x80000000             2147483648
(Account)
drivers

Create, edit,
Resource
and delete       0x400000000            17179869184
(Account)
orders

Create, edit,
Resource         and delete
0x1000000000           68719476736
(Account)        tags
(passengers)

Create, edit,
Resource
and delete       0x200000000000         35184372088832
(Account)
trailers

## Editing critical data and deleting messages

The token flag 0x1000 (4096) grants access rights related to editing critical
data and deleting messages.

Applies                                       ACL bit        ACL bit
Access right name
to                                            (HEX)          (DEC)

Any
Delete object                   0x8            8
object

Any
Manage object log               0x800          2048
object

Applies                                        ACL bit      ACL bit
Access right name
to                                             (HEX)        (DEC)

Any          View administrative
0x1000       4096
object       fields

Any          Edit administrative
0x2000       8192
object       fields

Edit connectivity
settings (device type,
Unit, unit
UID, phone, access                0x100000     1048576
group
password, messages
filter)

Unit, unit   Create, edit, and delete
0x200000     2097152
group        sensors

Unit, unit
Edit counters                     0x400000     4194304
group

Unit, unit
Delete messages                   0x800000     8388608
group

Unit, unit
Import messages                   0x40000000   1073741824
group

Unit, unit
Export messages                   0x80000000   2147483648
group

## Sending commands

The token flag 0x2000 (8192) grants the permission to send (execute)
commands for units and unit groups.

Access right                 ACL bit      ACL bit
Applies to
name                         (HEX)        (DEC)

Unit, unit
Send commands                0x1000000    16777216
group

Working as an authorized user (unlimited
access)

The token flag -1 means the token doesn’t restrict the authorized user by
token access levels (0x100, 0x200, 0x400, and so on). The following ACL bits
are only available with this flag and aren’t included in any other token flag.

Applies        Access right
ACL bit (HEX)     ACL bit (DEC)
to             name

Edit ACL-
Any object                               0x400             1024
propagated items

Unit, unit
View routes               0x4000000         67108864
group

Unit, unit     Create, edit, and
0x8000000         134217728
group          delete routes

Unit, unit
View events               0x1000000000      68719476736
group

Unit, unit     Create, edit, and
0x2000000000      137438953472
group          delete events

Unit, unit     Use unit in jobs,         0x8000000000      549755813888
group          notifications,

Applies         Access right
ACL bit (HEX)      ACL bit (DEC)
to              name

routes,
retranslators

Resource
Manage account          0x100000000        4294967296
(Account)

### See also

token/update. Create, edit, or delete tokens.
token/login. Authenticate using a token.
core/check_items_billing. Full list of ACL flags by object type.
Frequently asked questions. Common token-related scenarios.

Access rights. Overview of access rights in Wialon.
