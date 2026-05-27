# Resources

Depending on the specified flags, the response format may vary.

This chapter describes the flags that can be applied to resources and the
corresponding parts of the resulting JSON they control. If multiple flags are
specified, their respective parts are combined into a single JSON.

All flags are used only in DEC format.

## Resource flags

The following flags can be applied to resources:

HEX value        DEC value         Description

0x0000000
1                 Base flag
1

0x0000000
2                 Custom properties
2

0x0000000
4                 Billing information
4

0x0000000
8        General custom fields
8

0x0000002
32       Messages
0

0x0000004
64       GUID
0

0x0000008
128      Administrative custom fields
0

0x0000010
256      Drivers
0

0x0000020
512      Jobs
0

0x0000040
1024     Notifications
0

0x0000080
2048     POIs
0

0x0000100
4096     Geofences
0

0x0000200
8192     Report templates
0

0x0000400            List of units to which drivers can be
16384
0                    assigned automatically

0x0000800
32768    Driver groups
0

0x0001000
65536               Trailers
0

0x0002000
131072              Trailer groups
0

0x0004000                           List of units to which trailers can be
262144
0                                   assigned automatically

0x0008000
524288              Orders
0

0x0010000
1048576             geofences groups
0

0x0020000
2097152             Tags (passengers)
0

List of units to which tags
0x0040000
4194304             (passengers) can be assigned
0
automatically

0x0080000
8388608             Tag groups (passenger groups)
0

0x3FFFFFFF      4611686018
Set all possible resource flags
FFFFFFFF        427387903

## General properties

The flag of general properties is 0x00000001.

```json
{
    "nm": <text>,    /* Name */
    "cls": <uint>,   /* Superclass ID: "avl_resource" */

       "id": <uint>,       /* Resource ID */
       "mu": <uint>,       /* Measurement system:
                             0 — SI,
                             1 — US,
                             2 — imperial,
                             3 — metric with gallons */
       "uacl": <uint>      /* Current user's access rights to the resource */
}
```

## Custom properties

The flag of custom properties is 0x00000002.

You can store any resource data in custom properties.

```json
{
       "prp": {   /* Custom properties */
            "emails": "[<text>]",                 /* List of emails for jobs */
            "nf_rep_emails": "[<text>]", /* List of emails for notifications */
            "phones": "[<text>]"                  /* List of phone numbers forthe "Send fuel information by email or SMS" job */...
       },
       "ftp": {   /* FTP settings */
            "hs": <text>,     /* Host */
            "lg": <text>,     /* Login */
            "pt": <text>,     /* Directory path */
            "ch": <uint>,     /* FTP settings validity: 1 — yes, 0 — no
*/
            "tp": <uint>,     /* Use Wialon hosting FTP: 1 — yes, 0 — no
*/
            "fl": <uint>      /* Wialon hosting FTP availability: 1 — yes, 0 — no */
       }

}
```

## Billing information

The flag of billing information is 0x00000004.

```json
{
    "crt": <uint>,      /* Creator ID */
    "bact": <uint>,     /* Account ID */
    "bpact": <uint>     /* Parent account ID */
}
```

## General custom fields

The flag of custom fields is 0x00000008.

```json
{
    "flds": {          /* Custom fields */
         "<uint>": { /* Sequence number */
               "id": <uint>,   /* ID */
               "n": <text>,    /* Name */
               "v": <text>     /* Value */
         },
         ...
    },
    "fldsmax": <long> /* Maximum number of custom fields (-1 for unlimited) */
}
```

## Messages

The flag of messages is 0x00000020.

After setting this flag, you can receive resource messages.

```json
{}
```

## GUID

The flag of GUID is 0x00000040.

```json
{
        "gd":<text>       /* Resource GUID */
}
```

## Administrative custom fields

The flag of administrative custom fields is 0x00000080.

```json
{
        "aflds": {     /* Administrative fields */
                 "<uint>": {   /* Sequence number */
                          "id": <uint>,       /* ID */
                          "n": <text>,       /* Name */
                          "v": <text>       /* Value */
                 },
                 ...
        },
        "afldsmax": <long>     /* Maximum number of administrative fields (-1 for unlimited) */
}
```

## Drivers

The flag of drivers is 0x00000080.

