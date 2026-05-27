# Users

Depending on the specified flags, the response format may vary.

This chapter describes the flags that can be applied to users and the
corresponding parts of the resulting JSON they control. If multiple flags are
specified, their respective parts are combined into a single JSON.

All flags are used only in DEC format.

## User flags

The following flags can be applied to users:

HEX value          DEC value                  Description

0x00000001         1                          General properties (base flag)

0x00000002         2                          Custom properties

0x00000004         4                          Billing information

0x00000008         8                          Custom fields

0x00000020         32                         Messages

0x00000040         64                         GUID

0x00000080         128                        Administrative fields

0x00000100        256                         Other user properties

0x00000200        512                         Notifications

User host connectivity settings
0x00000400        1024
(e.g. host mask)

0x00000800        2048                        User mobile apps

0x3FFFFFFFFF      461168601842
Set all user flags
FFFFFF            7387903

## General properties

The flag of general properties is 0x00000001.

```json
{
        "nm": "<text>",     /* Username */
        "cls": <uint>,     /* Superclass ID: "user" */
        "id": <uint>,     /* User ID */
        "mu": <uint>,     /* Measurement system:
                0 - SI,
                1 - US,
                2 - imperial,
                3 - metric with gallons */
        "uacl": <uint>     /* User's access rights to this user */
}
```

## Custom properties

The flag of custom properties is 0x00000002.

You can store any user data in custom properties. Usually, such settings are
user e-mail, map position after logging in, and so on

```json
{
        "prp": {
                 "cfmt": "<text>",      /* Coordinates format: 0 - degrees and minutes, 1 - degrees */
                 "email": "<text>",     /* User email */
                 "msc": "<text>",       /* Map position after loggingin: 0 - default, 1 - saved */
                 "poisrv": "<text>"     /* Render POIs on the server
*/
        }
}
```

## Billing information

The flag of billing information is 0x00000004.

```json
{
        "crt": <uint>,   /* Creator ID */
        "bact": <uint>   /* Account ID */
}
```

## Custom fields

The flag of custom fields is 0x00000008.

```json
{
        "flds": {                  /* Custom fields */
                 "<text>": {            /* Sequence number */
                         "id": <uint>,      /* ID */

                         "n": "<text>",     /* Name */
                         "v": "<text>"      /* Value */
                   }
        },
        "fldsmax": <long> /* Maximum number of custom fields (-1 for unlimited) */
}
```

## Messages

The flag of custom fields is 0x00000020.

After setting this flag, you can receive messages from the unit.

```json
{}
```

## GUID

The flag of GUID is 0x00000040.

```json
{
        "gd": <text>     /* User GUID */
}
```

## Administrative fields

The flag of administrative fields is 0x00000080.

```json
{
        "aflds": { /* Administrative fields */

                  <text>: { /* Sequence number */
                          "id": <uint>, /* ID */
                          "n": <text>, /* Name */
                          "v": <text> /* Value */
                  },
                  ...
        },
        "afldsmax": <long>,        /* Maximum number of administrative fields (-1 for unlimited) */
}
```

## Other user properties

The flag of other user properties is 0x00000100.

```json
{
        "fl": <uint>, /* Flags of user settings */
        "hm": <text>, /* Host mask */
        "ld": <uint>, /* Last login time */
        "pfl": <uint>, /* Parent account flags */
        "ap": {
             "type": <uint>, /* Two-factor authentication type */
             "phone": <text>       /* Two-factor authentication type
*/
        }
}
```

The flags of user settings are listed on the update_user_flags page.

## Notifications

The flag of notifications is 0x00000200.

```json
{
        "usnf": {   /* User notifications */
                "<text>": {   /* Sequence number */
                         "id": <long>,       /* ID */
                         "t": <uint>,        /* Lifetime (seconds) */
                         "d": "<text>",        /* Notification text */
                         "h": "<text>",        /* Subject */
                         "s": "<text>"       /* Sender */
                }
        }
}
```

## User mobile flags

The flag of user mobile flags is 0x00000800.

```json
{
        "mobile_apps": <text>,
}
```
