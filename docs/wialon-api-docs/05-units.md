# Units

Depending on the specified flags, the response format may vary.

This chapter describes the flags that can be applied to units and the
corresponding parts of the resulting JSON they control. If multiple flags are
specified, their respective parts are combined into a single JSON.

All flags are used only in DEC format.

## Unit flags

The following flags may be applied to units:

HEX value                DEC value           Description

General
0x00000001               1                   properties (base
flag)

0x00000002               2                   Custom properties

0x00000004               4                   Billing information

General custom
0x00000008               8
fields

0x00000010               16                  Image

0x00000020               32                  Messages

0x00000040               64                  GUID

Administrative
0x00000080               128
custom fields

Advanced
0x00000100               256
properties

Commands
0x00000200               512                 available at the
moment

Last message and
0x00000400               1024
location

HEX value    DEC value           Description

0x00000800   2048                Driver code

0x00001000   4096                Sensors

0x00002000   8192                Counters

0x00004000   16384               Routes

0x00008000   32768               Maintenance

0x00010000   65536               Unit logs

Unit configuration
in reports: trip
0x00020000   131072
detector and fuel
consumption

All other unit
0x00040000   262144              settings: message
validity filtering

List of all possible
0x00080000   524288              commands for this
unit

Message
0x00100000   1048576
parameters

Unit connection
0x00200000   2097152
status

0x00400000   4194304             Location

0x00800000   8388608             Profile properties

HEX value                  DEC value                  Description

0x01000000                 16777216                   Tasks

Set all possible
0x3FFFFFFFFFFFFFFF         4611686018427387903
unit flags

## General properties

The flag of general properties is 0x00000001.

```json
{
     "mu": <uint>,     /* Measurement system:
         0 — SI,
         1 — US,
         2 — imperial,
         3 — metric with gallons */
     "nm": "<text>",     /* Name */
     "cls": <uint>,      /* Superclass ID: "avl_unit" */
     "id": <uint>,       /* Unit ID */
     "uacl": <uint>      /* User's access rights to this unit */
}
```

## Custom properties

The flag of custom properties is 0x00000002.

```json
{
     "prp": {                                     /* Custom properties
*/
         "img_rot": "<text>",                     /* Rotate images: 1
- yes, 0 - no */
         "monitoring_sensor_id": "<text>",        /* Sensor ID which w

ill be displayed in the monitoring system */
         "motion_state_sensor_id": "<text>",        /* ID of the sensorused as a motion state source */
         "sensors_colors_id": "<text>",             /* ID of the sensorused as a track color source */
         "use_sensor_color": "<text>",              /* Use sensor colorin the monitoring system: 1 - yes, 0 - no */

         /* One of the parameters for selecting the track color source is used */
         "sensors_colors": "<text>",        /* Table of colors for tracks colored based on sensor values */
         "solid_colors": "<text>",     /* Solid track color */
         "speed_colors": "<text>",     /* Table of colors for coloringtracks based on speed */

         /* Storage of last used colors */
         "track_sensor": "<text>", /* Table of colors for tracks colored based on sensor values */
         "track_solid": "<text>",     /* Solid track color */
         "track_speed": "<text>",     /* Table of colors for coloringtracks based on speed */

         "monitoring_battery_id": "<text>"       /* ID of the sensor showing battery status */
    },
    "ct": <uint>     /* Creation time */
}
```

## Billing information

The flag of billing information is 0x00000004.

```json
{
    "crt": <uint>,       /* Creator ID */
    "bact": <uint>       /* Account ID */
}
```

## Custom fields

The flag of custom fields is 0x00000008.

```json
{
    "flds": {                  /* Custom fields */
         <text>: {            /* Sequence number */
               "id": <uint>, /* ID */
               "n": <text>,   /* Name */
               "v": <text>        /* Value */
         },
         ...
    },
    "fldsmax":<long>, /* Maximum number of custom fields (-1 for unlimited) */
}
```

## Unit image

The flag of the unit image is 0x00000010.

```json
{
    "uri": <text> /* Image link */
    "ugi": <uint> /* Number of image changes */
}
```

## Messages

The flag of messages is 0x00000020.

After specifying this flag, you can receive messages from the unit.

## GUID

The flag of GUID is 0x00000040.

```json
{
    "gd":<text>      /* Unit GUID */
}
```

## Administrative fields

The flag of administrative fields is 0x00000080.

```json
{
    "aflds": {          /* Administrative fields */
         "<text>": {    /* Sequence number */
             "id": <uint>,    /* ID */
             "n": "<text>",    /* Name */
             "v": "<text>"    /* Value */
         }
    },
    "afldsmax": <long>     /* Maximum number of administrative fields
(-1 for unlimited) */
}
```

## Advanced properties