```json
{
        "drvrs": {
                <text>: {     /* Sequence number of the driver */
                         "id": <long>,       /* ID */
                         "n": <text>,        /* Name */
                         "c": <text>,        /* Code */
                         "pwd": <text>,      /* Password for mobile authorization */
                         "ej": <text>,       /* Extended JSON */
                         "jp": {             /* Custom fields */
                                    <text>: <text>,     /* Name: value */...
                         },
                         "ds": <text>,       /* Description */
                         "p": <text>,        /* Phone number */
                         "r": <double>,      /* Image aspect ratio */
                         "ck": <ushort>, /* Checksum (CRC16) */
                         "bu": <long>,       /* Assigned unit */
                         "pu": <long>,       /* Previous assigned unit
*/
                         "bt": <uint>,       /* Time of the last assignment/separation */
                         "pos": {            /* Location */
                                    "y": <double>,      /* Latitude */
                                    "x": <double>       /* Longitude */
                         },
                         "infr": {           /* Parameters for analyzing the driver's work and rest infringements (AETR) */
                                    "a": <uint>,      /* Current activity
*/
                                    "t": <uint>,      /* Start time of the current activity */
                                    "ud": <uint>,     /* Uninterrupted driving duration before the current activity */
                                    "ur": <uint>,     /* Uninterrupted re
```

st duration before the current activity */

```json
"uil": <uint>, /* Allowed duration
```

of uninterrupted driving */

```json
"uim": <uint>, /* Maximum uninterr
```

upted driving duration for a minor infringement */

```json
"uis": <uint>, /* Maximum uninterr
```

upted driving duration for a serious infringement. If exceeded, th
e infringement is classified as very serious. */

```json
"uir": <uint>, /* Required rest du
```

ration */

```json
"ddt": <uint>, /* Daily driving ti
```

me before the current activity */

```json
"ddc": <uint>, /* Number of times
```

daily driving can be prolonged this week */

```json
"ddil": <uint>,/* Allowed duration
```

of daily driving */

```json
"ddim": <uint>,/* Maximum daily dr
```

iving duration for a minor infringement */

```json
"ddis": <uint>,/* Maximum daily dr
```

iving duration for a serious infringement. If exceeded, the infrin
gement is classified as very serious. */

```json
"wdt": <uint>, /* Weekly driving d
```

uration before the current activity */

```json
"wdil": <uint>,/* Allowed duration
```

of weekly driving */

```json
"wdim": <uint>,/* Maximum weekly d
```

riving duration for a minor infringement */

```json
"wdis": <uint>,/* Maximum weekly d
```

riving duration for a serious infringement. If exceeded, the infri
ngement is classified as very serious. */

```json
"twdt": <uint>,/* Biweekly driving
```

duration before the current activity */

```json
"twdil": <uint>,/* Allowed biweekl
```

y driving duration */

```json
"twdim": <uint>,/* Maximum biweekl
```

y driving duration for a minor infringement */

```json
"twdis": <uint>,/* Maximum biweekl
```

y driving duration for a serious infringement. If exceeded, the in
fringement is classified as very serious. */

```json
                             "drt": <uint>,     /* Previous daily

rest duration*/
                                     "drd": <uint>,      /* Required dailyrest duration */
                                     "dril": <uint>, /* Time before which daily rest should occur */
                                     "drim": <uint>, /* Time before which the infringement is classified as minor */
                                     "dris": <uint>, /* Time before which the infringement is classified as serious. If exceeded, the infringement is classified as very serious. */
                                     "wrt": <uint>,      /* Previous weeklyrest duration*/
                                     "wrd": <uint>,      /* Required weeklyrest duration */
                                     "wril": <uint>, /* Time before which weekly rest should occur */
                                     "wrim": <uint>, /* Time before which the infringement is classified as minor */
                                     "wris": <uint>      /* Time before which the infringement is classified as serious If exceeded, the infringement is classified as very serious. */
                           }
                   },
                   ...
        },
        "drvrsmax": <long>       /* Maximum number of drivers (-1 for unlimited) */
}
```

## Jobs

The flag of jobs is 0x00000200.

```json
{
        "ujb": {
                   "<text>": {   /* Sequence number of the job */
                           "id": <uint>,      /* ID */

                         "n": <text>,        /* Name */
                         "d": <text>,        /* Description */
                         "m": <uint>,        /* Maximum allowed number ofexecutions */
                         "st": {     /* State */
                                    "e": <uint>,    /* Active (1) / Inactive (0) */
                                    "c": <uint>,    /* Number of executions */
                                    "l": <uint>    /* Last execution time (UTC) */
                         },
                         "act": <text>       /* Action type */
                 },
                 ...
          },
          "ujbmax": <long>    /* Maximum number of jobs (-1 for unlimited) */
}
```

Action types are described in the get_job_data chapter.

## Notifications

The flag of notifications is 0x00000400.

