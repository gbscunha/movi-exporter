# retranslator

This section describes all the methods that can be applied to retranslators.
The creation of retranslators is described here.

## update_config

To update retranslator configuration, use the retranslator/update_config
method:

```http
svc=retranslator/update_config&params={"itemId":<long>,
                          "config":{
                              "protocol":<text>,
                              "server":<text>,
                              "port":<ushort>,
                              "v6type":<text>,
                              "auth":<text>,

                              "attach_sensors":<bool>,
                              "ssl":<text>,
                              "login":<text>,
                              "password":<text>,
                              "notauth":<int>
                       }}
```

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| itemId* | Retranslator ID. |
| Configuration. The set of parameters in the object | config* config depends on the protocol type. |
| protocol* | Protocol name (see below). |
| server* | Server for retransmission. |
| port* | Port (for all protocols except NIS) |
| Use protocol v.6 (only for Granit Navigator): |  |
| v6type*              1 — yes | 0 — no |
| auth* | Authorization (only for NIS and Wialon IPS) |
| attach_sensors    Retranslate calculated sensor values (for Wialon IPS | & Wialon Retranslator) |

#### 1 — yes

| Name | Description |
| --- | --- |
| 0 — no | The parameter is optional. |
| Secure connection (for NIS): |  |
| ssl*           1— yes | 0 — no |
| login* | Login. |
| password* | Password. |
| Disable authorization (only for EGTS): |  |
| notauth*       1— yes | 0 — no |

## Protocols

Value                    Protocol

wialon                   Wialon Retranslator

wialon_ips               Wialon IPS

nis                      Nis

granit3                  Granit Navigator

skaut                    Skaut

Value                            Protocol

cyber_glx                        Cyber GLX

vt300                            VT300

egts                             EGTS

soap                             SOAP

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
{
      "rtrc":{
          "port":<ushort>,   /* Port (for all except NIS). */
          "protocol":<text>,      /* Protocol. */
          "server":<text>,   /* Server for retransmission. */
          "v6type":<text>,   /* Protocol v.6 (only for Granit Navigator): 1 — yes, 0 — no. */
          "auth":<text>,          /* Authorization (only for NIS and Wialon IPS). */
          "ssl":<text>,        /* Secure connection (for NIS): 1 — yes,
0 — no */
          "login":<text>,         /* Login. */
          "password":<text>,      /* Password. */
          "notauth":<int>         /* Disable authorization (only for E
GTS): 0 — no, 1 — yes. */
      }
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

Failed to parse input parameters or failed to set the
4
configuration.

No ADF_ACL_AVL_RETR_EDIT_SETTINGS access right to
7
the retranslator.

6            Failed to generate the response.

## get_stats

To obtain data on the status of history retransmission, use the
retranslator/get_stats method.

```http
svc=retranslator/get_stats&params={"itemId":<long>}
```

### Parameters

The request must contain the itemId parameter, specifying the
retranslator ID.

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
{
    "au": <long>, /* The number of objects which have been added t

o the retranslator or removed from it directly. */
    "ru": <long>, /* The number of objects in the queue for history retransmission */
    "hf": <long>, /* Time when the retransmission started. */
    "ht": <long>   /* Time when the retransmission finished. */
    "hc": <uint>, /* Time of the last retransmitted message. */
    "hms": <uint>, /* Current queue of historical messages. */
    "hp": <uint>, /* Progress percentage. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

No ADF_ACL_AVL_RETR_EDIT_SETTINGS access right to
7
the retranslator.

4            Wrong input parameters.

## list

To get the list of custom retranslators, use the retranslator/list method.

```http
svc=retranslator/list&params={}
```

### Parameters

No parameters are required. Pass an empty object in the request.

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
{
    "custom_retranslators": [
         {
             "name": "apad_gps",
             "params": {
                 "fields": [
                      {
                           "key": "server",
                           "type": "name"
                      },
                      {
                           "key": "api_key",
                           "type": "name"
                      },
                      {
                           "key": "password",
                           "type": "name"
                      }
                 ],
                 "name": "APAD GPS",
                 "public": 1
             }
    },
    {
             "name": "blac_solutions",
             "params": {
                 "fields": [
                      {
                           "key": "server",
                           "type": "name"
                      },
                      {
                           "key": "username",
                           "type": "name"

                        },
                        {
                              "key": "password",
                              "type": "name"
                        }
                   ],
                   "name": "Blac Solutions IQER",
                   "public": 1
              }
        },
        ...
    ]
}
```

Otherwise, an error code is returned.

### Error codes

Error code         Description

5                  Failed to get custom retranslators.

6                  The current user has no right to execute the method.

## update_units

To add units to a retranslator or remove them from it, use the
retranslator/update_units method.

```http
svc=retranslator/update_units&params={"itemId":<long>,
                             "units":[{"a":<text>,
                              "i":<long>,
                              "st":<uint>}, ...],

                        "callMode":<text>
}
```

Set callMode to add and include a description for each object in the units
array.

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| itemId* | Retranslator ID. |
| units* | Array of units IDs for retransmission. |
| i* | Unit ID. |
| a* | Hardware unique ID. |
| st | Time when the retransmission stops. The parameter is optional. |
| callMode | Mode: add or remove. The parameter is optional. |

### Response

```json
{
    "rtru":[
          {
              "i":<long>,    /* Unit ID. */

             "a":<text>,    /* Hardware unique ID. */
             "st":<uint>    /* Time when retransmission stopped. */
        }
    ]
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

No ADF_ACL_AVL_RETR_EDIT_SETTINGS access right to
7
the retranslator.

Failed to parse the input text or no current retranslator
4
units.

6             Failed to generate the response.

## update_operating

To start or stop a retranslator or retransmission for a past period, use the
method retranslator/update_operating:

```http
svc=retranslator/update_operating&params={"itemId":<long>,
                        "operate":<bool>,
                        "stopTime":<uint>,
                        "timeFrom":<uint>,
                        "timeTo":<uint>,
                        "callMode":<text>
                 }
```

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| itemId* | Retranslator ID. |
| Start or stop retransmission: use true to start and false | operate* to stop. 1 and 0 are also accepted. |
| Set callMode to switch to start or stop the retranslator. Set | callMode     callMode to history to start or stop the retransmission for a past period. If not set, the default value is switch. |
| Time, when retransmission will be stopped automatically. | stopTime     The parameter can be used only when callMode=switch and operate=true. Optional parameter. |
| timeFrom | Beginning of history retransmission, Unix time. Required only when callMode=history and operate=true. |
| timeTo | End of history retransmission, Unix time. Required only when callMode=history and operate=true. |

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
{
    "rtro":<int>,    /* 0 - stopped, 1 - started */
    "rtrst":<uint>    /* Time when the retransmission stops. Unix ti

me. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4            Wrong input parameters or failed to start/stop retranslator.

The retranslator isn’t found or the user doesn’t have the
ADF_ACL_AVL_RETR_EDIT_SETTINGS access right to the
7
retranslator (Edit retranslator properties including
start/stop).
