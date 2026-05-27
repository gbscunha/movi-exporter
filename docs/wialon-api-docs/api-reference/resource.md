# resource

This section describes the methods that can be applied to the following
resource subitems: geofences, drivers, trailers, notifications, and jobs. The

reports also refer to the resources, but they are described separately in the
report section. The creation of the resources is described here.

Some methods related to resources are not described in the Wialon Help
Center yet. Please refer to the previous version of the API documentation to
get information about the following methods:

## bind_unit_driver

The bind_unit_driver function is used to assign drivers to units or to
separate them from units.

```http
svc=resource/bind_unit_driver&params={"resourceId":<long>,

"unitId":<long>,

"driverId":<long>,

"time":<uint>,

"mode":<bool>

}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| unitId | Unit ID. |
| driverId | Driver ID. |
| time | Time (0 — current time). |
| Modes: |  |
| mode | 1/true — assign; |
| 0/false — separate. |  |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7         (ADF_ACL_AVL_RES_EDIT_DRIVERS) or failed to fetch the unit with the desired ACL (ADF_ACL_ITEM_VIEW). |
| 6 | Failed to assign the driver. |
| Failed to fetch the driver with the desired driverId or wrong | 4 input parameters. |

## Request examples

Sent request for assigning a driver:

```http
svc=resource/bind_unit_driver&params={"resourceId":930849,"driverId":2,"time":0,"unitId":24675341,"mode":1}
```

Returned result:

```json
{ }
```

Sent request for separating a driver:

```http
svc=resource/bind_unit_driver&params={"resourceId":930849,"driverId":2,"time":0,"unitId":24675341,"mode":0}
```

Returned result:

```json
{ }
```

Assign driver on Feb 07 2022 07:07:00:

```http
svc=resource/bind_unit_driver&params={"resourceId":930849, "driver
Id":17, "time":1644217620, "unitId":22361100, "mode":1}
```

Returned result:

```json
{ }
```

Separate driver on Feb 07 2022 09:08:00:

```http
svc=resource/bind_unit_driver&params={"resourceId":930849,"driverId":17,"time":1644224880,"unitId":22361100,"mode":0}
```

Returned result:

```json
{ }
```

You also can merge these two requests into one using core/batch:

```http
svc=core/batch&params={"params":[{"svc":"resource/bind_unit_driver","params":{"resourceId":930849,"driverId":17,"time":164421762
0,"unitId":22361100,"mode":true}},{"svc":"resource/bind_unit_driver","params":{"resourceId":930849,"driverId":17,"time":164422488
0,"unitId":22361100,"mode":false}}],"flags":0}
```

For the returned result, see the response section for the batch function.

## bind_unit_tag

The bind_unit_tag function is used to bind a tag to a unit or to unbind it
manually. The tags are used when assigning or separating passengers.

It is recommended to assign passengers automatically.

```http
svc=resource/bind_unit_tag&params={"resourceId":<long>,

"unitId":<long>,

"tagId":<long>,

"time":<uint>,

"mode":<bool>

}
```

### Parameters

| Name | Description |
| --- | --- |
| d | resourceI Resource ID. |
| unitId | Unit ID. |
| tagId | Tag ID. |
| time | Time (0 — current time). Unix time value in GMT+0 time zone. |
| Modes: |  |
| mode             1/true — bind; | 0/false — unbind. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7         (ADF_ACL_AVL_RES_EDIT_TAGS) or failed to fetch the unit with the desired ACL (ADF_ACL_ITEM_VIEW). |
| 6 | Failed to bind the tag. |
| Failed to fetch the tag with the desired tagId or wrong input | 4 parameters. |

## bind_unit_trailer

The bind_unit_trailer function is used to assign trailers to units or to
separate them from units.

```http
svc=resource/bind_unit_trailer&params={"resourceId":<long>,

"unitId":<long>,

"trailerId":<long>,

"time":<uint>,

"mode":<bool>

}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| unitId | Unit ID. |
| trailerId | Trailer ID. |
| time | Time (0 — current time). |
| Modes: |  |
| mode                            1/true — assign; | 0/false — separate. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7           (ADF_ACL_AVL_RES_EDIT_TRAILERS) or failed to fetch the unit with the desired ACL (ADF_ACL_ITEM_VIEW). |
| 6 | Failed to assign the trailer. |
| Failed to fetch the trailer with the desired trailerId or wrong | 4 input parameters. |

## cleanup_driver_interval

The cleanup_driver_interval function is used to delete the records about
assigning a driver to a unit or separating it from a unit during a specified
time interval.

```http
svc=resource/cleanup_driver_interval&params={"resourceId":<long>,

"driverId":<long>,

"timeFrom":<uint>,

"timeTo":<uint>

}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| driverId | Driver ID. |
| timeFrom | The beginning of the interval. |
| timeTo | The end of the interval. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ACL_RES_EDIT_DRIVERS and ACL_ITEM_EXECUTE_REPORTS). |
| One of the following errors: |  |
| Failed to fetch the driver with the desired driverId. | If the end of the interval is after the time of the last 4            message received from the unit, all messages except the last one are deleted and the returned result contains the "forbidden delete the last message" text. Wrong input parameters. |
| 3 | Failed to fetch messages. |

## cleanup_trailer_interval

The cleanup_trailer_interval function is used to delete the records about
assigning a trailer to a unit or separating it from a unit during a specified
time interval.

```http
svc=resource/cleanup_trailer_interval&params={"resourceId":<long>,

"trailerId":<long>,

"timeFrom":<uint>,

"timeTo":<uint>

}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| trailerId | Trailer ID. |
| timeFrom | The beginning of the interval. |
| timeTo | The end of the interval. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ACL_RES_EDIT_TRAILERS and ACL_ITEM_EXECUTE_REPORTS). |
| Failed to fetch the trailer with the desired trailerId or wrong | 4 input parameters. |
| 3 | Failed to fetch messages. |

## create_zone_by_track

The create_zone_by_track function is used to create geofences from
tracks.

svc=resource/create_zone_by_track&params={"layerName":"<text>",

"itemId":<uint>,

"unitId":<uint>,

"n":"<text>",

"c":<int>,

"w":<int>

}

### Parameters

| Name | Description |
| --- | --- |
| layerName | Track layer name. |
| itemId | Resource ID. |
| unitId | Unit ID. |
| n | Geofence name. |
| c | Colour (ARGB). Optional. The default value is 0x009933. |
| w | Line thickness. Optional. The default value is 100. |

## Returned result

```json
{
        "all_zones":<uint>,         /* the number of new geofences (the maximum number of points in one geofence is 10000) */
        "created_zone":<uint>       /* the number of created geofences
*/
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_ZONES). |
| 6 | Failed to fetch the renderer or no geofences created. |
| 4 | Failed to get messages or wrong input parameters. |

## driver_status

The driver_status function is used to check the status of a unit that has
an assigned driver.

```http
svc=resource/driver_status&params={"phoneNumber":"<text>",

"password":"<text>",

"app":"<text>",

"fl":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| mber | phoneNu The driver's prone number. |
| password | The mobile key. The field can't be empty. |
| app | The application name for the generated token. The field is optional. The default value is "Wialon Logistics". |
| fl | Optional flags: |
| 1 — returns token; |  |
| 2 — returns the status even if the driver is not | assigned to a unit. |

## Returned result

{
"drv":{                            /* driver params */

```json
"rid":<uint>,     /* resource ID */
"id":"<text>",     /* driver ID */
"nm":"<text>"}     /* driver name */
```

},
"un":{                             /* unit params */

```json
"nm":"<text>",
"cls":<uint>,
"id":<uint>,
"mu":<uint>,
"ct":<uint>,
"ftp":{ ... },
"pos":{ ... },
"lmsg":{ ... },
"uri":"<text>",
"ugi":<uint>,
"uacl":<int>
```

},
"uh":"<text>",                     /* encrypted device information (f
or WiaTag) */
"ul":"<text>",                     /* encrypted phone number */
"h":"<text>"                       /* token */
}

You can find the description of the parameters and the
entry for “pos”, “lmsg” here.

Possible error codes:

| Code | Description |
| --- | --- |
| 8 | Wrong password or phone number. |
| Failed to fetch unit, unit account, user creator or driver | 7 plugin. |
| 6 | Failed to find the first assigned driver or undefined error. |
| One of the following errors in the request: |  |
| No phoneNumber or password field. |  |
| 4            Empty password field. | Item with the desired phoneNumber not found. |
| Wrong input parameters. |  |

## get_driver_bindings

The get_driver_bindings function is used to receive information about
driver assignments and separations during a specified time interval.

```http
svc=resource/get_driver_bindings&params={"resourceId":<long>,

"unitId":<long>,

"driverId":<long>,

"timeFrom":<uint>,
```

"timeTo":<uint>}

You can't execute this request simultaneously with the
following requests:

report/exec_report;
report/export_result;
report/get_result_chart;
report/get_result_map;
messages/load_interval;
render/create_messages_layer;
unit/get_trips;
resource/get_trailer_bindings;
the requests from the exchange section;
account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| unitId | Unit ID (0 — all units). |
| driverId | Driver ID (0 — all drivers). |
| timeFrom | The beginning of the interval. |
| timeTo | The end of the interval. |

## Returned result