```json
{
          "unf": {
                 "<text>": {    /* Sequence number of the notification */
                         "id": <long>,         /* Notification ID */
                         "n": <text>,          /* Name */
                         "ta": <uint>,         /* Activation time */
                         "td": <uint>,         /* Deactivation time */
                         "ma": <uint>,         /* Maximum number of triggers (0 for unlimited) */
                         "fl": <uint>,         /* Notification types */

                           "ac": <uint>,     /* Number of triggers */
                           "un": [<long>],   /* Array of unit IDs */
                           "act": [<text>], /* List of actions */
                           "trg": <text>,    /* Control type */
                           "crc": <long>     /* Checksum of the binaryview of the notification */
                   },
                   ...
          },
          "unfmax": <long>   /* Maximum number of notifications (-1 for unlimited) */
}
```

Action types, control types and notification flags are described in the
get_notification_data chapter.

## POIs

The flag of POIs is 0x00000800.

```json
{
          "poi": {
                   "<text>": {   /* Sequence number of POI */
                           "id": <long>,     /* POI ID */
                           "n": <text>,      /* Name */
                           "y": <double>,    /* Latitude */
                           "x": <double>,    /* Longitude */
                           "t": <double>,    /* Image aspect ratio */
                           "i": <short>,     /* Image checksum (CRC16)
*/
                           "e": <ushort>     /* POI checksum (CRC16)
*/
                   },
                   ...
          },
          "poimax": <long>   /* Maximum number of POIs (-1 for unlimited) */
```

}

## Geofences

The flag of geofences is 0x00001000.

{

```json
"zl": {
          "<text>": {   /* Sequence number of the geofence */
                  "n": <text>,        /* Name */
                  "d": <text>,        /* Description */
                  "id": <long>,       /* ID */
                  "f": <uint>,        /* Flags */
                  "t": <int>,         /* Type: 1 — line, 2 — pol
```

ygon, 3 — circle */

```json
"e": <ushort>,      /* Checksum (CRC16) */
"c": <uint>,        /* ARGB color */
"i": <ushort>,      /* Checksum of image (CRC1
```

6) */

```json
"ct": <uint>,       /* Creation time (Unix tim
```

estamp) */

```json
"mt": <uint>,       /* Last modification time
```

(Unix timestamp) */

```json
"b": {     /* Configuration for rendering geo
```

fences */

```json
"min_x": <double>,     /* Minimum lon
```

gitude */

```json
"min_y": <double>,     /* Minimum lat
```

itude */

```json
"max_x": <double>,     /* Maximum lon
```

gitude */

```json
"max_y": <double>,     /* Maximum lat
```

itude */

```json
"cen_x": <double>,     /* Longitude o
```

f the geofence center */

```json
"cen_y": <double>      /* Latitude of
```

the geofence center */

```json
                          }
                 },
                 ...
        },
        "zlmax": <long>       /* Maximum number of geofences (-1 for unlimited) */
}
```

Geofence flags are described in the get_zone_data chapter.

## Report templates

The flag of report templates is 0x00002000.

```json
{
        "rep": {
                 <text>: {     /* Sequence number of the template */
                          "id": <long>,       /* Template ID */
                          "n": <text>,        /* Template name */
                          "ct": <text>,       /* Template type */
                          "c": <ushort>       /* Checksum (CRC16) */
                 },
                 ...
        },
        "repmax": <long>      /* Maximum number of templates (-1 for unlimited) */
}
```

Template types are described in the get_report_data chapter.

List of units to which drivers can be assigned
automatically

The flag of units to which drivers can be assigned automatically is
0x00004000.

```json
{
        "drvrun": [<long>]         /* Array of unit IDs */
}
```

## Driver groups

The flag of driver groups is 0x00008000.

```json
{
        "drvrsgr": {    /* Driver groups */
                 <text>: {   /* Sequence number of the group */
                          "id": <long>,     /* Group ID */
                          "n": <text>,      /* Group name */
                          "d": <text>,      /* Group description */
                          "drs": [<uint>]     /* Array of driver IDs */
                 },
                 ...
        },
        "drvrsgrmax": <long>    /* Maximum number of driver groups
(-1 for unlimited) */
}
```

## Trailers

The flag of the trailers is 0x00010000