The flag of advanced properties is 0x00000100.

```json
{
    "uid": <text>,      /* Unique ID (hardware) */
    "uid2": <text>,     /* Second unique ID (hardware) */
    "hw": <long>, /* Hardware type */
    "ph": <text>, /* Phone number */
    "ph2": <text>,      /* Second phone number */
    "psw": <text> /* Password */
}
```

## Available commands

The flag of available commands is 0x00000200.

```json
{
    "cmds": [                  /* Array of commands */
         {
             "n": <text>,     /* Name */
             "a": <uint>,     /* Access level (access rights the usermust have to execute this command) */
             "t": <text>,     /* Link type */
             "c": <text>          /* Command type */
         }
    ]
}
```

The types of commands and links are described on the
unit/update_command_definition page. The list of access flags for units is
provided in the General and Units and unit groups sections on the
core/check_items_billing page.

## Last message and location

The flag of the last message and location is 0x00000400.

```json
{
    "pos": {               /* Last known location */
         "t": <uint>,     /* Time (UTC) */
         "y": <double>,     /* Latitude */
         "x": <double>,       /* Longitude */
         "z": <double>,       /* Altitude */
         "s": <int>,          /* Speed */
         "c": <int>,          /* Course */
         "sc": <int>          /* Number of satellites */
    },
    "lmsg": {              /* Last known message */

         ...
    }
}
```

The message format depends on the message type. All types are described
on the messages page.

## Sensors

The flag of sensors is 0x00001000.

```json
{
    "sens": {                  /* Sensors */
         <text>: {            /* Sequence number of the sensor */
               "id": <long>, /* ID */
               "n": <text>,   /* Name */
               "t": <text>,   /* Type */
               "d": <text>,   /* Description */
               "m": <text>,   /* Unit of measurement */
               "p": <text>,   /* Parameter */
               "f": <uint>,   /* Sensor flags */
               "c": <text>,   /* Configuration */
               "vt": <uint>, /* Validation type */
               "vs": <uint>, /* Validation sensor ID */
               "tbl": [         /* Calculation table */
                   {           /* Parameters */
                       "x": <double>,
                       "a": <double>,
                       "b": <double>
                   }
               ]
         },
         ...
    },
    "sens_max": <long>        /* Maximum number of sensors (-1 for unlimited) */
}
```

Sensor flags, types of sensors and validation, as well as examples of
configuration are provided on the unit/update_sensor page.

## Counters

The flag of counters is 0x00002000.

```json
{
     "cfl": <uint>,      /* Calculation flags */
     "cnm": <uint>,      /* Mileage counter, km or miles */
     "cneh": <uint>,     /* Engine hours counter, h */
     "cnkb": <uint>      /* GPRS traffic counter, KB */
}
```

Calculation flags are described on the unit/update_calc_flags page.

## Maintenance

The flag of service intervals is 0x00008000.

```json
{
     "si": {                   /* service intervals */
           <text>: {          /* sequence number of service interval
*/
               "id": <uint>, /* ID */
               "n": <text>,   /* name */
               "t": <text>,   /* description */
               "im": <uint>, /* mileage interval */
               "it": <uint>, /* days interval */
               "ie": <uint>, /* engine hours interval */
               "pm": <uint>, /* last service for mileage interval, km
*/
               "pt": <uint>, /* last service for days interval, sec
(UTC) */
               "pe": <uint>, /* last service for engine hours interval, h */
               "c": <uint>        /* done times */

            },
            ...
       },
       "simax": <long>          /* Maximum number of service intervals
(-1 for unlimited) */
}
```

## Trip detector and fuel consumption

The flag of the trip detector and fuel consumption is 0x00020000.

```json
{
       "rtd": {                                   /* Trip detector */
            "type": <uint>,                         /* Type of movement detection */
            "gpsCorrection": <int>,                 /* Allow GPS correction:
0 - no, 1 - yes */
            "minSat": <uint>,                   /* Minimun number of satellites */
            "minMovingSpeed": <uint>,           /* Minimum moving speed, km/h */
            "minStayTime": <uint>,                  /* Minimum parking time,
seconds */
            "maxMessagesDistance": <uint>,          /* Maximum distance between messages, meters */
            "minTripTime": <uint>,                  /* Minimum trip time, seconds */
            "minTripDistance": <uint>           /* Minimum trip distance, meters */
       },
       "rfc": {                                       /* Fuel consumption */
            "calcTypes": <uint>,                    /* Type of calculation
*/
            "fuelLevelParams": {                      /* Detection of fuel fillings and thefts */
                  "flags": <uint>,                  /* Flags of fillings andthefts */
                  "ignoreStayTimeout": <uint>,      /* Ignore messages after
```

the start of motion, s */

```json
"minFillingVolume": <uint>,           /* Minimum fuel filling
```

