# Messages

This chapter describes the formats of all message types. You can request
messages of a specific type using flags.

All flags are used only in DEC format.

## Message types

The following message types are available:

Flag in          Flag in
Description
HEX              DEC

0x0000           0                Data message

0x0100           256              SMS

0x0200           512              Command

0x0400           1024             User log

0x0300           768              User notification

0x0500           1280             Billing message

0x0600           1536             Event

0x0700           1792             Plot cultivation

0x0800           2048             WDC service record

0x0900           2304             SMS from driver

0x1000           4096             Log record

Flag in           Flag in
Description
HEX               DEC

0x2000            8192              Video usage

Message about a triggered
0x4000            16384
notification

0x5000            20480             Task

To delete specific messages, you must have the following ACL flags:

Message              Message flag
ACL flag HEX(DEC)
type                 HEX(DEC)

Data message         0x0000(0)                    0x800000(8388608)

SMS                  0x0100(256)                  0x800000(8388608)

Command              0x0200(512)                  0x800000(8388608)

Event                0x0600(1536)                 0x2000000(33554432)

Log                  0x1000(4096)                 0x800(2048)

For further information about ACL flags, see the Access
flags section.

## Data message

The flag of data messages is 0x0000.

{

```json
"t": <uint>,           /* Message time (UTC) */
"f": <uint>,           /* Flags (see below) */
"tp": "ud",            /* Message type ('ud' denotes a data messag
```

e) */

```json
"pos": {               /* Location */
     "y": <double>, /* Latitude */
     "x": <double>, /* Longitude */
     "z": <int>,       /* Altitude */
     "s": <uint>,      /* Speed */
     "c": <uint>,      /* Course */
     "sc": <ubyte>     /* Number of satellites */
},
"i": <uint>,           /* Input data */
"o": <uint>,           /* Output data */
"p": {                 /* Parameters */
     <text>: <double>...
},
     "sensors": {          /* Present only when calcSensors paramet
```

er is used */
"<sensor_id>": {

```json
"value": <double|text>,        /* Raw sensor value
```

*/

```json
"format": {
    "value": <text>            /* Formatted sensor
```

value with units */

```json
                   }
                                 }
                       }
"lc": <int>,           /* LBS message checksum */
"rt": <uint>           /* Message registration time (UTC) */
```

}

Data message flags:

HEX              DEC
Description
value            value

0x01             1             Location data is available.

0x02             2             Information about input data is available.

0x04             4             Information about output data is available.

0x10             16            The message contains an alarm bit.

The message contains information about
0x20             32            the driver code in the avl_driver
parameter.

0x20000          131072        The message was corrected by LBS.

## SMS

The flag of SMS messages is 0x0100(256).

{

```json
"t": <uint>,      /* Message time (UTC) */
"f": <uint>,      /* Flags: SMS messages have no flags, so 0 will
```

be placed */

```json
"tp": "us",       /* Message type ('us' denotes an SMS message)
```

*/

```json
"st": <text>,     /* Message text */
"mp": <text>,     /* Modem phone number */
"p": {}           /* Parameters */
```

}

## Command

The flag of commands is 0x0200(512)

```json
{
        "t": <uint>,     /* Message time (UTC) */
        "f": <uint>,     /* Flags: commands have no flags, so 0 will be placed */
        "tp": "ucr",     /* Message type ('ucr' denotes a command)
*/
        "ca": <text>,    /* Command name */
        "cn": <text>,    /* Command type */
        "cp": <text>,    /* Command parameters */
        "ui": <uint>,    /* User ID */
        "ln": <text>,    /* Link name */
        "lt": <text>,    /* Link type */
        "et": <uint>,    /* Execution time */
        "p": {}              /* Parameters */
}
```

Link types are described on the Update command definition page.

## Event

The flag of events is 0x0600(1536).