```json
{
        "trlrs": {     /* Trailers */
                 <text>: {   /* Sequence number of the trailer */
                          "id": <long>,     /* Trailer ID */
                          "n": <text>,      /* Trailer name */
                          "c": <text>,      /* Trailer code */

                         "ej": <text>,      /* Extended JSON */
                         "jp": {    /* Custom fields */
                                   <text>: <text>,     /* Name: value */...
                         },
                         "ds": <text>,      /* Description */
                         "p": <text>,        /* Phone number */
                         "r": <double>,      /* Image aspect ratio */
                         "ck": <short>,      /* Image checksum */
                         "bu": <long>,      /* Assigned unit */
                         "pu": <long>,      /* Previous assigned unit
*/
                         "bt": <uint>,      /* Last assignment/sepatation time */
                         "pos": {     /* Location */
                                   "y": <double>,    /* Latitude */
                                   "x": <double>     /* Longitude */
                         }
                 }
        },
        "trlrsmax": <long>     /* Maximum number of trailers (-1 forunlimited) */
}
```

## Trailer groups

The flag of trailer groups is 0x00020000.

```json
{
        "trlrsgr": {   /* Trailer groups */
                 <text>: {    /* Sequence number of the group */
                         "id": <long>,      /* Group ID */
                         "n": <text>,        /* Group name */
                         "d": <text>,        /* Group description */
                         "drs": [<uint>]      /* Array of trailer IDs
*/
                 }

          },
          "trlrsgrmax": <long>   /* Maximum number of trailer groups
(-1 for unlimited) */
}
```

List of units to which trailers can be assigned
automatically

The flag of units to which drivers can be assigned automatically
is 0x00040000.

```json
{
          "trlrun": [<long>]       /* Array of unit IDs */
}
```

## Orders

The flag of orders is 0x00080000.

```json
{
    "orders": {
        "<uint>": {       /* Order number, the same as in the "id"
parameter */
          "id": <uint>,   /* Order ID within the resource */
          "n": <text>,     /* Order name */
          "p": {          /* User-defined object content */...
          },
          "f": <bool>,     /* Order flags: 1 - marked as completed if at least one message within the order area has zero speed */
          "tf": <uint>,   /* Lower bound of the order completion time */
          "tt": <uint>,   /* Upper bound of order completion time
```

*/

```json
"uid": <uint>,    /* Unique ID (used as a unique key in the
```

order history) */

```json
          "r": <uint>,      /* Order point radius */
          "y": <double>,    /* Order point latitude */
          "x": <double>,    /* Order point longitude */
          "u": <long>,      /* Unit ID */
          "s": <uint>,      /* Order status:
                              0 - inactive (no unit assigned)
                              1 - active (unit assigned)
                              2 - completed in time
                              3 - completed overdue
                              4 - cancelled (not used) */
          "st": <uint>      /* Last status modification time */
     },
     ...
}
```

}

## Geofences groups

The flag of geofence groups is 0x00100000.

{

```json
"zg": {      /* Geofence groups */
     "<text>": {    /* Group sequence number */
          "id": <long>,      /* Group ID */
          "n": <text>,       /* Name */
          "d": <text>,       /* Description */
          "drs": [<uint>]    /* Array of geofence IDs */
     },
     ...
},
"zgmax": <long>      /* Maximum number of geofence groups (-1 for u
```

nlimited) */
}

## Tags (passengers)

The flag of tags (passengers) is 0x00200000.

```json
{
     "item": {
         "tags": {
              "<uint>": {                   /* Tag ID */
                    "id": <uint>,           /* Tag ID */
                    "n": <text>,            /* Tag name */
                    "c": <text>,            /* Tag code */
                    "jp": {                 /* Custom fields (key:value) */
                         "<text>": <text>
                    },
                    "r": <double>,          /* Image aspect ratio */
                    "ck": <ushort>,         /* Checksum (CRC16) */
                    "bu": <long>,           /* Assigned unit */
                    "pu": <long>,           /* Previously assigned unit */
                    "bt": <uint>,           /* Last assignment/separation time
*/
                    "tz": <int>,            /* Time zone */
                    "pos": {                /* Location */
                         "y": <double>,     /* Latitude */
                         "x": <double>      /* Longitude */
                    }
              },
              ...
         },
         "tagsmax": -1          /* Maximum number of tags (-1 for unlimited)
*/
     }
}
```

List of units to which tags can be assigned
automatically

The flag of units to which tags (passengers) can be assigned automatically
is 0x00400000.

```json
{
    "tagrun":[<long>]     /* Array of unit IDs */
}
```

## Tags groups (passenger groups)

The flag of tag groups (passenger groups) is 0x00800000.

```json
{
    "tagsgr": {
        <long>: {                           /* Group ID */
              "id": <long>,        /* Group ID */
              "n": <text>,         /* Group name */
              "d": <text>,         /* Description */
              "tgs": [<uint>]      /* Array of tag IDs */
        },
        ...
    }
    "tagsgrmax": -1                /* Maximum number of groups */
}
```
