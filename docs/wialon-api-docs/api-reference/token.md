# token

This section describes the methods for working with tokens.

## list

To get the list of tokens, use the token/list method.

```http
svc=token/list&params={"userId":<text>}
```

### Parameters

The request can contain the userId parameter, specifying the subuser ID.
The parameter is optional.

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
[
    {
         "h": <text>,         /* Unique token name, 72 symbols. */
         "app": <text>,        /* Application name. */
         "at": <uint>,        /* Token activation time, UNIX time. */
         "ct": <uint>,        /* Token creation time, UNIX time. */
         "dur": <uint>,        /* Token duration after activation, in seconds. */
         "fl": <uint>,        /* Access flags. */
         "items": [<long>],    /* List of item IDs to which the token grants access. */
         "p": <text>          /* Custom parameters; the value must be anobject or an array of objects. */
         "ll" <uint>,         /* Last authorization time, UNIX time. */
    },

     ... /* Other tokens (if any). */
]
```

If the request fails, the response contains error code 7, indicating that the
user doesn’t have the required access right
(ADF_ACL_ITEM_VIEW_PROPERTIES).

## login

To get a token, use the forms mentioned in login.
To work under the token, token/login is used. The method signature is as
follows:

```http
svc=token/login&params={"token":<text>,
                           "operateAs":<text>,
                           "fl":<uint>
                      }
```

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| token* | Unique token name. Consists of 72 symbols. |
| operateAs | Subuser name for login. The parameter is optional. |
| fl* | Response flags (see below). |

## Response flags

Flag in HEX        Flag in DEC       Description

0x1                1                 Basic information.

0x2                2                 User information.

0x4                4                 Token information.

0x8                8                 Information about items.

0x10               16                Information about billing services.

0x20               32                Custom properties of the user.

## How to get a token name

Create a new token (token/update method, callmode:create);
If tokens are already created, execute the token/list method.

You can’t log in using a non-activated token (at parameter in token
parameters).

### Response

If the request is completed successfully, a new token parameter is added
to all token parameters as a value. The response of the following format is
returned:

```json
{
      "eid": <text>,                    /* Session ID. */
      "gis_sid": <text>,                /* Session ID for GIS services. */
      "host": <text>,                   /* Host. */
      "hw_gw_ip": <text>,               /* Hardware gateway IP. */

  "au": <text>,                         /* Username. */
  "pi": <int>,                          /* Ping interval. */
  "tm": <uint>,                         /* Current time (UTC). */
  "wsdk_version": <text>,              /* SDK version */

  "user": {                             /* User on whose behalf you wa
```

nt to perform login. */

```json
"nm": <text>,                    /* Name. */
"cls": <uint>,                   /* ID of superclass "user". */
"id": <long>,                    /* ID */
"prp": {                         /* Custom properties, for exam
```

ple: */

```json
"dst": <text>,              /* Daylight saving time */
"language": <text>,         /* Language (two-letter code)
```

*/

```json
"msakey": <text>,           /* Access key to the mobile si
```

te */

```json
"pcal": <text>,             /* Iranian calendar */
"tz": <text>,               /* Time zone */
"us_units": <text>,         /* US metrics (miles and gallo
```

ns) */
...

```json
},
"crt": <uint>,                   /* Creator ID. */
"bact": <uint>,                  /* Account ID. */
"fl": <uint>,                    /* User flags. */
"hm": <text>,                    /* Host mask. */
"uacl": <uint>,                  /* User access to their accoun
```

t. */

```json
"mu": <uint>,                    /* Measurement system. */
"ct": <uint>,                    /* User creation date. */
"ftp": { <text> },               /* FTP settings */
"ld": <uint>,                    /* Last login date. */
"pfl": <uint>,                   /* Creator flag */
"ap": {                          /* Two-factor authentication s
```

ettings */

```json
"type": <uint>,             /* Authentication type (0 - no
```

ne, 1 - email, 2 - SMS). */

```json
     "phone": <text>             /* Phone number. */
},

  "mapps": { <text> },           /* Mobile apps list. */
  "mappsmax": <int>              /* Restrictions on mobile appl
```

ications specified in the billing plan. */

```json
},

"classes": {                          /* Superclasses available to t
```

he current user (key - superclass name, value - superclass ID): */

