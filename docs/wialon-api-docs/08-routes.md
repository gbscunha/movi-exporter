# Routes

Depending on the specified flags, the response format may vary.

This chapter describes the flags that can be applied to routes and the
corresponding parts of the resulting JSON they control. If multiple flags are
specified, their respective parts are combined into a single JSON.

All flags are used only in DEC format.

## Route flags

The following flags can be applied to routes:

HEX value                DEC value             Description

0x00000001               1                     Base flag

0x00000002               2                     Custom properties

0x00000004               4                     Billing information

0x00000040               64                    GUID

Administrative
0x00000080               128
fields

0x00000100               256                   Configuration

0x00000200               512                   Check points

0x00000400               1204                  Schedules

0x00000800               2048                  Rides

Route monitor
0x00001000               4096
state

Set all possible
0x3FFFFFFFFFFFFFFF       4611686018427387903
route flags

## General properties

The flag of general properties is 0x00000001.

```json
{
    "nm": <text>,     /* Name */
    "cls": <uint>,    /* Superclass ID: "avl_route" */
    "id": <uint>,     /* Route ID */
    "mu": <uint>,     /* Measurement units:
                          0 — SI,
                          1 — US,
                          2 — imperial,
                          3 — metric with gallons */
    "uacl": <uint>    /* User's access rights to the route */
}
```

## Custom properties

The flag of custom properties is 0x00000002.

You can store any route data in custom properties.

```json
{
    "prp": {}    /* Custom properties */
}
```

## Billing information

The flag of billing information is 0x00000004.

```json
{
    "crt": <uint>,     /* Creator ID */
    "bact": <uint>     /* Account ID */
}
```

## GUID

The flag of GUID is 0x00000040.

```json
{
    "gd": <text>     /* Route GUID */
}
```

## Administrative fields

The flag of administrative fields 0x00000080.

```json
{
    "aflds": {                  /* Administrative fields */
         <text>: {            /* Sequence number */
               "id": <uint>, /* ID */
               "n": <text>,   /* Name */
               "v": <text>        /* Value */
         },
         ...
    },
    "afldsmax": <long>,           /* Maximum number of administrativefields (-1 for unlimited) */
}
```

## Configuration

The flag of configuration is 0x00000100.

```json
{
    "rcfg":{                   /* Configuration */
         "color":<long>,          /* Color (ARGB) */
         "descr":<text>,          /* Description */
         "units":[<long>]     /* Array of unit IDs */

    }
}
```

## Check points

The flag of check points is 0x00000200.

```json
{
    "rpts":[                     /* Check points */
        {
               "n": <text>,     /* Name */
               "f": <uint>,     /* Type (see below) */
               "u": <long>,     /* Unit ID, 0 — if the check point is not of the "check point from a unit" type */
               "y": <double>,       /* Longitude */
               "x": <double>,       /* Latitude */
               "r": <uint>          /* Radius, m */
        },
        ...
    ]
}
```

Check points can be of the following types:

1 — check point from the map or POI;
2 — check point from a geofence;

3 — check point from a unit.

## Schedules

The flag of schedules is 0x00000400.

```json
{
    "rs": {     /* List of schedules */
        "<text>": {     /* Schedule sequence number */

              "id": <long>,      /* Schedule ID */
              "n": "<text>",      /* Name */
              "f": <uint>,     /* Type */
              "tz": <uint>,      /* Time zone */
              "cfg": {    /* Custom configuration (example) */
                   "autoName": <byte>,          /* Use an automatically generated name: 0 — no, 1 — yes */
                   "enabled": <byte>,          /* Create rides for the schedule automatically: 1 — enable, 0 — disable */
                   "name": "<text>",      /* Ride name */
                   "roundFlags": <uint>,          /* Ride flags */
                   "units": [<long>],          /* Array of unit IDs */
                   "validityPeriod": <uint>         /* Validity period */
              },
              "tm": [    /* Point visit time */
                   {
                        "at": <uint>,     /* Arrival time */
                        "ad": <uint>,     /* Deviation from the arrival time */
                        "dt": <uint>,     /* Departure time */
                        "dd": <uint>     /* Deviation from the departuretime */
                   }
              ],
              "sch": {    /* Time limitation */
                   "f1": <uint>,     /* Beginning of interval 1 */
                   "f2": <uint>,     /* Beginning of interval 2 */
                   "t1": <uint>,     /* End of interval 1 */
                   "t2": <uint>,     /* End of interval 2 */
                   "m": <uint>,     /* Mask for days of the month */
                   "y": <uint>,     /* Month mask */
                   "w": <uint>     /* Mask for days of the week */
              }
          }
    }
}
```

Schedule types are described in the update_schedule chapter.

## Rides

The flag of rides is 0x00000800.

```json
{
    "rr": {       /* Rides */
        "<text>": {          /* Ride sequence number */
              "id": <long>,        /* Ride ID */
              "n": "<text>",        /* Name */
              "d": "<text>",        /* Description */
              "sh": "<text>",        /* Schedule name */
              "f": <uint>,        /* Ride flags */
              "tz": <uint>,        /* Time zone */
              "u": <long>,        /* Unit assigned to this ride */
              "at": <uint>,        /* Activation time */
              "vt": <uint>,        /* Time from which validity period begins */
              "vp": <uint>,        /* Validity period */
              "sts": <uint>,        /* State flags */
              "st": {        /* Ride state */
                    "st": {     /* General ride state */
                         "pi": <uint>,       /* Index of the check point (42
94967295 if the ride hasn't started) */
                         "ps": <uint>,       /* State and event flags */
                         "ut": <uint>      /* Last event time */
                    },
                    "pts": {     /* State by points */
                         "<text>": {      /* ID of the check point */
                               "st": <uint>,       /* Event flags */
                               "tm": <uint>       /* Last event time */
                         }
                    }
              }
        }
    }
}
```

Values of ride, state and event flags are described in the get_round_data
chapter.