volume, liters */

```json
"minTheftTimeout": <uint>,                /* Minimum stay time
```

out to detect fuel theft, s */

```json
"minTheftVolume": <uint>,             /* Minimum fuel theft vo
```

lume, liters */

```json
"filterQuality": <ubyte>,             /* Filtering level (0..2
```

55) */

```json
"fillingsJoinInterval": <uint>,           /* Timeout to separa
```

te consecutive fillings, s */

```json
"theftsJoinInterval": <uint>, /* Timeout to separate c
```

onsecutive thefts, s */

```json
"extraFillingTimeout": <uint> /* Timeout to detect fin
```

al filling volume, s */

```json
},
"fuelConsMath": {              /* Consumption math */
     "idling": <double>,             /* Idling, liters per hour */
     "urban": <double>,              /* Urban cycle, liters per 100
```

km */

```json
"suburban": <double>      /* Suburban cycle, liters per 10
```

0 km */

```json
},
"fuelConsRates": {                     /* Consumption by rates */
     "consSummer": <int>,             /* Summer consumption, liters
```

per 100 km */

```json
"consWinter": <int>,             /* Winter consumption, liters
```

per 100 km */

```json
"winterMonthFrom": <int>,          /* Winter from (month: 0-1
```

1) */

```json
"winterDayFrom": <int>,              /* Winter from (day 1-31)
```

*/

```json
"winterMonthTo": <int>,              /* Winter to (month 0-11)
```

*/

```json
     "winterDayTo": <int>             /* Winter to (day 1-31) */
},
"fuelConsImpulse": {                 /* Impulse fuel consumption se
```

nsors */

```json
             "maxImpulses": <int>, /* Maximum number of impulses */
             "skipZero": <int>         /* Skip the first zero value */

                }
       }
}
```

Types of movement detection are described on the unit/get_trip_detector
page. Types of fuel consumption calculation as well as filling and theft flags
are described on the get_fuel_settings page.

## Commands

The flag of commands is 0x00080000.

```json
{
       "cml": {                        /* List of commands */
                <text>: {            /* Sequence number of the command */
                      "id": <uint>,    /* ID */
                      "n": <text>,     /* Name */
                      "c": <text>,     /* Type */
                      "l": <text>,     /* Link type */
                      "p": <text>,     /* Parameters */
                      "a": <uint>,     /* Access level (access rights the usermust have to send this command) */
                      "f": <uint>        /* Phone number flags: 0 - any (primary, then secondary), 0x1 - primary, 0x2 - secondary */
                },
                ...
       },
       "cml_max": <long> /* Maximum number of commands (-1 for unlimited)       */
}
```

The types of commands and links are described on the
unit/update_command_definition page. The list of access flags for units is
provided in the General and Units and unit groups sections on the
check_items_billing page.

## Message parameters

Allows using the accumulative system of message parameter values.
Parameters will be stored in the corresponding JSON object section, which
will store not only the values of parameters from the last message, but also
the values of parameters from earlier messages.

The flag of message parameters is 0x00100000.

```json
{
    "prms": {                  /* List of message parameters */
        <text>: {             /* Parameter name */
              "v":   <any>,   /* Parameter value */
              "ct": <uint>, /* Time of the last value change */
              "at": <uint>    /* Time of the last message with this parameter */
        },
        ...
    }
}
```

## Connection

The flag of the unit connection status is 0x00200000.

```json
{
    "item": {
        "netconn": <bool>
    }
}
```

## Location

The flag of the unit location is 0x00400000.

```json
{
    "pos":{                 /* Last known location */
        "t":<uint>,           /* Time (UTC) */
        "y":<double>, /* Latitude */
        "x":<double>, /* Longitude */
        "z":<double>, /* Altitude */
        "s":<int>,           /* Speed */
        "c":<int>,           /* Course */
        "sc":<int>           /* Number of satellites */
    }
}
```

## Profile properties

The flag of profile properties is 0x00800000.

```json
{
    "pflds":{
        "<long>":{            /* Field ID */
              "id":<long>, /* Field ID */
              "n":<text>,      /* Field name */
              "v":<text>       /* Field value */
    }
}
```

## Tasks

The flag of tasks is 0x01000000.

```json
{
    "task_sub_type": <uint>,      /* Task subtype */
    "task_reg_type": <uint>,      /* Register type */
    "task_evt_name": <text>,      /* Task name */
    "task_id": <text>,            /* Task ID */

    "task_update_time": <int>, /* Last update time */
    "task_status": <uint>,       /* Task status */
    "task_priority": <uint>,     /* Task priority */
    "task_assignee": <long>,     /* Task assignee */
    "task_comments": <text>,     /* Comments on the task */
    "task_account": <long>,      /* Account of the task */
}
```