```json
{
        "<text>":[{                                 /* driver ID */
                                    "t":<unit>,     /* time of assignment/separation */
                                    "u":<long>      /* unit ID in caseof assignment, 0 in case of separation */
                          },
                          ...],
                 ...
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | (ADF_ACL_ITEM_EXECUTE_REPORTS and 7 ADF_ACL_AVL_RES_VIEW_DRIVERS), or failed to fetch the unit with the desired ACL (ADF_ACL_ITEM_VIEW). |
| 4 | Failed to fetch the list of drivers or wrong input parameters. |

## get_email_template

The get_email_template function is used to get an email template
(subject and body).

```http
svc=resource/get_email_template&params={"resourceId":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |

## Returned result

```json
{
        "subject":"<text>",
        "body":"<text>",
        "flags":<int>
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_ITEM_VIEW_PROPERTIES). |
| 4 | Wrong input parameters. |

## get_job_data

The get_job_data function is used to receive detailed information about
the specified jobs.

```http
svc=resource/get_job_data&params={"itemId":<long>,

"col":[<long>]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| The array of job IDs. | col            The field is optional. If it is not present, the function is executed for all the jobs. |

## Returned result

```json
[
          {
                     "id":<long>,                         /* job ID */
                     "n":"<text>",                                 /* name */
                     "d":"<text>",                                 /* description */
                     "r":"<text>",                                 /* execution type (see below) */
                     "at":<uint>,                         /* activation time
*/
                     "m":<uint>,                                   /* maximum
```

executions limit, 0 — unlimited */

```json
"fl":<uint>,                           /* delete the job when the
```

maximum executions limit is reached, 1 — yes */

```json
"tz":<int>,                                  /* time zo
```

ne, sec */

```json
"l":"<text>",                                /* languag
```

e used for the job */

```json
"st":{                                       /* state
```

*/

```json
"e":<int>,                         /* enable
```

d/disabled */

```json
"c":<uint>,                        /* executi
```

ons count */

```json
"l":<uint>                         /* last ex
```

ecution time */

```json
},
"sch":{                                      /* time li
```

mitation */

```json
"f1":<uint>,               /* the beginning o
```

f the interval 1 */

```json
"f2":<uint>,               /* the beginning o
```

f the interval 2 */

```json
"t1":<uint>,               /* the end of the
```

interval 1 */

```json
"t2":<uint>,               /* the end of the
```

interval 2 */

```json
"m":<uint>,                        /* the mas
```

k of days of month */

```json
"y":<uint>,                        /* the mas
```

k of months */

```json
"w":<uint>,                        /* the mas
```

k of days of week */

```json
"fl":<int>                         /* schedul
```

e flags */

```json
},
"act":{                                      /* actions
```

(see the list of actions) */

```json
"t":"<text>",                      /* type */
"p":{                              /* paramet
```

ers */

"<text>":"<text>",         /* name: v
alue */
...

```json
                          }
                 },
                 "ct":<uint>,                         /* creation time
*/
                 "mt":<uint>                          /* last modification time */
          }
]
```

There are two available types of execution:

Form a detailed list of executions according to a precise schedule. In this
case, the format of the r field is “1 …”, where after 1, the execution time
should be indicated. If there should be several executions, use a space
to separate their time. The time format is “hours:minutes” or “hours”.
Set an interval between executions. If there should be a definite interval
between job executions, the format of the r field is “2 …”, where after 2,
indicate in Unix format the interval after which the job must be executed
iteratively.

## Action types

The following types of actions are available for jobs:

Send a command to units;
Change access to units;

Send a report by email;
Send fuel information by email or SMS;

Mileage counters;
Engine hours counters;

GPRS traffic counters.

## Send a command to units

```json
"act":{
          "t":"exec_unit_cmd",               /* action type */
          "p":{
                  "cmd_name":"<text>",              /* command name */
                  "cmd_type":"<text>",              /* command type */
                  "cmd_param":"<text>",             /* command parameter */
                  "link_type":"<text>",             /* link type */
                  "timeout":"<text>",               /* the time duringwhich the system will try to execute the command, s */
                  "units":"<text>"                           /* the list of IDs of units/unit groups (separated by commas) */
          }
}
```

You can find the list of available command types here.

## Change access to units

```json
"act":{
          "t":"change_access_user",          /* action type */
          "p":{
                  "acl_bits":"<text>",              /* 1 — set bit, 0
— remove bit */
                  "acl_mask":"<text>",              /* the mask of bits to be changed */
                  "units":"<text>",                          /* the list of IDs of units/unit groups (separated by commas) */
                  "users":"<text>"                           /* the list of IDs of users (separated by commas) */
          }
}
```

## Send a report by email

```json
"act":{
          "t":"send_email_report",             /* action type */
          "p":{
                  "email_to":"<text>",                /* email addressesseparated by commas */
                  "file_type":"<text>",               /* file format */
                  "flags":"<text>",                            /* interval flags */
                  "params":"<text>",                  /* report configuration (XML) */
                  "report_guid":"<text>", /* resource ID */
                  "report_id":"<text>",               /* report template
ID */
                  "report_objects":"<text>",/* the list of unit IDsseparated by commas */
                  "time_from":"<text>",               /* the beginning of time interval */
                  "time_to":"<text>"                  /* the end of timeinterval */
          }
}
```

The interval flags are described here.

File formats (ZIP archive content):

1 — HTML;
2 — PDF;

4 — XLS;
8 — XLSX;

16 — XML;
32 — CSV.

## Send fuel information by email or SMS

```json
"act":{
          "t":"send_email_sms_fuel",           /* action type */
          "p":{
                   "email_to":"<text>",               /* email addressesseparated by commas */
                   "flags":"<text>",                           /* flags
(see below) */
                   "phone_to":"<text>",               /* phone numbers
*/
                   "time_offset":"<text>", /* time offset, min */
                   "units":"<text>"                            /* the list of IDs of units/unit groups (separated by commas) */
          }
}
```

Flags:

Value              Description

0x01               Separate message for each unit.

0x02               All units in one message.

0x04               Event type: fuel filling.

0x08               Event type: fuel drain.

0x10               Event type: fuel level.

0x20               Delivery method: email.

0x40               Delivery method: SMS.

## Mileage counters

"act":{

```json
"t":"reset_unit_mileage_counter",        /* action type */
"p":{
        "param_name":"<text>",           /* parameter name;
```

if it's empty, the counter value isn't stored as parameter of unit
data message */

```json
"skip_reset":"<text>",           /* set new value f
```

or the mileage counter (0 — yes, 1 — no) */

```json
"store_mileage":"<text>",                /* store c
```

ounter value in unit history */

```json
"units":"<text>",                                    /*
```

list of IDs of units/unit groups (separated by commas) */

```json
"value_mileage":"<text>"                 /* new val
```

ue of mileage counter, m */

```
}
```

}

## Engine hours counters

"act":{

```json
"t":"reset_unit_engine_hours_counter",   /* action type */
"p":{
        "param_name":"<text>",           /* parameter name;
```

if it's empty, the counter value isn't stored as parameter of unit
data message */

```json
"skip_reset":"<text>",           /* set new value f
```

or the engine hours (0 — yes, 1 — no) */

```json
"store_eh":"<text>",                     /* store c
```

ounter value in unit history */

```json
"units":"<text>",                                    /*
```

list of IDs of units/unit groups (separated by commas) */

```json
"value_eh":"<text>"                      /* new val
```

ue of engine hours, s */

```
          }
}
```

## GPRS traffic counters

```json
"act":{
          "t":"reset_unit_bytes_counter", /* action type */
          "p":{
                  "reset_bytes":"<text>",           /* reset counter value (1 — yes, 2 — no) */
                  "store_bytes":"<text>",           /* store counter value in unit history (1 — yes, 0 — no) */
                  "units":"<text>"                                        /*list of IDs of units/unit groups (separated by commas) */
          }
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_VIEW_JOBS). |
| 4 | Wrong input parameters. |

## get_notification_data

The get_notification_data function is used to get detailed information
about specified notifications.

```http
svc=resource/get_notification_data&params={"itemId":<long>,

"col":[<long>]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| The array of notification IDs. | col          The field is optional. If it is not present, the function is executed for all the notifications. |

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
[
        {
                    "id":<long>,       /* notification ID */
                    "n":"<text>",      /* name */
                    "txt":"<text>", /* notification text */
                    "ta":<uint>,       /* activation time (Unix format)
*/
                    "td":<uint>,       /* deactivation time (Unix format)
*/
                    "ma":<uint>,       /* maximum number of alarms (0 — unlimited) */
                    "mmtd":<uint>,     /* maximum time interval between messages, s */
                    "cdt":<uint>,      /* timeout of alarm, sec */

             "mast":<uint>,     /* minimum duration of the alarm s
```

tate, s */

```json
"mpst":<uint>,     /* minimum duration of previous st
```

ate, s */

```json
"cp":<uint>,       /* period of control relative to c
```

urrent time, s */

```json
"fl":<uint>,       /* notification flags (see below)
```

*/

```json
"tz":<uint>,       /* time zone */
"la":"<text>",     /* user language (two-letter code)
```

*/

```json
"ac":<uint>,       /* alarms count */
"d":"<text>",                /* notification descriptio
```

n */

```json
"sch":{            /* time limitation */
          "f1":<uint>,       /* the beginning of the in
```

terval 1 (minutes from midnight) */

```json
"f2":<uint>,       /* the beginning of the in
```

terval 2 (minutes from midnight) */

```json
"t1":<uint>,       /* the end of the interval
```

1 (minutes from midnight) */

```json
"t2":<uint>,       /* the end of the interval
```

2 (minutes from midnight) */

```json
"m":<uint>,        /* the mask of days of mon
```

th [1: 2||0, 31: 2||30] */

```json
"y":<uint>,        /* the mask of months [Ja
```

n: 2||0, Dec: 2||11] */

```json
"w":<uint>,        /* the mask of days of wee
```

k [Mon: 2||0, Sun: 2||6] */

```json
          "fl":<int>         /* schedule flags */
},
"ctrl_sch":{       /* the schedule of maximum alarms
```

count intervals */

```json
"f1":<uint>,       /* the beginning of the in
```

terval 1 (minutes from midnight) */

```json
"f2":<uint>,       /* the beginning of the in
```

terval 2 (minutes from midnight) */

```json
"t1":<uint>,       /* the end of the interval
```

1 (minutes from midnight) */

```json
"t2":<uint>,       /* the end of the interval
```

2 (minutes from midnight) */

```json
"m":<uint>,         /* the mask of days of mon
```

th [1: 2||0, 31: 2||30] */

```json
"y":<uint>,         /* the mask of months [Ja
```

n: 2||0, Dec: 2||11] */

```json
"w":<uint>          /* the mask of days of wee
```

k [Mon: 2||0, Sun: 2||6] */

```json
          "fl":<int> /* schedule flags */
},
"un":[<long>],      /* array of IDs of units/unit grou
```

ps */

```json
"act":[                       /* actions */
          {
                    "t":"<text>",               /* action
```

type (see below) */

```json
"p":{                       /* paramet
```

ers */

```json
"blink": "<text>",             /*
```

mini-map blinking when triggered */

```json
"color": "<text>",             /*
```

online notification colour */

```json
"url": "<text>",
```

/* URL address of the notification sound */
...

```json
                    },
                    ...
          }
],
"trg":{                       /* control */
          "t":"<text>",              /* control type (s
```

ee below) */

```json
"p":{                      /* parameters */
          "<text>":"<text>",                       /*
```

parameter name: value */
...

```json
                       }
             },
             "ct":<uint>,              /* creation time */
             "mt":<uint>               /* last modification time */
      }

]
```

Notification flags:

| Flag | Description |
| --- | --- |
| 0x0 | Notification triggers for the first message. |
| 0x1 | Notification triggers for every message. |
| 0x2 | Notification is disabled. |
| For notifications of the Off time control type, the value of | the mast parameter specified in seconds must correspond to the value of the min_idle_time parameter specified in minutes. Thus, if you want the notification to be triggered after 10 minutes of off time, specify 10 for min_idle_time and 600 for mast. |
| If the request fails, an error code is returned. |  |

## Action types

The following types of actions are available for notifications:

Notify by email;
Notify by SMS;

Display online notification in a pop-up window;
Send mobile notification;

Send a request;
Send notification to Telegram;

Register event for unit;
Send a command;

Change access to units;

Set counter value;
Store counter value as a parameter;

Register unit status;
Add or remove units from groups;
Send a report by email;
Create a ride;
Separate driver;
Separate trailer;
Create task.

## Notify by email

{

```json
"t":"email",                  /* action type */
"p":{
            "email_to":"<text>",      /* email address */
            "html":"<text>",                  /* use HTML tags:
```

0 — no, 1 — yes */

```json
"img_attach":"<text>",    /* attach image from notif
```

ication: 1 — yes, 0 — no */

```json
            "subj":"<text>"           /* text of message */
}
```

}

## Notify by SMS

{

```json
"t":"sms",                    /* action type */
"p":{
            "phones":"<text>"                 /* list of phone n
```

umbers (separated by semicolons) */

```
}
```

}

## Display online notification in a pop-up window

{

```json
"t":"message",             /* action type */
"p":{
        "color":"<text>",                   /* notification co
```

lour */

```json
"name":"<text>",                    /* notification na
```

me */

```json
"url":"<text>"               /* URL address of the noti
```

fication sound */

```
}
```

}

## Send mobile notification

{

```json
"t":"mobile_apps",                   /* action type */
"p":{
        "apps":"{\"<text>\":[        /* mobile app name */
                           <uint>    /* user ID */
        ]}"
}
```

}

## Send a request

{

```json
"t":"push_messages",      /* action type */
"p":{
        "url":"<text>",            /* server name (port may b
```

e defined), start it with "http(s)" */

```json
"get":<bool>               /* request type: 1 — GET,
```

0 — POST */

```
}
```

}

## Send notification to Telegram

{

```json
"t":"messenger_messages",          /* action type */
"p":{
        "chat_id":"<text>",               /* channel ID in T
```

elegram */

```json
"token":"<text>"                  /* user token in T
```

elegram */

```
}
```

}

## Register event for unit

{

```json
"t":"event",              /* action type */
"p":{
        "flags":"<text>"                  /* register as: 0
```

— event, 1 — violation */

```
}
```

}

## Send a command

```json
{
         "t":"exec_cmd",          /* action type */
         "p":{
                 "cmd_type":"<text>",       /* command type */
                 "link":"<text>",                  /* link type */
                 "name":"<text>",                  /* command name */
                 "param":"<text>"                  /* parameters */
         }
}
```

You can find the list of available types of methods here.

## Change access to units

```json
{
         "t":"user_access",       /* action type */
         "p":{
                 "acl_bits":"<text>",       /* 1 — set bit, 0 — removebit */
                 "acl_mask":"<text>",       /* mask of bits which mustbe changed */
                 "units":"<text>",                 /* list of unit IDs (separated by commas) */
                 "users":"<text>"                  /* list of user IDs (separated by commas) */
         }
}
```

## Set counter value

```json
{
         "t":"counter",             /* action type */
         "p":{
                   "engine_hours":"<text>",          /* engine hours counter value */
                   "flags":"<text>",                 /* counter flags
(see below) */
                   "mileage":"<text>",        /* mileage counter value
*/
                   "traffic":"<text>"         /* GPRS traffic counter value */
         }
}
```

Counter flags:

| Flag | Description |
| --- | --- |
| 1 | Set mileage counter value. |
| 2 | Set engine hours counter value. |
| 4 | Set GPRS traffic counter value. |

## Store counter value as a parameter

```json
{
         "t":"store_counter",                 /* action type */
         "p":{
                   "engine_hours":"<text>",                   /* name ofparameter for engine hours counter */
                   "flags":"<text>",                          /* flags
(see below) */
                   "mileage":"<text>"                /* name of paramet

er for mileage counter */
        }
}
```

Flags:

| Flag | Description |
| --- | --- |
| 1 | Store mileage counter value as a parameter. |
| 2 | Store engine hours counter value as a parameter. |

## Register unit status

```json
{
        "t":"status",              /* action type */
        "p":{
                   "ui_text":"<text>"        /* status */
        }
}
```

## Add or remove units from groups

```json
{
        "t":"group_manipulation",            /* action type */
        "p":{
                   "add_to":"<text>",               /* add to specified groups */
                   "remove_from":"<text>"           /* remove from specified groups */
        }

}
```

## Send a report by email

```json
{
         "t":"email_report",        /* action type */
         "p":{
                   "email_to":"<text>",             /* email address
*/
                   "file_type":"<text>",            /* file format (see below) */
                   "flags":"<text>",                        /* interval flags */
                   "params":"<text>",               /* report configuration (XML) */
                   "report_guid":"<text>",          /* resource ID */
                   "report_id":"<text>",            /* template ID */
                   "report_object_guid":"<text>",   /* ID of item forreport */
                   "report_object_id":"<text>",     /* ID of subitem
(0 — if report executed for item) */
                   "time_from":"<text>",            /* the beginning of the time interval */
                   "time_to":"<text>"               /* the end of thetime interval */
         }
}
```

Interval flags are described here.

File formats:

1 — HTML;
2 — PDF;

4 — XLS;
8 — XLSX;

16 — XML;
32 — CSV.

## Create a ride

```json
{
        "t":"route_control",     /* action type */
        "p":{
                 "description":"<text>", /* description */
                 "expiration":"<text>",    /* expiration date */
                 "flags":"<text>",                /* ride flags */
                 "name":"<text>",                 /* name */
                 "route":"<text>",                /* route ID */
                 "schedule":"<text>"       /* schedule ID */
        }
}
```

Ride flags are described here.

## Separate driver

```json
{
        "t":"drivers_reset",     /* action type */
        "p":{}
}
```

## Separate trailer

```json
{
         "t":"trailers_reset",     /* action type */
         "p":{}
}
```

## Create task

```json
{
         "t": "create_task",       /* action type */
         "p": {
         "task_priority": "<int>", /* task priority */
         "task_assignee": "<int>" /* ID of the user to whom the task is assigned */
         }
}
```

## Control types

The following control types are available for notifications:

Geofence;
Address;
Speed;

Alarm (SOS);

Digital input;
Parameter in a message;

Sensor value;
Connection loss;

Off time;
SMS;

Interposition of units;

Excess of messages;
Route progress;

Driver;
Trailer;
Maintenance;
Fuel filling or battery charge;
Fuel drain
Health check status
Combination of several conditions

## Geofence

"trg":{

```json
"t":"geozone",            /* control type */
"p":{
        "sensor_type":"<text>",           /* sensor type */
        "sensor_name_mask":"<text>",      /* sensor name mas
```

k */

```json
"lower_bound":<uint>,             /* sensor value fr
```

om */

```json
"upper_bound":<uint>,             /* sensor value to
```

*/

```json
"prev_msg_diff":<uint>,           /* this flag allow
```

s forming boundaries for the current value according to the previo
us value(prev) in the following way: [prev+lower_bound ; prev+uppe
r_bound]; so boundaries for the current value are always relative
to the previous value; 0 — disable the option, 1 — enable the opti
on */

```json
"merge":<uint>,                   /* similar sensor
```

s: 0 — calculate separately, 1 — sum up values */

```json
"reversed":<uint>,                /* trigger: 0 — in
```

the specified range, 1 — out of the specified range */

```json
"geozone_ids":"<text>",           /* list of geofenc
```

e references separated by commas in format propID:createTime (for
geofences from the same resource as the notification) or itemId_pr
opId:createTime (for geofences from a different resource). For exa

mple, to reference a geofence with ID 15 created on 2024-01-15 at
10:30:00 UTC (timestamp: `1705315800`), specify "15:1705315800" */

```json
"type":<uint>,                     /* control type: 0
```

— control entries to a geofence, 1 — control exits from a geofence
*/

```json
"min_speed":<uint>,                /* minimum speed,
```

km/h */

```json
"max_speed":<uint>,                /* maximum speed,
```

km/h */

```json
"include_lbs":<uint>,              /* process LBS mes
```

sages: 1 — yes, 0 — no */

```json
"lo":"<text>"                      /* logic operator
```

(optional): "AND", "OR" */

```
}
```

}

You can use the resource/get_zone_data method to retrieve geofence
properties.

## Address

"trg":{

```json
"t":"address",             /* control type */
"p":{
        "sensor_type":"<text>",            /* sensor type */
        "sensor_name_mask":"<text>",       /* sensor name mas
```

k */

```json
"lower_bound":<uint>,              /* sensor value fr
```

om */

```json
"upper_bound":<uint>,              /* sensor value to
```

*/

```json
"prev_msg_diff":<uint>,            /* this flag allow
```

s forming boundaries for the current value according to the previo
us value(prev) in the following way: [prev+lower_bound ; prev+uppe
r_bound]; so boundaries for the current value are always relative
to the previous value; 0 — disable the option, 1 — enable the opti
on */

```json
"merge":<uint>,                     /* similar sensor
```

s: 0 — calculate separately, 1 — sum up values */

```json
"reversed":<uint>,                  /* trigger: 0 — in
```

the specified range, 1 — out of the specified range */

```json
"radius":<uint>,                    /* trigger radius
```

*/

```json
"type":<uint>,                      /* control type: 0
```

— control in the address radius, 1 — control out of the address ra
dius */

```json
"min_speed":<uint>,                 /* minimum speed,
```

km/h */

```json
"max_speed":<uint>,                 /* maximum speed,
```

km/h */

```json
"country":"<text>",                 /* country */
"region":"<text>",                  /* region */
"city":"<text>",                             /* city */
"street":"<text>",                  /* street */
"house":"<text>",                            /* house
```

*/

```json
"include_lbs":<uint>                /* process LBS mes
```

sages: 1 — yes, 0 — no */

```
}
```

}

## Speed

"trg":{

```json
"t":"speed",               /* control type */
"p":{
        "lower_bound":"<text>", /* sensor value from */
        "max_speed":"<text>",        /* maximum speed, km/h */
        "merge":"<text>",                   /* similar sensor
```

s: 0 — calculate separately, 1 — sum up values */

```json
"min_speed":"<text>",        /* minimum speed, km/h */
"prev_msg_diff":"<text>", /* this flag allows form
```

ing boundaries for the current value according to the previous val
ue(prev) in the following way: [prev+lower_bound ; prev+upper_boun

d]; so boundaries for the current value are always relative to the
previous value; 0 — disable the option, 1 — enable the option */

```json
"reversed":"<text>",      /* trigger: 0 — in the spe
```

cified range, 1 — out of the specified range */

```json
"sensor_name_mask":"<text>",      /* sensor name mas
```

k */

```json
"sensor_type":"<text>", /* sensor type */
"upper_bound":"<text>"    /* sensor value to */
"driver":"<text>"         /* this flag allows taking
```

into account driver assignments: 1 — the notification will be trig
gered when no driver is assigned, 2 — it will be      triggered when t
here is an assigned driver, 0 — this flag will be ignored */

```
}
```

}

## Alarm (SOS)

"trg":{

```json
"t":"alarm",               /* control type */
"p":{}
```

}

## Digital input

"trg":{

```json
"t":"digital_input",       /* control type */
"p":{
         "input_index":"<text>", /* digital input (1-32) */
         "type":"<text>"                   /* control type: 0
```

— check for activation, 1 — check for deactivation */

```
}
```

}

## Parameter in a message

```json
"trg":{
          "t":"msg_param",          /* control type */
          "p":{
                  "kind":"<text>",                   /* parameter control type (see below) */
                  "lower_bound":"<text>", /* parameter value from */
                  "param":"<text>",                  /* parameter name
*/
                  "text_mask":"<text>",       /* text mask */
                  "type":"<text>",                   /* trigger: 0 — inthe specified range, 1 — out of the specified range */
                  "upper_bound":"<text>"      /* parameter value to */
          }
}
```

Parameter control types:

Type                Description

0                   Value range.

1                   Text mask.

2                   Parameter availability.

3                   Parameter lack.

## Sensor value

```json
"trg":{
          "t":"sensor_value",                 /* control type */

         "p":{
                  "lower_bound":"<text>",          /* sensor value fr
```

om */

```json
"merge":"<text>",                         /* similar
```

sensors: 0 — calculate separately, 1 — sum up values */

```json
"prev_msg_diff":"<text>",            /* this flag all
```

ows forming boundaries for the current value according to the prev
ious value(prev) in the following way: [prev+lower_bound ; prev+up
per_bound]; so boundaries for the current value are always relativ
e to the previous value; 0 — disable the option, 1 — enable the op
tion */

```json
"sensor_name_mask":"<text>",     /* sensor name mas
```

k */

```json
"sensor_type":"<text>",          /* sensor type */
"type":"<text>",                          /* trigge
```

r: 0 — in the specified range, 1 — out of the specified range */

```json
"upper_bound":"<text>"           /* sensor value to
```

*/

```
}
```

}

## Connection loss

"trg":{

```json
"t":"outage",            /* control type */
"p":{
         "time":"<text>",                 /* time interval,
```

s */

```json
"type":"<text>",                 /* control type: 0
```

— coordinates loss, 1 — connection loss */

```json
"include_lbs":<uint>,     /* process LBS messages: 1
```

— yes, 0 — no     */

```json
"check_restore":<uint>, /* notify when: 0 — connec
```

tion lost, 1 — connection lost and restored, 2 — connection restor
ed */

```json
"geozones_type":"<text>", /* control type: 0 — out
```

of geofence, 1 — in geofence */

```json
"geozones_list":"<text>"    /* list of geofence refe
```

rences separated by commas in format propID:createTime (for geofen
ces from the same resource as the notification) or itemId_propId:c
reateTime (for geofences from a different resource). For example,
to reference a geofence with ID 15 created on 2024-01-15 at 10:30:
00 UTC (timestamp: `1705315800`), specify "15:1705315800" */

```
}
```

}

## Off time

"trg":{

```json
"t":"speed",            /* control type */
"p":{
        "lower_bound":"<text>",          /* sensor value fr
```

om */

```json
"max_speed":"<text>",            /* maximum speed,
```

km/h */

```json
"merge":"<text>",                         /* similar
```

sensors: 0 — calculate separately, 1 — sum up values */

```json
"min_idle_time":"<text>",                 /* minimum
```

idle time, min */

```json
"min_speed":"<text>",            /* minimum speed,
```

km/h */

```json
"prev_msg_diff":"<text>",            /* this flag all
```

ows forming boundaries for the current value according to the prev
ious value(prev) in the following way: [prev+lower_bound ; prev+up
per_bound]; so boundaries for the current value are always relativ
e to the previous value; 0 — disable the option, 1 — enable the op
tion */

```json
"reversed":"<text>",             /* trigger: 0 — in
```

the specified range, 1 — out of the specified range */

```json
"sensor_name_mask":"<text>",     /* sensor name mas
```

k */

```json
"sensor_type":"<text>",          /* sensor type */
"upper_bound":"<text>",          /* sensor value to
```

*/

```json
                  "geozones_type":"<text>",         /* control type: 0
— out of geofence, 1 — in geofence */
                  "geozones_list":"<text>"          /* list of geofence references separated by commas in format propID:createTime (forgeofences from the same resource as the notification) or itemId_propId:createTime (for geofences from a different resource). For exa
mple, to reference a geofence with ID 15 created on 2024-01-15 at
10:30:00 UTC (timestamp: `1705315800`), specify "15:1705315800" */
          }
}
```

The value of the min_idle_time parameter specified in minutes must
correspond to the value of the mast parameter specified in seconds. Thus,
if you want the notification to be triggered after 10 minutes of off time,
specify 10 for min_idle_time and 600 for mast.

## SMS

```json
"trg":{
          "t":"sms",                /* control type */
          "p":{
                  "mask":"<text>"            /* SMS text mask */
          }
}
```

## Interposition of units

```json
"trg":{
          "t":"interposition",               /* control type */
          "p":{
                  "sensor_name_mask":"<text>",      /* sensor name mask */
                  "sensor_type":"<text>",           /* sensor type */
                  "lower_bound":"<text>",           /* sensor value fr
```

om */

```json
"upper_bound":"<text>"             /* sensor value to
```

*/

```json
"merge":"<text>",                           /* similar
```

sensors: 0 — calculate separately, 1 — sum up values */

```json
"max_speed":"<text>",              /* maximum speed,
```

km/h */

```json
"min_speed":"<text>",              /* minimum speed,
```

km/h */

```json
"reversed":"<text>",               /* trigger: 0 — in
```

the specified range, 1 — out of the specified range */

```json
"prev_msg_diff":"<text>",             /* this flag all
```

ows forming boundaries for the current value according to the prev
ious value(prev) in the following way: [prev+lower_bound ; prev+up
per_bound]; so boundaries for the current value are always relativ
e to the previous value; 0 — disable the option, 1 — enable the op
tion */

```json
"radius":"<text>",                 /* radius, m */
"type":"<text>",                            /* control
```

type: 0 — control approaching to units, 1 — control moving away fr
om units */

```json
"unit_guids":"<text>",             /* the list of con
```

trol unit IDs (separated by commas) */

```json
"include_lbs":<uint>,              /* process LBS mes
```

sages: 1 — yes, 0 — no */

```json
"lo":"<text>"                      /* logic operator
```

(optional): "AND", "OR" */

```
}
```

}

## Excess of messages

"trg":{

```json
"t":"msgs_counter",                 /* control type */
"p":{
        "flags":"<text>",                           /* message
```

type: 1 — data messages, 2 — SMS messages */

```json
                  "msgs_limit":"<text>",              /* limit of messages */
                  "time_offset":"<text>"              /* reset counter each (limit 24h), s */
          }
}
```

## Route progress

```json
"trg":{
          "t":"route_control",                 /* control type */
          "p":{
                  "mask":"<text>",                             /* route name mask */
                  "round_mask":"<text>",              /* ride name mask
*/
                  "schedule_mask":"<text>",                    /* schedule name mask */
                  "types":"<text>"                             /* route control types (separated by commas) */
          }
}
```

Route control types:

Type               Description

1                  Ride started.

2                  Ride finished.

4                  Ride aborted.

8                   Arrival at check point.

16                  Check point skipped.

32                  Departure from check point.

64                  Delay.

128                 Outrunning.

256                 Return to schedule.

## Driver

"trg":{

```json
"t":"driver",              /* control type */
"p":{
         "driver_code_mask":"<text>",      /* driver code mas
```

k */

```json
"flags":"<text>"                          /* control
```

type: 1 — driver assignment, 2 — driver separation */

```
}
```

}

## Trailer

"trg": {

```json
"t": "trailer",            /* control type */
"p": {
         "driver_code_mask": "<text>",     /* trailer code ma
```

sk */

```json
                  "flags": "<text>"                         /* control

type: 1 — trailer assignment, 2 — trailer separation */
           }
}
```

## Maintenance

```json
"trg":{
           "t":"service_intervals",              /* control type */
           "p":{
                    "days":"<text>",                             /* days interval */
                    "engine_hours":"<text>",                     /* enginehours interval, h */
                    "flags":"<text>",                            /* maintenance control flags (see below) */
                    "mask":"<text>",                             /* wildcard based mask */
                    "mileage":"<text>",                 /* mileage interval, km */
                    "val":"<text>"                      /* notify when: 1
— service term approaches, -1 — service term is expired */
           }
}
```

Maintenance control flags:

| Flag | Description |
| --- | --- |
| 0 | Control all service intervals. |
| 1 | Mileage interval. |
| 2 | Engine hours interval. |
| 4 | Days interval. |

## Fuel filling or battery charge

"trg":{

```json
"t":"fuel_filling",        /* control type */
"p":{
         "sensor_name_mask":"<text>",                          /*
```

sensor name mask */

```json
"geozones_type":<uint>,           /* geofence contro
```

l type: 0 — disabled or outside geofence, 1 — inside geofence */

```json
"geozones_list":"<text>",                             /*
```

list of geofence references separated by commas in format propID:c
reateTime (for geofences from the same resource as the notificatio
n) or itemId_propId:createTime (for geofences from a different res
ource). For example, to reference a geofence with ID 15 created on
2024-01-15 at 10:30:00 UTC (timestamp: `1705315800`), specify "15:
1705315800" */

```json
"realtime_only":<uint>,                   /* ignore
```

the recalculation of historical data: 0 — disable, 1 — enable */

```
}
```

}

## Fuel drain

"trg":{

```json
"t":"fuel_theft",          /* control type */
"p":{
         "sensor_name_mask":"<text>",                          /*
```

sensor name mask */

```json
"geozones_type":<uint>,           /* geofence contro
```

l type: 0 — disabled or outside geofence, 1 — inside geofence */

```json
"geozones_list":"<text>",                  /* list o
```

f geofence references separated by commas in format propID:createT

ime (for geofences from the same resource as the notification) or
itemId_propId:createTime (for geofences from a different resourc
e). For example, to reference a geofence with ID 15 created on 202
4-01-15 at 10:30:00 UTC (timestamp: `1705315800`), specify "15:170
5315800" */

```json
                 "realtime_only":<uint>,                        /* ignorethe recalculation of historical data: 0 — disable, 1 — enable */
        }
}
```

## Health check status

```json
"trg": {
        "t": "health_check",       /* Control type */
        "p": {
              "healthy": <uint>,     /* Shows if the device is healthy:
0 — no, 1 — yes */
              "unhealthy": <uint>,        /* Shows if the device is unhealthy: 0 — no, 1 — yes */
              "needAttention": <uint>,         /* Shows if the device is needs attention: 0 — no, 1 — yes */
              "triggerForEachIncident": <uint>         /* Trigger for eachincident: 0 — disabled, 1 — enabled */
        }
    }
```

## Combination of several conditions

This control type allows combining up to three notification conditions in a
single expression using logical operators (AND/OR).

```json
"trg": {
    "t": "expression",
    "p": {},
    "expression": "<text>",            // Text string defining the logic
```

al expression combining several conditions. Uses condition names c
onnected with "AND" or "OR" operators.

```json
"conditions": {                  // Parameters for each condition
```

in the expression. Keys are condition names from the expression, v
alues are objects with condition-specific parameters.
"<condition_name>": {
// Condition-specific parameters

```
     }
}
```

}

## Supported condition types

There are combinable and non-combinable condition types. Combinable
ones can be used with AND/OR operators (up to 3 conditions), whereas
non-combinable ones must be the only condition in the expression.

## Combinable conditions

Condition type         Description

speed                  Speed threshold violation.

idling                 Engine idling detection.

speed_gis              Speed limit violation according to GIS.

driver_unassigned      Driver separation from the unit.

address                Address-based trigger.

geozone_inside         Unit entering geofence.

geozone_outside        Unit leaving geofence.

Condition type        Description

interposition         Unit distance from other units.

Sensor value within or outside the specified
sensor_range
range.

sensor_change         Sensor value change.

alarm                 Alarm button activation.

msg_param             Parameter in a message.

digital_input         Digital input state.

## Non-combinable conditions

Condition type            Description

tag                       Passenger assignment to the unit.

msgs_counter              Message limit reached.

trailer                   Trailer assignment to the unit.

driver                    Driver assignment to the unit.

sms                       SMS reception.

Expression examples:

### "geozone_inside OR geozone_outside"

### "speed AND driver_unassigned"

### "address OR sensor_range"

If the same condition type is used multiple times, add an underscore and
number suffix:

### "geozone_inside_1 AND geozone_inside_2 AND speed"

## Condition parameters

Each condition in the conditions object has specific parameters depending
on its type.

## Speed

```json
{
    "speed": {
        "min_speed": 2,
        "max_speed": 10
    }
}
```

## Idling (off time)

```json
{
    "idling": {
        "min_speed": 2,
        "max_speed": 10,
        "min_idle_time": 5
    }
}
```

## Speed road limit

```json
{
    "speeding_gis": { # or speed_gis , old has speeding_gis

       "speeding_tolerance": "15"
   }
```

}

## Sensor value range

{

```json
"sensor_range": {
    "sensor_type": "",
    "sensor_name_mask": "*",
    "merge": "1",
    "lower_bound": "-1",
    "upper_bound": "1",
    "reversed": "0"
}
```

}

## Sensor value change

{

```json
"sensor_change": {
    "sensor_type": "",
    "sensor_name_mask": "*",
    "prev_msg_diff": "1", //FE maybe always set to 1 , TODO: de
```

lete maybe

```json
      "lower_bound": "-1",
    "upper_bound": "1",

}
```

}

## Driver unassigned

{

```json
"driver_unassigned": {
    "driver": 1
}
```

}

## Alarm

{

```json
"alarm": {}
```

}

## Message parameter

{

```json
"msg_param": {
    "kind": "0",
    "lower_bound": "-1",
    "param": "cell_id",
    "text_mask": "",
    "type": "1",
    "upper_bound": "-1"
}
```

}

## Unit inside geofence

{

```json
"geozone_inside": {
    "geozone_ids": "1255_1:1679329344,1255_2:1679329345",
    "lo": "OR",
    "type": 0, //TODO: delete
    "include_lbs": "0"

}
```

}

## Unit outside geofence

{

```json
"geozone_outside": {
    "geozone_ids": "1255_1:1679329344,1255_2:1679329345",
    "lo": "OR",
    "type": 1, // TODO : delete
    "include_lbs": "0"
}
```

}

## Connection loss

{

```json
"outage": {
    "check_restore": "0",
    "time": "3600",
    "type": "0",
    "include_lbs": "0"
}
```

}

## SMS

{

```json
"sms": {
    "mask": "*"
}
```

}

## Address

```json
{
    "address": {
        "city": "Cloverdale",
        "country": "USA",
        "house": "",
        "radius": "50",
        "region": "IN 46120",
        "street": "Minks Rd",
        "type": "0",
        "include_lbs": "0"
    }
}
```

## Fuel filling

```json
{
    "fuel_filling": {
        "realtime_only": "1",
        "sensor_name_mask": "*"
    }
}
```

## Fuel drain

```json
{
    "fuel_theft": {
        "realtime_only": "1",
        "sensor_name_mask": "*"
    }
}
```

## Fuel charge

```json
{
    "battery_charge": {
        "realtime_only": "1",
        "sensor_name_mask": "*"
    }
}
```

## Route control

```json
{
    "route_control": {
        "mask": "*",
        "round_mask": "*",
        "schedule_mask": "*",
        "types": "1,2,4,8,32,16,64,128,256"
    }
}
```

## Trailer

```json
{
    "trailer": {
        "code_mask": "*",
        "flags": "1",
        "type": "2"
    }
}
```

## Driver

```json
{
    "driver": {
        "code_mask": "*",

       "flags": "1",
       "type": "1" //TODO: delete this field
   }
```

}

## Passenger alarm

{

```json
"tag_alarm": {
    "time": "3600"
}
```

}

## Digital input

{

```json
"digital_input": {
    "input_index": "1",
    "type": "0"
}
```

}

## Unit interposition

{

```json
"interposition": {
    "lo": "OR",
    "radius": "1000",
    "type": "0",
    "unit_guids": "1758,1760",
    "include_lbs": "0"
}
```

}

## Message limit

{

```json
"msgs_counter": {
    "flags": "1",
    "msgs_limit": "3",
    "time_offset": "10"
}
```

}

## Passenger activity

{

```json
"tag": {
    "tag_code_mask": "*",
    "type": "1"
}
```

}

## Maintenance

{

```json
"service_intervals": {
    "days": "2",
    "engine_hours": "3",
    "flags": "7",
    "mask": "*",
    "mileage": "1",
    "val": "1"
}
```

}

## Health check

```json
{
    "health_check": {
        "healthy": "1",
        "needAttention": "1",
        "realtime_only": "1",
        "triggerForEachIncident": "1",
        "unhealthy": "1"
    }
}
```

### Error codes

| Code | Description |
| --- | --- |
| 4 | Wrong input parameters. |
| The user doesn't have the required access right to the | 7 resource (ADF_ACL_AVL_RES_VIEW_NF). |

## get_orders_notification

The get_orders_notification function is used to get the settings of the
order notification template.

```http
svc=resource/get_orders_notification&params={"resourceId":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |

## Returned result

```json
{} /* orders notification template settings as JSON */
```

See the JSON format here.

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_VIEW_ORDERS). |
| 4 | Wrong input parameters. |

## get_tag_bindings

The get_tag_bindings function is used to receive information about tag
assignments and separations during a specified time interval. The tags are
used when assigning or separating passengers.

```http
svc=resource/get_tag_bindings&params={"resourceId":<long>,

"unitId":<long>,
```

"tagId":<long>,

"timeFrom":<uint>,

"timeTo":<uint>}

You can't execute this request simultaneously with the
following requests:

report/exec_report;
report/export_result;
report/get_result_chart;
report/get_result_map;
messages/load_interval;
render/create_messages_layer;
unit/get_trips;
resource/get_trailer_bindings;
the requests from the exchange section;
account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| unitId | Unit ID (0 — all units). |
| tagId | Tag ID (0 — all tags). |
| timeFrom | The beginning of the interval. |
| timeTo | The end of the interval. |

## Returned result

```json
{
        "<text>":[{        /* tag ID */
                  "t":<unit>,       /* time of assignment/separation
*/
                  "u":<uint>,       /* unit ID in case of assignment,
0 in case of separation */
                  "pu":<uint>,      /* previous unit ID in case of separation, 0 in case of assignment */
                  "f":<uint>        /* timeout of separation, 4 — yes
*/
        }, ...],
        ...
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the | desired ACL (ADF_ACL_AVL_RES_VIEW_TAGS and ADF_ACL_ITE 7 M_EXECUTE_REPORTS), or failed to fetch the unit with the desired ACL (ADF_ACL_ITEM_VIEW). |
| 4 | Failed to fetch the list of tags or wrong input parameters. |

## get_trailer_bindings

The get_trailer_bindings function is used to receive information about
trailer assignments and separations during a specified time interval.

```http
svc=resource/get_trailer_bindings&params={"resourceId":<long>,

"unitId":<long>,

"trailerId":<long>,

"timeFrom":<uint>,

"timeTo":<uint>}

    You can't execute this request simultaneously with thefollowing requests:

       report/exec_report;
       report/export_result;

       report/get_result_chart;
       report/get_result_map;
       messages/load_interval;
       render/create_messages_layer;

       unit/get_trips;
       resource/get_trailer_bindings;

       the requests from the exchange section;
       account/get_account_history.
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| unitId | Unit ID (0 — all units). |
| trailerId | Trailer ID (0 — all trailers). |
| timeFrom | The beginning of the interval. |
| timeTo | The end of the interval. |

## Returned result

```json
{
           "<text>":[{      /* trailer ID */
                  "t":<unit>,         /* time of assignment/separation
*/
                  "u":<long>          /* unit ID in case of assignment,
0 in case of separation */
           }, ...],
           ...
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | (ADF_ACL_AVL_RES_VIEW_TRAILERS and ADF_ACL_ITEM_EXEC 7 UTE_REPORTS), or failed to fetch the unit with the desired ACL (ADF_ACL_ITEM_VIEW). |
| 4 | Failed to fetch the list of trailers or wrong input parameters. |

## get_unit_drivers

The get_unit_drivers function is used to receive the list of the drivers
assigned to a unit.

```http
svc=resource/get_unit_drivers&params={"unitId":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| unitId | Unit ID. |

## Returned result

```json
{
    "<text>":[   /* resource ID */
        {
             "id":"<text>",         /* driver ID */
             "nm":"<text>",         /* driver name */
             "ph":"<text>"                    /* driver phone number */
        }, ...
    ], ...
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the unit with the desired ACL | 7 (ADF_ACL_ITEM_VIEW). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## get_unit_trailers

The get_unit_drivers method is used to obtain the list of the drivers
assigned to a unit.

```http
svc=resource/get_unit_trailers&params={
    "unitId": <long>    // ID of the unit
}
```

### Parameters

The request must contain the unitId parameter which specifies the ID of
the unit.

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "<text>": [                 /* Resource ID. */
         {
              "id": <text>,     /* Trailer ID. */
              "nm": <text>      /* Trailer name. */
         },
         ...
    ],
    ...
}
```

If the request fails, an error code is returned.

### Error codes

Error Code             Description

4                      Wrong input parameters.

6                      Unknown error.

7                      Missing ADF_ACL_ITEM_VIEW access right to the unit.

## get_zone_data

The get_zone_data function is used to receive detailed information about
geofences.

```http
svc=resource/get_zone_data&params={"itemId":<long>,

"col":[<long>],

"flags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| The array of geofence IDs. | col        The field is optional. If it is not present, the function is executed for all IDs. |
| flags | The flags that determine the format of the returned JSON (optional). The default value is 0x1C. |
| The following flag values are available: |  |
| Value | Description |
| 0x01 | Area. |
| 0X02 | Perimeter. |
| 0X04 | The coordinates of the centre and the limits of the geofence. |
| 0X08 | All points. |
| 0X10 | Basic properties. |

## Returned result

[                                                    /* the array with
data about geofences */

```json
{
      "n":"<text>",                /* geofence name */
      "d":"<text>",                /* description */
      "id":<long>,       /* geofence ID in the resource/acc
```

ount */

```json
"rid":<long>,      /* resource/account ID */
"t":<byte>,                  /* type: 1 — line, 2 — pol
```

ygon, 3 — circle */

```json
"w":<uint>,                  /* line thickness or circl
```

e radius */

```json
"f":<uint>,                  /* geofence flags (see bel
```

ow) */

```json
"c":<uint>,                  /* colour (ARGB) */
"tc":<uint>,       /* text colour (RGB) */
"ts":<uint>,       /* font size */
"min":<uint>,      /* show on map starting with this
```

zoom */

```json
"max":<uint>,      /* show on map until this zoom */
"i":<ushort>,      /* the check sum of the image (CRC
```

16) */

```json
"icon":"<text>",             /* zone item image URI */
"path":"<text>",             /* short path to the defau
```

lt icon */

```json
"ar":<double>,     /* area */
"pr":<double>,     /* perimeter */
"libId":<long>, /* icon library ID, 0 — ID of the
```

default icon library */

```json
"jp":<JSON>,       /* custom JSON */
"b":{                        /* limits */
          "min_x":<double>,          /* minimum longitu
```

de */

```json
"min_y":<double>,          /* minimum latitud
```

e */

```json
"max_x":<double>,          /* maximum longitu
```

de */

```json
"max_y":<double>,          /* maximum latitud
```

e */

```json
                              "cen_x":<double>,         /* the longitude of the centre     */
                              "cen_y":<double>          /* the latitude ofthe centre */
                      },
                      "p":[                      /* the array of geofence points */
                              {
                                       "x":<double>,    /* longitude */
                                       "y":<double>,    /* latitude */
                                       "r":<uint>                /* radius
*/
                              },
                              ...
                      ],
                      "ct":<uint>,     /* creation time */
                      "mt":<uint>      /* the previous modification time
*/
           },
           ...
]
```

Geofence flags (“f”):

Value                   Description

0x20                    Show shape.

0X40                    Not simplify the geofence.

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | (ADF_ACL_AVL_RES_VIEW_ZONES and ADF_ACL_ITEM_EXECUT 7 E_REPORTS), or failed to fetch the unit with the desired ACL (ADF_ACL_ITEM_VIEW). |
| 4 | Wrong input parameters. |

## get_zones_by_point

The get_zones_by_point function is used to check if a point is inside
certain geofences or to find the nearest geofence.

```http
svc=resource/get_zones_by_point&params={"spec": {

"lat":<double>,

"lon":<double>,

"radius":<double>,

"zoneId":{

"<long>":[<uint>,

...

],

...

},

}

}
```

### Parameters

| Name | Description |
| --- | --- |
| zoneId | The list of geofences: {“resource ID”:[geofence ID,…], …}. |
| lat | Latitude. |
| lon | Longitude. |
| radius | The geofences search radius, m. Optional field. |
| If the array of geofence IDs for the indicated “resource ID” | is empty, all the resource geofences are taken. |

## Returned result

If the point is inside the geofence, the returned result is:

```json
[
         {
                   "<text>": {      /* resource ID */
                            "<text>": 0,      /* geofence ID, the distance to the geofence, m (always 0 in this case) */...
                   },
                   ...

         }
]
```

If the point is outside the geofence, the returned result is:

```json
[
         {
                  "<text>":{             /* resource ID */
                             "<text>": <double>,         /* geofence ID, distance to geofence, m */
                  }
         }
]
```

If there is no radius field, the returned result is:

```json
[
         {
                  "<text>": [            /* resource ID */
                             <long>, /* geofence IDs */...
                  ],
                  ...
         }
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | General error. |
| 4 | Wrong input parameters. |

## get_zones_by_unit

The get_zones_by_unit request checks if the specified units are inside the
specified geofences.

### Endpoint

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=resource/get_zones
_by_unit
```

### Parameters

The following parameters are required:

Na     Ty
Description
me     pe

str
sid    in     The session ID used for authentication.
g

par    ob
am     je     A JSON object containing request specifications.
s      ct

Contains information about the geofences (zoneId), units
ob
spe           (units), and time (time) for which the unit location inside
je
c             the geofences is checked. See the description of these
ct
parameters below.

## spec parameters

The following spec parameters are required:

Na
Type       Description
me

A JSON object that maps resource IDs to arrays of
geofence IDs.
Each key is the resource ID, and the value is an
array of corresponding geofence IDs for this
resource.
Example

```json
"zoneId": {
 “912”: [4, 5, 6, 7, 8, 9],
```

zon
object
eId                “913”: [1, 2, 3, 4, 5, 76]

In this example:

The resource with ID 912 includes the
geofences with IDs 4, 5, 6, 7, 8, 9.
The resource with ID 913 includes the
geofences with IDs 1, 2, 3, 4, 5, 76.

A list of unit IDs for which presence in the
array of   geofences is checked.
unit
integer    Example
s
s          “units”: [917]
In this example, the unit with ID 917 is checked.

tim    integer    Specifies the time for which the unit location inside
e                 the geofences is checked:

If a timestamp value in the Unix format is
specified, then the unit location at the
specified time is checked.
If 0 is specified, the latest known location of
the unit is checked.

Example
“time”: 0

In this example, the latest location of the unit is
checked.

## Request example

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=resource/get_zones
_by_unit&sid=0b149aca05cd00ee2c7658124f5248fe&params={"spec":{"zoneId":{"912":[4,5,6,7,8,9],"913":[1,2,3,4,5,76]},"units":[917],"time":0}}
```

In this example:

The request checks if the unit with ID 917 is located within the specified
geofences of two resources with IDs 912 and 913.
time=0 specifies that the latest location of unit 917 is checked.

## Returned result

The response indicates whether the specified unit or units were located
within the specified geofences at the requested time.

```json
{
    "<text>": {     /* resource ID */
          "<text>": [   /* geofence IDs */
              <long>,   /* unit IDs */...
          ]
    },
    ...
}
```

## Success response example

```json
{"912":{"4":[917]}}
```

In this example, the unit with ID 917 is inside the geofence with ID 4. The
geofence belongs to the resource with ID 912.

## Empty response

If no units are found in the geofences at the specified time, an empty JSON
is returned.

```json
{ }
```

## Possible error codes

If the request is not completed successfully, an error code is returned.

Error code                 Description

4                          Invalid input parameters.

6                          Unknown error.

## update_driver

The update_driver function is used to create, edit, or delete drivers.

svc=resource/update_driver&params={"itemId":<long>,

```json
"id":<long>,
"callMode":"<text>",
"ej":{"apps":[{"appId":"<text
```

>","type":"<text>","uid":"<text>","sn":"<text>"},...]},

```json
"c":"<text>",
"ck":<short>,
"ds":"<text>",
"n":"<text>",
"p":"<text>",
"r":<double>,
"f":<uint>,
"pwd":"<text>",
"jp":{
       "<text>":"<text>",
       ...
}}
```

### Parameters

Name      Description     Required to

itemId    Resource ID.

Driver ID
id        (0 — create)
.

Action:
create,
callMo
update,
de
delete,
reset_image.

create      update      reset_image       delete

Extended
JSON (with
example for
ej                    {}          {}   -           -
push
notifications
).

c     Code.           +           +    -           -

The check
sum of
ck                    -           -    -           -
driver
image.

ds    Description.    +           +    -           -

n     Name.           +           +    -           -

The phone
number, like
+12345678
p                     +           +    -           -
90 ( + must
be encoded
as %2B).

The aspect
ratio of the
r                     -           -    -           -
driver
image.

Flags
f     (4 — exclusi    0           0    -           -
ve).

pwd   The             +           +    -           -
password for
the mobile

authorizatio
n.

Custom
fields in
jp              the "name":        {}           {}          -                   -
"value" for
mat.

“{ }” and “0” are the default values.

## Returned result

For creation, modification, and reset_image requests:

```json
[
           <long>,                                             /* driver ID */
           {
                       "id":<long>,                  /* driver ID */
                       "n":"<text>",                           /* name */
                       "c":"<text>",                           /* code */
                       "ej":{ ... },                 /* extended JSON */
                       "jp": {                                 /* custom fields
*/
                                 "<text>":"<text>",            /* name:value */...
                       },
                       "pwd":"<text>",              /* the password for the mobile authorization */
                       "ds":"<text>",                /* description */
                       "p":"<text>",                           /* phone number */
                       "r":<double>,                 /* aspect ratio of driverimage */
                       "f":<uint>,                             /* flags (see below) */
                       "ck":<ushort>,                /* check sum of driver image */

                  "ct":<uint>,                /* creation time */
                  "mt":<uint>,                /* modification time */
                  "bu":<long>,                /* assigned unit */
                  "pu":<long>,                /* previous assigned unit
*/
                  "bt":<uint>,                /* time of last assignment/separation */
                  "bs":<long>,                /* sensor ID */
                  "pos":{                            /* position */
                            "y":<double>,     /* latitude */
                            "x":<double>      /* longitude */
                  }
        }
]
```

Flags:

| Flag | Description |
| --- | --- |
| 0x1 | Object type: Driver. |
| 0x2 | Object type: Trailer. |
| 0x4 | Restrict assignment. |
| 0x8 | Object type: Driver group. |
| 0x10 | Object type: Trailer group. |
| For deletion requests: |  |

```json
[
        <long>,             /* driver ID */null

]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to update the phone number. One of the possible | 1002 reasons is that the number already exists. |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_DRIVERS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_driver_units

The update_driver_units function is used to update the list of units
selected for the automatic assignment of drivers.

```http
svc=resource/update_driver_units&params={"itemId":<long>,

"units":[<long>]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| units | The array of unit IDs. |

## Returned result

```json
{
        "drvrun":[<long>]         /* array of units for automatic assignment */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_DRIVERS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_drivers_group

The update_drivers_group function is used to create, edit, or delete
driver groups.

```http
svc=resource/update_drivers_group&params={"itemId":<long>,

"id":<long>,

"callMode":<text>,

"n":<text>,

"d":<text>,

"drs":[<uint>],

"f":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Driver group ID. |
| callMode | Action: create, update, delete. |
| The following parameters are only required to create and delete driver | groups: |
| Name | Description |
| n | Name. |
| d | Description. |
| drs | The array of driver IDs. |
| f | Flags. Doesn't affect the request result. |

## Returned result

For creation and modification requests:

```json
[
     <long>,                                /* group ID */
     {
               "id":<long>,       /* group ID */
               "n":<text>,                  /* name */
               "d":<text>,                  /* description */
               "drs":[<uint>]     /* array of driver IDs */
     }
]
```

For deletion requests:

```json
[
     <long>,           /* group ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_DRIVERS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_email_template

The update_email_template function is used to update the custom letter
template.

svc=resource/update_email_template&params={"resourceId":<uint>,

"subject":"<text>",

"body":"<text>",

```json
"flags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | The resource ID of the user. |
| subject | Email subject. |
| body | Email body. |
| flags | Use the default template: |
| 0 — yes; | 1 — no. |
| The following variables can be used in the subject and body text: |  |
| Name | Description |
| %JOB_NOTIFICATION% | The name of the job or notification. |
| %ITEM% | The name of the item in the report. |
| %TEMPLATE% | The name of the report template. |
| %DATE_TIME% | Date and time. |
| %LINK% | The link to download the report. |

## Returned result

```json
{"error":0}              /* if the execution is successful */
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired ACL | 7         (ADF_ACL_ITEM_VIEW_PROPERTIES and ADF_ACL_ITEM_EDIT_OTHER). |
| 6 | Failed to update the email template. |
| 4 | Wrong input parameters. |

## update_job

The update_job function is used to create, edit, or delete jobs.

```http
svc=resource/update_job&params={"itemId":<long>,
                                                                        "id":<long>,
                                                                        "callMode":"<text>",

"n":"<text>",

"d":"<text>",

"r":"<text>",
                                                                        "at":<uint>,

"m":<uint>,
                                                                        "fl":<uint>, /* Not required for job creation, editing, and deletion. Used for test execution. Default: 0 */
                                                                        "tz":<int>,

"l":"<text>",

"e":<bool>,
                                                                        "sch":{
```

"f1":<uint>,

"f2":<uint>,

"t1":<uint>,

"t2":<uint>,

"m":<uint>,

"y":<uint>,

"w":<uint>

```
},
"a
```

ct":{

"t":"<text>",

"p":{

"<text>":"<text>",

...

}

```
}}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Job ID (0 — create). |
| callMode | Action: create, update, delete. |
| Other parameters are only required for creating and updating. See | the get_job_data page. |

## Returned result

For creation and modification requests:

```json
[
          <long>,             /* job ID */
          {
                    "id":<long>,       /* job ID */
                    "n":"<text>",      /* name */
                    "d":"<text>",      /* description */
                    "m":<uint>,        /* maximum executions count, 0 — unlimited */
                    "fl":<uint>,       /* delete job after maximum executions count, 1 — yes. Not required for job creation, editing, and deletion. Used for test execution. */
                    "st":{             /* state */
                              "e":<uint>,        /* enabled/disabled */
                              "c":<uint>,        /* executions count */
                              "l":<uint>         /* last execution time */
                    },
                    "act":"<text>", /* action */
                    "ct":<uint>,       /* creation time */
                    "mt":<uint>        /* last modification time */
          }
]
```

All the possible action types are described here.

For deletion requests:

```json
[
          <long>,            /* job ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired | 7 ACL (ADF_ACL_AVL_RES_EDIT_JOBS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_notification

The update_notification function is used to create, edit, or delete
notifications.

svc = "resource/update_notification"

```json
params = {
    "itemId": <long>,
    "id": <long>,    // Notification ID
    "callMode": "<text>",
    "e": <uint>,
    "n": "<text>",    // Name
    "txt": "<text>",    // Notification text
    "ta": <uint>,    // Activation time (Unix format)
    "td": <uint>,    // Deactivation time (Unix format)
```

"ma": <uint>,       // Maximum number of alarms (0 = unlimited)
"mmtd": <uint>,       // Max time interval between messages (sec)
"cdt": <uint>,       // Alarm timeout (sec)
"mast": <uint>,       // Min duration of alarm state (sec)
"mpst": <uint>,       // Min duration of previous state (sec)
"cp": <uint>,       // Control period relative to current time (sec)
"fl": <uint>,       // Notification flags
"tz": <int>,       // Time zone
"la": "<text>",       // User language (2-letter code)
"un": [<long>],       // Array of unit or unit group IDs
"d": [<text>],        // Notification description
"sch": {       // Notification schedule

```json
"f1": <uint>,    // Interval 1 start (minutes from midnight)
"f2": <uint>,    // Interval 2 start (minutes from midnight)
"t1": <uint>,    // Interval 1 end (minutes from midnight)
"t2": <uint>,    // Interval 2 end (minutes from midnight)
"m": <uint>,    // Day-of-month mask
"y": <uint>,    // Month mask
"w": <uint>     // Day-of-week mask
```

},

"ctrl_sch": {       // Max alarms control schedule

```json
"f1": <uint>,
"f2": <uint>,
"t1": <uint>,
"t2": <uint>,
"m": <uint>,
"y": <uint>,
"w": <uint>
```

},

"trg": {       // Trigger

```json
"t": "<text>",
"p": {
    "<text>": "<text>",
    ...
}
```

},

"act": [       // Actions

```json
        {
            "t": "<text>",    // Action type
            "p": {
                "<text>": "<text>",   // Parameters...
            }
        }
    ]
}
```

See notifications flag and action type description on the
get_notification_data page.

For notifications of the Off time control type, the value of
the mast parameter specified in seconds must correspond to the value of
the min_idle_time parameter specified in minutes. Thus, if you want the
notification to be triggered after 10 minutes of off time, specify 10
for min_idle_time and 600 for mast.

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Notification ID (0 — create). |
| callMode | Action: create, edit, delete, enable. |
| Is used only for the "enable" callMode: |  |
| e | 0 — disable; |
| 1 — enable. |  |
| Other parameters are only required for creating and updating. See | the get_notification_data page. |

## Returned result

For creation and modification requests:

```json
[
           <long>,                                /* notification ID */
           {
                     "id":<long>,       /* notification ID */
                     "n":"<text>",                /* name */
                     "txt":"<text>", /* notification text */
                     "ta":<uint>,       /* activation time (Unix format)
*/
                     "td":<uint>,       /* deactivation time (Unix format)
*/
                     "ma":<uint>,       /* maximum alarms count (0 — unlimited) */
                     "fl":<uint>,       /* notification flags */
                     "ac":<uint>,       /* execution count */
                     "un":[<long>],     /* array of units/unit group IDs
*/
                     "act":["<text>"],            /* actions */
                     "trg":"<text>", /* control type */
                     "trg_p":{},                  /* control settings */
                     "crc":<long>,      /* check sum of binary representation of notification */
                     "ct":<uint>,       /* creation time */
                     "mt":<uint>        /* last modification time */
           }
]
```

Notification flags, action, and control types are described here.

For deletion requests:

```json
[
         <long>,            /* notification ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_NF). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_orders_notification

The update_orders_notification function is used to update the settings
of the notification templates for orders.

```http
svc=resource/update_orders_notification&params={"resourceId":<long
>,

"ordersNotification":<JSON>}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| ordersNotification | The notification template settings in JSON format. |
| JSON keys: |  |
| { | "sms":"<text>",               /* SMS notification text */ "subj":"<text>",                        /* email subject */ "text":"<text>",                        /* email text */ "html":<uint>,                /* email text as HTML (1 — yes) */ "currency":"<text>",          /* currency */ "dns":"<text>",               /* locator URL (without http://) */ "driverPushMsg":{             /* driver push notification settings */ |

```json
"crR":{
"t":"<text>"        /* notification text after creatin
```

g a new route */

```json
         },
"delR":{
         "t":"<text>"        /* notification text after deletin
```

g a route */

```json
},
"updC":{
         "t":"<text>"        /* notification text after changin
```

g contact details */

```json
},
"attO":{
         "t":"<text>"        /* notification text after attachi
```

ng files */

```json
},
"detO":{
     "t":"<text>"            /* notification text after deletin
```

g files */

```json
          },
          "updG":{

               "t":"<text>"       /* notification text after changing order parameters */
          },
          "vtD":{
               "t":"<text>"       /* notification text after exceeding the delivery time*/
          },
          "utD":{
               "t":"<text>"       /* notification text after exceeding the unloading time */
          },
          "trk":{
               "t":"<text>"       /* notification text in case of adeviation from a route */
          }
          "skp":{
               "t":"<text>"       /* notification text in case of skipping an order */
          },
          "stO":{
               "t":"<text>"       /* notification text in case an order is not confirmed by the courier/operator */
          }
     },
}
```

The tags of notification body and email subject:

Tag                                          Description

%ORDER_NAME%                                 Order name.

%ORDER_ARRIVAL_TIME%                         Estimated arrival.

%ORDER_COST%                                 Order cost.

%ORDER_COMMENT%                               Comment.

%LOCATOR_LINK%                                Current location.

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_ORDERS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_tag

The update_tag function is used to create, edit, or delete tags. The tags
are used when assigning or separating passengers.

```http
svc=resource/update_tag&params={"itemId":<long>,
                                                                         "i
```

d":<long>,
"c
allMode":"<text>",

"c":"<text>",
"c
k":<short>,

"n":"<text>",

"p":"<text>",

"r":<double>,
"t
z":<int>,

"f":<int>,
"a
rt":<uint>,
"j
p":{

"<text>":"<text>",

...

```
}}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Tag ID. To create a tag, send 0. |
| callMode | Modes: |
| create; | update; |
| delete; | reset_image. |
| The following parameters are only required to create and update tags: |  |
| Name | Description |
| c | Code. |
| ck | The check sum of the tag image. |
| n | Tag name. |
| p | Phone number of the +1234567890 type. Should be encoded as %2B. |
| tz | Time zone. |
| jp | Custom fields in the "name":"value" format. |
| f | Flags (optional). 0 by default. |
| art | The timeout for automatic reset (optional). 36000 (10 hours) by default. |

## Returned result

For creation and modification requests:

```json
[
         <long>,                                       /* tag ID */
         {
                   "id":<long>,                 /* ID */
                   "n":"<text>",                       /* name */
                   "c":"<text>",                       /* code */
                   "jp": {                             /* custom fields
*/
                             "<text>":"<text>",        /* "name":"value"
*/...
                   },
                   "r":<double>,                /* aspect ratio of tag image */
                   "ck":<ushort>,               /* the check sum of tag image */
                   "f":<ushort>,                /* flag, not currently used, default value = 1 */
                   "bu":<long>,                 /* the assigned unit */
                   "pu":<long>,                 /* the previous assigned unit */
                   "bt":<uint>,                 /* the time of the previous assignment/separation */
                   "pos":{                             /* position */
                             "y":<double>,      /* latitude */
                             "x":<double>       /* longitude */
                   }
         }
]
```

For deletion requests:

```json
[
         <long>,             /* tag ID */null

]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_TAGS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_tag_message

The update_tag_message function is used to update or delete the
message of binding a tag. The tags are used when assigning or separating
passengers.

Only works with the previously created bindings.

```http
svc=resource/update_tag_message&params={"resourceId":<long>,

"unitId":<long>,

"tagId":<long>,

"time":<uint>,

"callMode":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| d | resourceI Resource ID. |
| The unit ID to change for assignment, 0 — to change for | unitId         separation. Only required for the "update" mode. |
| tagId | Tag ID. |
| time | Time. |
| callMode | Mode: update or delete. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_TAGS or ADF_ACL_ITEM_VIEW). |
| 4 | Wrong input parameters. |
| 3 | Failed to fetch messages. |

## update_tag_units

The update_tag_units function is used to update the list of units selected
for the automatic assignment of tags in a resource. The tags are used when
assigning or separating passengers.

```http
svc=resource/update_tag_units&params={"itemId":<long>,

"units":[<long>]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| units | The array of unit IDs. |

## Returned result

```json
{
        "tagrun":[<long>]         /* array of units for automatic assignment */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_TAGS). |
| 6 | Failed to update. |
| 4 | Wrong input parameters. |

## update_tags_group

The update_tags_group function is used to create, edit, or delete tag
groups. The tags are used when assigning or separating passengers.

```http
svc=resource/update_tags_group&params={"itemId":<uint>,

"id":<uint>,

"callMode":"<text>",

"n":"<text>",

"d":"<text>",

"tgs":[<uint>,...]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Tag group ID. |
| callMode | Action: create, update, delete. |
| The following parameters are only required to create and delete tag groups: |  |
| Name | Description |
| n | Name. |
| d | Description. |
| trs | The array of tag IDs. |

## Returned result

For creation and modification requests:

```json
[
          <long>,                                                  /* group I
D */
          {
                    "id":<long>,                        /* ID */

                    "n":"<text>",                              /* name */
                    "d":"<text>",                              /* description */
                    "tgs":[<uint>,...]          /* tag IDs array */
          }
]
```

For deletion requests:

```json
[
          <long>,          /* group ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_TAGS). |
| 6 | Failed to get the current user or undefined error. |
| 4 | Wrong input parameters. |

## update_trailer

The update_trailer function is used to create, edit, or delete trailers.

svc=resource/update_trailer&params={"itemId":<long>,
"i
d":<long>,
"c
allMode":"<text>",
"e
j":{ ... },

"c":"<text>",
"d
s":"<text>",

"n":"<text>",

"f":<uint>,
"j
p":{

"<text>":"<text>",

...

```
}}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Trailer ID. To create a trailer, send 0. |
| callMode | Modes: |
| create; |  |
| update; | delete; |
| reset_image. |  |
| The following parameters are only required to create and update trailers: |  |
| Name | Description |
| ej | Extended JSON (optional). { } by default. |
| c | Code. |
| ds | Description. |
| n | Trailer name. |
| f | Flags, not currently used. |
| jp | Custom fields in the "name":"value" format. Optional. { } by default. |

## Returned result

For creation and modification requests:

```json
   [
        <long>,                                         /* trailer ID */
        {
                    "id":<long>,                 /* trailer ID */
                    "n":"<text>",                       /* name */
                    "c":"<text>",                       /* code */
                    "ej":"<text>",               /* extended JSON */
                    "jp": {                             /* custom fields

*/
                             "<text>":"<text>",        /* name: value */...
                   },
                   "ds":"<text>",               /* description */
                   "p":"<text>",                       /* phone number */
                   "r":<double>,                /* aspect ratio of the image */
                   "ck":<ushort>                /* the check sum of the image */
                   "bu":<long>,                 /* the assigned unit */
                   "pu":<long>,                 /* the previous assigned unit */
                   "bt":<uint>,                 /* the time of the previous assignment/separation */
                   "pos":{                             /* position */
                             "y":<double>,      /* latitude */
                             "x":<double>       /* longitude */
                   }
         }
]
```

For deletion requests:

```json
[
         <long>,             /* trailer ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_TRAILERS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_trailer_units

The update_trailer_units function is used to update the list of units
selected for the automatic assignment of trailers.

```http
svc=resource/update_trailer_units&params={"itemId":<long>,

"units":[<long>]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| units | The array of unit IDs. |

## Returned result

```json
{
        "trlrun":[<long>]        /* array of units for automatic as

signment */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_TRAILERS). |
| 6 | Failed to update or undefined error. |
| 4 | Wrong input parameters. |

## update_trailers_group

To create, edit, or delete trailer groups, use the
resource/update_trailers_group method.

### Endpoint

```http
svc=resource/update_trailers_group&params={
    "itemId": <long>,
    "id": <long>,
    "callMode": <text>,
    "n": <text>,
    "d": <text>,
    "drs": [<uint>]
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Trailer group ID. |
| callMode | Action type: create, update, delete. |
| n | Trailer group name. Required only for the create and update action type. |
| Trailer group description. Required only for the create | d ** and update action type. |
| drs | Array of trailer IDs. Required only for the create and update action type. |

### Response

If the request for creating or editing the trailer group is completed
successfully, the response is returned in the following format:

```json
[
      <long>,   // Trailer group ID.
      {
          "id": <long>,   // Trailer group ID.
          "n": <text>,    // Trailer group name.
          "d": <text>,    // Trailer group description.
          "drs": [<uint>]    // Array of trailer IDs.

    }
]
```

If the request for deleting the trailer group is completed successfully, the
response is returned in the following format:

```json
[
    <long>,     // Trailer group ID.null
]
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4               Invalid input parameters.

6               Unknown error.

Missing ADF_ACL_AVL_RES_EDIT_TRAILERS access right to
7
the resourse.

## update_zone

The update_zone function is used to create, edit, or delete geofences.

```http
svc=resource/update_zone&params={"itemId":<long>,

"id":<long>,
```

"callMode":"<text>",

"n":"<text>",

"d":"<text>",

"t":<int>,

"w":<int>,

"f":<uint>,

"c":<int>,

"tc":<uint>,

"ts":<uint>,

"min":<uint>,

"max":<uint>,

"path":"<text>",

"libId":<long>,

"oldItemId":<uint>,

"oldZoneId":<uint>,

"jp":<JSON>,

"p":[

{

"x":<double>,

"y":<double>,

```json
"r":<int>

}

]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Geofence ID (0 — create). |
| callMode | Action: create, update, delete, reset_image. |
| oldItemId | The ID of the resource from which the geofence should be copied. |
| d | oldZoneI The ID of the geofence which should be copied. |
| n | Name. |
| d | Description. |
| Geofence type: |  |
| t | 1 — line; 2 — polygon; |
| 3 — circle. |  |
| w | Line width. |
| f | Flags (see below). |
| c | Colour. |
| tc | Text colour. |
| ts | Text size. |
| min | Minimum scale (visibility from). |
| max | Maximum scale (visibility to). |
| path | Icon path. |
| lindId | Icon library ID. |
| jp | Custom fields in the name:value format. |
| p | Points, where "r" is the radius. |
| If you want to copy (and to edit at the same time) a | geofence, use the oldItemId and oldZoneId parameters to indicate it. |
| The other parameters are only required to create and to edit geofences. | Read more on the get_zone_data page. |
| Flags: |  |
| Flag | Description |
| 0х1 | Address. |
| 0x2 | The beginning of the trip. |
| 0x4 | The end of the trip. |
| 0x10 | Float. |
| 0x20 | Show shape. |
| 0x40 | Skip the simplification. |

## Returned result

For creation and modification requests:

```json
[
          <long>,                                        /* geofence ID */
          {
                    "n":"<text>",                        /* name */
                    "d":"<text>",                        /* description */
                    "id":<long>,                 /* geofence ID */
                    "f":<uint>,                          /* flags
*/
                    "t":<int>,                           /* type: 1
— line, 2 — polygon, 3 — circle */
                    "e":<ushort>                 /* check sum (CRC1
6) */
                    "c":<uint>,                          /* RGB colour */
                    "i":<ushort>,                /* check sum of image (CRC16) */
                    "icon":"<text>",                     /* icon image URI */

                  "path":"<text>",                         /* short path to default icon */
                  "libId":<long>,                /* ID of the iconlibrary, 0 — ID of the default icon library */
                  "w":<int>,                                           /*line width */
                  "b":{                                    /* configuration for rendering */
                          "min_x":<double>,      /* minimum longitude */
                          "min_y":<double>,      /* minimum latitude */
                          "max_x":<double>,      /* maximum longitude */
                          "max_y":<double>,      /* maximum latitude */
                          "cen_x":<double>,      /* the longitude of the centre */
                          "cen_y":<double>       /* the latitude ofthe centre */
                  },
                  "ct":<uint>,                   /* creation time
*/
                  "mt":<uint>,                   /* last modification time */
                  "jp":<JSON>                    /* custom JSON */
        }
]
```

The geofence flags are described on the get_zone_data page.

For deletion requests:

```json
[
        <long>,           /* geofence ID */null

]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired ACL | (ADF_ACL_AVL_RES_EDIT_ZONES or 7 ADF_ACL_AVL_RES_VIEW_ZONES) or item/zone with the old_id not found. |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_zones_group

The update_zones_group function is used to create, edit, or delete
geofence groups.

```http
svc=resource/update_zones_group&params={"itemId":<long>,
                                          "id":<long>,
                                          "callMode":"<text>",
                                          "n":"<text>",
                                          "d":"<text>",
                                          "zns":[<uint>]}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Geofence group ID. |
| callMode | Action: create, update, delete. |
| The following parameters are only required to create and delete geofence | groups: |
| Name | Description |
| n | Name. |
| d | Description. |
| trs | The array of geofence IDs. |

## Returned result

For creation and modification requests:

```json
[
          <long>,                                /* group ID */
          {
                    "id":<long>,       /* group ID */
                    "n":"<text>",                /* name */
                    "d":"<text>",                /* description */
                    "zns":[<uint>]     /* array of geofences IDs */
          }
]
```

For deletion requests:

```json
[
        <long>,             /* group ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_ZONES). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## upload_driver_image

The upload_driver_image function is used to attach an image to a driver.

```http
svc=resource/upload_driver_image&params={"itemId":<long>,

"driverId":<long>,

"eventHash":"<text>",

"oldItemId":<long>,

"oldDrvId":<uint>}
                                  &sid="<text>"

      To delete the image, use the update_driver function.
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| driverId | Driver ID. |
| eventHa      The name of the event which should be generated after | sh           attaching the image. Optional parameter. |
| oldItemI     The resource ID from which the driver image should be | d            copied. Optional parameter. |
| oldTagId | The driver ID the image of which should be copied. Optional parameter. |
| To upload an image, use a POST request with multiple contents | (multipart/form-data), where one part contains the parameters and the other contains the image. |
| Example: |  |
| Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=resou | rce/upload_driver_image Request Method: POST Host: hst-api.wialon.com |
| B4wasXYYHLTNXHBl | Connection: keep-alive Content-Length: 31755 Cache-Control: no-cache Content-Type: multipart/form-data; boundary=----WebKitFormBoundary Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*; q=0.8 Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3 Accept-Encoding: gzip,deflate,sdch Accept-Language: ru,en-US;q=0.8,en;q=0.6 |
| ------WebKitFormBoundaryB4wasXYYHLTNXHBl | Content-Disposition: form-data; name="params" |

```json
{"itemId":717314,"driverId":17,"eventHash":"jUploadForm13727685549
99"}
------WebKitFormBoundaryB4wasXYYHLTNXHBl
Content-Disposition: form-data; name="eventHash"

jUploadForm1372768554999
------WebKitFormBoundaryB4wasXYYHLTNXHBl
Content-Disposition: form-data; name="drivers_dlg_props_upload_image"; filename="image.jpg"
Content-Type: image/jpeg

------WebKitFormBoundaryB4wasXYYHLTNXHBl--
```

It is also possible to copy an image from another driver. To do this, execute
a request with no image but with the oldItemId and oldDrvId fields.

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired | ACL (ADF_ACL_AVL_RES_EDIT_DRIVERS) or the item/driver 7 with the old_id not found (when copying the image from another driver). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |
| To make sure that the image has been uploaded, execute | the avl_evts request: |

```json
{
         "tm":<uint>,                                   /* current servertime (UTC) */
         "events":[
                 {
                           "i":<long>,                          /* driver
ID (-1 if unknown) */
                           "d":{                                /* data */
                                     "hash":"<text>"            /* the uploading is complete */
                           }
                 }
         ]
}
```

## upload_tacho_file

The resource/upload_tacho_file method is used for uploading
tachograph files to the server.

To upload a tachograph file and get it parsed, use signature 1:

```http
svc=resource/upload_tacho_file&params={
      "outputFlag": <uint>,
      "eventHash": <text>
}
```

To bind the content of the uploaded file to a specified driver, use signature
2:

```http
svc=resource/upload_tacho_file&params={
      "itemId": <long>,
      "driverCode": <text>,
      "guid": <text>,
      "outputFlag": <uint>
}
```

### Parameters

Below is te description of the request parameters.

| Parameter | Description |
| --- | --- |
| itemId | Resource ID. |
| driverCode | Driver code. |
| guid | Uploaded file identifier. You can obtain it from the response to a POST request that uses signature 1. |
| outputFlag | Response flag: 1 — get the DDD header; 2 — get activity. |
| Parameter | Description |
| eventHash | Event name which will be generated after processing the data. |

### Response

If the file is parsed successfully, the response is returned in the following
format:

```json
{
     "guid": <text>,                             // Uploaded file identifier.
     "parseResult": {                            // Parsing result.
           "an": <text>,                         // Issue authority.
           "c": <text>,                          // Country.
           "dc": <text>,                         // Driver's code, 14 characters.
           "dn": <text>,                         // Driver's name.
           "la": <long>,                         // Last activity date.
           "ed": <long>,                         // Expiry date.
           "fa": <long>,                         // First activity date.
           "id": <long>,                         // ID.
           "vb": <long>,                         // Validity period beginning.
           "vl": [<text>],                       // Vehicle registration plate.
           "activity": {                         // Driver's activity.
Shown if outputFlag:2 is set.
               "Availability": {
                  "a": <uint>,                   // Driver's action: 0
— break/rest, 1 — availability, 2 — work, 3 — driving.
                  "cs": <uint>,                  // Card status: 0 — inserted; 1 — not inserted.
                  "s": <uint>,                   // Driver's slot: 0 —

driver, 1 — co-driver.
                  "st": <uint>,                 // Number of drivers:
0 — one driver, 1 — crew.
                  "t": <uint>                   // Time.
             },
             "Break/Rest": {
                  "a": <uint>,
                  "cs": <uint>,
                  "s": <uint>,
                  "st": <uint>,
                  "t": <uint>
             },
             "Driving": {
                  "a": <uint>,
                  "cs": <uint>,
                  "s": <uint>,
                  "st": <uint>,
                  "t": <uint>
             },
             "Work": {
                  "a": <uint>,
                  "cs": <uint>,
                  "s": <uint>,
                  "st": <uint>,
                  "t": <uint>
             }
         }
    }
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
Code

One of the following errors:

Invalid input parameters. (for signature 2)
4
Driver not found (for signature 2).
Failed to parse or validate a file with the guid.

One of the following errors:

Failed to upload the DDD file (for signature 1).

5              Failed to write the DDD file (for signature 2).

Failed to read a file with the guid from the file system
(for signature 2).

One of the following errors (for signature 2):

Missing ADF_ACL_AVL_RES_EDIT_DRIVERS access right
7              to the resource.
Failed to find the resource with the specified ID.

## upload_tag_image

The upload_tag_image function is used to attach an image to a tag. The
tags are used when assigning or separating passengers.

svc=resource/upload_tag_image&params={"itemId":<long>,

"tagId":<long>,

"eventHash":"<text>",

```json
"oldItemId":<long>,

"oldTagId":<uint>}
                                 &sid="<text>"

       To delete the image, use the update_tag function.
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| tagId | Tag ID. |
| eventHa       The name of the event which should be generated after | sh            attaching the image. Optional parameter. |
| oldItemI      The resource ID from which the tag (passenger) image | d             should be copied. Optional parameter. |
| oldTagId | The tag ID the image of which should be copied. Optional parameter. |
| To upload an image, use a POST request with multiple contents | (multipart/form-data), where one part contains the parameters and the other contains the image. |
| Example: |  |
| B4wasXYYHLTNXHBl | Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=resou rce/upload_tag_image Request Method: POST Host: hst-api.wialon.com Connection: keep-alive Content-Length: 31755 Cache-Control: no-cache Content-Type: multipart/form-data; boundary=----WebKitFormBoundary Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*; q=0.8 Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3 Accept-Encoding: gzip,deflate,sdch Accept-Language: ru,en-US;q=0.8,en;q=0.6 |
| ------WebKitFormBoundaryB4wasXYYHLTNXHBl | Content-Disposition: form-data; name="params" |

```json
{"itemId":717314,"tagId":17,"eventHash":"jUploadForm137276855499
9"}
------WebKitFormBoundaryB4wasXYYHLTNXHBl
Content-Disposition: form-data; name="eventHash"

jUploadForm1372768554999
------WebKitFormBoundaryB4wasXYYHLTNXHBl
Content-Disposition: form-data; name="tags_dlg_props_upload_image"; filename="image.jpg"
Content-Type: image/jpeg

------WebKitFormBoundaryB4wasXYYHLTNXHBl--
```

It is also possible to copy an image from another tag (passenger). To do
this, execute a request with no image but with the oldItemId and
oldTagId fields.

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired | 7        ACL (ADF_ACL_AVL_RES_EDIT_TAGS) or the item/tag with the old_id not found (when copying the image from another tag). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |
| To make sure that the image has been uploaded, execute | the avl_evts request: |

```json
{
         "tm":<uint>,                                   /* current servertime (UTC) */
         "events":[
                 {
                           "i":<long>,                          /* tag ID
(-1 if unknown) */
                           "d":{                                /* data */
                                     "hash":"<text>"            /* the uploading is complete */
                           }
                 }
         ]
}
```

## upload_trailer_image

The upload_trailer_image function is used to attach an image to a trailer.

```http
svc=resource/upload_trailer_image&params={"itemId":<long>,

"trailerId":<long>,

"eventHash":"<text>",

"oldItemId":<long>,

"oldTrId":<uint>}
                                     &sid="<text>"

      To delete the image, use the update_trailer function.
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| trailerId | Trailer ID. |
| eventHa      The name of the event which should be generated after | sh           attaching the image. Optional parameter. |
| oldItemI     The resource ID from which the trailer image should be | d            copied. Optional parameter. |
| oldTagId | The trailer ID the image of which should be copied. Optional parameter. |
| To upload an image, use a POST request with multiple contents | (multipart/form-data), where one part contains the parameters and the other contains the image. |
| Example: |  |
| Ljl26xgAWBYzO713 | Request URL:https: //hst-api.wialon.com/wialon/ajax.html?svc=resou rce/upload_trailer_image Request Method: POST Host: hst-api.wialon.com Connection: keep-alive Content-Length: 31756 Cache-Control: no-cache Content-Type: multipart/form-data; boundary=----WebKitFormBoundary Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*; q=0.8 Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3 Accept-Encoding: gzip,deflate,sdch Accept-Language: ru,en-US;q=0.8,en;q=0.6 |
| ------WebKitFormBoundaryLjl26xgAWBYzO713 | Content-Disposition: form-data; name="params" |

```json
{"itemId":717314,"trailerId":6,"eventHash":"jUploadForm13727689359
31"}
------WebKitFormBoundaryLjl26xgAWBYzO713
Content-Disposition: form-data; name="eventHash"

jUploadForm1372768935931
------WebKitFormBoundaryLjl26xgAWBYzO713
Content-Disposition: form-data; name="trailers_dlg_props_upload_image"; filename="image.jpg"
Content-Type: image/jpeg

------WebKitFormBoundaryLjl26xgAWBYzO713--
```

It is also possible to copy an image from another trailer. To do this, execute
a request with no image but with the oldItemId and oldTagId fields.

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired | ACL (ADF_ACL_AVL_RES_EDIT_TRAILERS) or the item/trailer 7 with the old_id not found (when copying the image from another trailer). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |
| To make sure that the image has been uploaded, execute | the avl_evts request: |

```json
{
         "tm":<uint>,                                   /* current servertime (UTC) */
         "events":[
                 {
                           "i":<long>,                          /* trailer
ID (-1 if unknown) */
                           "d":{                                /* data */
                                     "hash":"<text>"            /* the uploading is complete */

                           }
                }
        ]
}
```

## upload_zone_image

The upload_zone_image function is used to attach an image to a
geofence as well as to copy an image from one geofence to another.

```http
svc=resource/upload_zone_image&params={"itemId":<long>,

"id":<long>,

"eventHash":"<text>",

"oldItemId":<long>,

"oldZoneId":<uint>}
                               &sid="<text>"
```

To delete an image, use the update_zone function.

To get an image, use avl_zone_image function.

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Geofence ID. |
| eventHa     The event name which should be generated after | sh          uploading the image. |
| oldItemI    The resource ID of the geofence the image of which | d           should be applied. Optional parameter. |
| oldZoneI    The ID of the geofence the image of which should be | d           applied. Optional parameter. |
| To upload an image, use a POST request with multiple parameters | (multipart/form-data), where one part contains parameters and the other contains the image. |
| Example: |  |
| X2W1y7AVnQkXQAM0 | Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=resou rce/upload_zone_image Request Method: POST Host: hst-api.wialon.com Connection: keep-alive Content-Length: 31753 Cache-Control: no-cache Content-Type: multipart/form-data; boundary=----WebKitFormBoundary Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*; q=0.8 Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3 Accept-Encoding: gzip,deflate,sdch Accept-Language: ru,en-US;q=0.8,en;q=0.6 |
| ------WebKitFormBoundaryX2W1y7AVnQkXQAM0 | Content-Disposition: form-data; name="params" |

```json
{"itemId":717314,"id":1,"eventHash":"jUploadForm1372768029714"}
------WebKitFormBoundaryX2W1y7AVnQkXQAM0
Content-Disposition: form-data; name="eventHash"

jUploadForm1372768029714
------WebKitFormBoundaryX2W1y7AVnQkXQAM0
Content-Disposition: form-data; name="zone_create_upload_image"; filename="zZeVUgLEJXE.jpg"
Content-Type: image/jpeg

------WebKitFormBoundaryX2W1y7AVnQkXQAM0--
```

It is also possible to copy an image from one geofence to another. To do it,
execute a request without an image, but with the oldItemId and
oldZoneId fields.

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | (ADF_ACL_AVL_RES_EDIT_ZONES) or the item/geofence with 7 the oldItemId or oldZoneId not found (when copying image from another geofence). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |
| To make sure that the image has been uploaded, execute the | avl_evts request: |

```json
{
        "tm":<uint>,                                /* current servertime (UTC) */
        "events":[
                 {
                          "i":<long>,                       /* geofence ID (-1 if unknown) */
                          "d":{                             /* data */
                                    "hash":"<text>" /* the uploading is complete */
                          }
                 }
        ]
}
```