```json
{
        "t": <uint>,     /* Message time (UTC) */
        "f": <uint>,     /* Flags (see below) */
        "tp": "evt",     /* Message type ('evt' denotes an event)
*/
        "et": <text>,    /* Event text */
        "x": <double>,   /* Longitude */
        "y": <double>,   /* Latitude */
        "p": {}          /* Parameters */

}
```

Event flags:

HEX           DEC
Description
value         value

0x0           0              Simple event.

0x1           1              Violation.

0x2           2              Maintenance service or fuel filling.

0x4           4              Route progress.

Maintenance service. This flag is set in
0x10          16
addition to 0x2.

Fuel filling. This flag is set in addition to
0x20          32
0x2.

## Notification

The flag of notifications is 0x0300(768).

```json
{
        "t": <uint>,      /* Message time (UTC) */
        "f": <uint>,      /* Flags: notifications have no flags, so
0 will be placed */
        "tp": "xx",           /* Message type */
        "p": {}               /* Parameters */
}
```

## Billing message

The flag of billing messages is 0x0500(1280).

```json
{
          "t": <uint>,      /* Message time (UTC) */
          "f": <uint>,      /* Flags: 0x1 is set when the message contains payment information */
          "tp": "xx",           /* Message type */
          "p": {}               /* Parameters */
}
```

## SMS to the driver

The flag of SMS messages is 0x0900(2304).

```json
{
          "t": <uint>,        /* Message time (UTC) */
          "f": <uint>,        /* Flags: 0x1 is set when the message issent */
          "tp": "xx",         /* Message type */
          "p": {              /* Parameters */
                    "phone": <text>,         /* Phone number */
                    "sms_text": <text>,      /* SMS text */
                    "driver_name": <text>,   /* Driver name */
                    "driver_id": <uint>      /* Driver ID */
          }
}
```

## Log

The flag of log records is 0x1000(4096)

{

```json
"t": <uint>,       /* Message time (UTC) */
"f": 4096,         /* Flags: 4096 denotes a log record */
"tp": "xx",        /* Message type */
"p": {             /* Parameters */
         "user": <text>,            /* Username */
         "action": <text>,          /* Action */
         "host": <text>,            /* Host */
         "p1": <text>,              /* Parameters */...
}
```

}

## WLN messages

WLN messages have the following format:

REG;time;lon;lat;speed;course;double params;int params;text param
s;long params;boolean params;

Inside the section, the parameters are separated by commas. Example:

REG;1466585078;30.4367027283;59.7207145691;1;273;ALT:24.0,adc1:0.
0,adc2:25.57,adc3:0.0,adc4:0.0,adc5:0.0,adc6:0.0,fuel1:0.0,fuel2:1
70.0,fuel3:0.0,odometer:7293607.0,acc:0.0,pwr_int:0.731,pwr_ext:2
5.751,hdop:1.7;in13:1,,SATS:5,count1:1,count2:0,temp1:0,temp2:23,t
emp3:0,sats_glonass:0,sats_gps:5;soft_version:"44";;;

## Messages about triggered notifications

When a notification is triggered, the system stores a message with flag
0x4000 (16384). These messages contain detailed information about the
notification trigger event.

```json
{
    "t": <uint>,             // Trigger timestamp (Unix time).
    "f": 16384,              // Message type flag (0x4000).
    "tp": "<text>",          // Message type identifier.
    "rt": <uint>,            // Message reception time (Unix time).
    "p": {                   // Parameters object.
        "name": "<text>",              // Notification name.
        "resource_id": <uint>,         // ID of the resource where notification is configured.
        "trigger_type": "<text>",      // Notification type (e.g., "msg_param", "geofence", etc.).
        "actions": "<text>",           // Action types (comma-separated,
e.g., "message,event")..
        "unit_id": <uint>,             // Unit ID for which the notification was triggered.
        "text": "<text>",              // Notification message text.
        "trigger_time": <uint>,        // Trigger timestamp (Unix time).
        "account_id": <uint>           // ID of the resource account.
    }
}
```