```json
       "avl_hw": <uint>,              /* Hardware type */
       "avl_resource": <uint>,        /* Resource */
       "avl_retranslator": <uint>, /* Retranslator */
       "avl_unit": <uint>,            /* Unit */
       "avl_unit_group": <uint>,      /* Unit group */
       "user": <uint>,                /* User */
       "avl_route": <uint>            /* Route */
},

"features": {
       "unlim": <bool>,               /* Billing plan type: 0 - regu
```

lar, 1 - special (for development/testing). */

```json
"svcs": {                      /* Hash collection of allowed
```

services. If the service is not mentioned here, it is forbidden.
*/
"<service_name>": <bool>, /* Key - service name, valu
e: 0 - the service is available, but the limit is reached; 1 - the
service is available and can be used */
...

```json
       }
},

...,                                  /* Core/login response. */

"token": "{\"app\":\"<text>\",\"ct\":<uint>,\"at\":<uint>,\"du
```

r\":<uint>,\"fl\":<uint>,\"p\":\"<text>\",\"items\":[<long>]}",

```
/* All token settings as esca
```

ped JSON. */

...                                   /* Core/login response */
}

If the request fails, an error code is returned.

### Error codes

Error
Description
code

6              Unknown error.

4              Wrong token length.

1003           Limit of requests.

User disabled, token activation time not reached, no
7
access to service.

The specified subuser is not found or you have no access
8
rights to this user.

## update

This method is used for managing your own tokens and tokens of users to
whom you have access. The method is not used for authorization. To log in,
use token/login.

To create, edit or delete the token, use the token/update method:

```http
svc=token/update&params={"callMode":<text>,
              "userId":<text>,
              "h":<text>,
              "app":<text>,
              "at":<uint>,
              "dur":<uint>,
              "fl":<uint>,

             "p":<text>,
             "items":[<long>],
             "deleteAll":<bool>|<text>
        }
```

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| Action you want to perform. To create a token, specify | callMode*    create in this parameter. To edit a token, pass update, and to delete it, pass delete. |
| userId | Subuser ID. The parameter is used to manage other user tokens. |
| Token name. Consists of 72 characters. This parameter | h*           must be used in requests for editing and deleting a token. |
| app* | Application name. |
| Token activation time, UNIX-time. | You can pass 0 in this parameter so that the token is at* activated immediately after the request is successfully completed. |
| Token duration after activation, seconds. | dur* Pass 0 in this parameter to set an infinite duration. |
| fl* | Access flags. |
| Name | Description |
| Custom parameters, value must be an object or an array | p* of objects. |
| items | List of item IDs to which the token grants access. |
| deleteAll | Relevant for callMode:delete Pass 1 or true to delete all the created tokens. |
| Tokens are deleted automatically after 100 days of | inactivity (even with dur:0). |
| Example of an object for the parameter p: |  |

```json
"p":"{\"paramA\":\"valueB\"}"
```

Example of an array of objects for the parameter p:

```json
"p":"[{\"paramA\":\"valueB\"},{\"paramB\":\"valueD\"}]"
```

## Access flags

Value            Description

0x100            Online tracking.

Value           Description

0x200           View access to most data.

0x400           Modification of non-sensitive data.

0x800           Modification of sensitive data.

Modification of critical data, including message
0x1000
deletion.

0x2000          Communication with the unit (sending commands).

Unlimited operation as an authorized user (allows
0xFFFFFFFF
managing user tokens).

For further information about token flags, see Tokens.

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
{
     "h":<text>,       /* Unique token name, 72 characters. */
     "app":<text>,     /* Application name. */
     "at":<uint>,      /* Token activation time, UNIX-time. */
     "ct":<uint>,      /* Token creation time, UNIX-time. */
     "dur":<uint>,     /* Token duration after activation, seconds.
*/
     "fl":<uint>,      /* Access flags. */
     "items":[<long>], /* List of item IDs to which the token grant

s access. */
      "p":<text>         /* Custom parameters. The value must be an object or an array of objects. */
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4               Wrong input parameters.

1003            Request limit reached.

One of the following errors:
Wrong token.
User token not found.
7
Failed to delete the token.
No ADF_ACL_USER_OPERATE_AS access right to the
user.
