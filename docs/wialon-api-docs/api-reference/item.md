# item

This section describes the general methods that can be applied to any item
in Wialon: unit, unit group, user, retranslator, resource (account), route. For
creating items, see the core section.

## add_log_record

The add_log_record function is used to add a log record.

```http
svc=item/add_log_record&params={"itemId":<long>,
                                                                          "action":"<text>",
                                                                          "newValue":"<text>",
                                                                          "oldValue":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Item ID. |
| action | Action ID written to the item log. See the list of available actions below. |
| newVal      Action-specific parameter #1 (stored as log parameter p1). | ue          Its meaning depends on action. |
| ue | Action-specific parameter #2 (stored as log parameter p2). oldVal Its meaning depends on action; may be empty for many actions. |
| Below are available actions and the corresponding log record text. |  |

## General

Action       Action
Action text
ID           description

custom_ms
Manual record       Manual record: ‘%s’.
g

create_un
Item creation       Unit ‘%s’ created.
it

create_us
Item creation       User ‘%s’ created.
er

create_gr
Item creation       Unit group ‘%s’ created.
oup

create_re
Item creation       Resource ‘%s’ created.
source

create_ac
Item creation       Account ‘%s’ created.
count

delete_it
Item deletion       Item ‘%s’ deleted.
em

delete_ac
Item deletion       Account ‘%s’ deleted.
count

update_na
Name change         Name changed from ‘%s’ to ‘%s’.
me

Action         Action
Action text
ID             description

Access to *** ‘%s’ changed (***
update_ac
Access change     stands for user, unit, unit group,
cess
resource, route, or user access rights).

## Unit properties

Action
Action ID                                    Action text
description

update_unit_
Icon change                 Unit icon changed.
icon

update_unit_     Access password
Access password changed.
pass             change

update_unit_     Phone number                Phone number changed from
phone            change                      ‘%s’ to ‘%s’.

update_unit_     Phone number                Second phone number
phone2           change                      changed from ‘%s’ to ‘%s’.

update_unit_                                 Unique ID changed from ‘%s’ to
Unique ID change
uid                                          ‘%s’.

update_unit_                                 Second unique ID changed
Unique ID change
uid2                                         from ‘%s’ to ‘%s’.

update_unit_                                 Device type changed from ‘%s’
Device change
hw                                           to ‘%s’.

Action
Action ID                                    Action text
description

update_unit_
Device change               Device configuration changed.
hw_cfg

## Counters

Action
Action ID                                             Action text
description

update_unit_calcflags
Calculation flags
(updating the sensor           Counters
changed.
calculation settings)

Mileage counter
update_unit_milcounter         Counters               changed from %d %s
to %d %s.

update_unit_bytecounter                               GPRS traffic counter
(updating the value of the     Counters               changed from %d KB
GPRS traffic counter)                                 to %d KB.

Engine hours counter
update_unit_ehcounter          Counters               changed from %.2f h
to %.2f h.

## Report and track settings

Action
Action ID                                 Action text
description

update_unit_drat (driver    Report        Driver activity source
activity)                   settings      changed.

Report        Fuel consumption
update_unit_fuel_cfg
settings      settings changed.

Report        Trip detector settings
update_unit_trip_cfg
settings      changed.

update_unit_report_cfg
Report        Unit report settings
(updating the parameters
settings      changed.
used in reports)

update_msgs_filter_cfg
(updating the filtration    Report        Message filtration
settings of the unit        settings      settings changed.
location in messages)

Measurement
system changed to
Report           %s.
convert_measure_units
settings
Conversion to the
%s.

update_track_color_settin   Tracks
g
Track colour
settings changed to
“By trips”.

Track colour
settings changed to
“Single”.

Action
Action ID                                   Action text
description

Track colour
settings changed to
“By speed”.
Track colour
settings changed to
“By sensor”.

## Sensors

Action ID        Action description        Action text

create_sensor    Sensors                   Sensor ‘%s’ created.

update_sensor    Sensors                   Sensor ‘%s’ modified.

delete_sensor    Sensors                   Sensor ‘%s’ deleted.

## Commands

Action ID       Action description       Action text

create_alias    Commands                 Command ‘%s’ created.

update_alias    Commands                 Command ‘%s’ modified.

delete_alias    Commands                 Command ‘%s’ deleted.

## Service intervals

Action
Action ID                                 Action text
description

create_service_int                        Service interval ‘%s’
Service intervals
erval                                     created.

update_service_int                        Service interval ‘%s’
Service intervals
erval                                     modified.

delete_service_int                        Service interval ‘%s’
Service intervals
erval                                     deleted.

## Fields

Action
Action ID                                 Action text
description

create_custom_fiel                        Custom field ‘%s’
Fields
d                                         created.

update_custom_fiel                        Custom field ‘%s’
Fields
d                                         modified.

delete_custom_fiel                        Custom field ‘%s’
Fields
d                                         deleted.

create_admin_field   Fields               Admin field ‘%s’ created.

Admin field ‘%s’
update_admin_field   Fields
modified.

Action
Action ID                                 Action text
description

delete_admin_field   Fields               Admin field ‘%s’ deleted.

update_profile_fie                        Profile field ‘%s’
Fields
ld                                        modified.

delete_profile_fie
Fields               Profile field ‘%s’ deleted.
ld

## Import and export

Action ID            Action description     Action text

import_item_cfg      Import                 Properties imported.

import_unit_cfg      Import                 Properties imported.

import_unit_msgs     Import                 Messages imported.

export_unit_msgs     Export                 Messages exported.

## Messages

Action
Action ID                       Action text
description

Deleted *** message dated %s (***
delete_uni      Message
stands for SMS, command, event, or
t_msg           deletion
data).

Deleted %s *** messages (***
delete_uni      Message
stands for SMS, command, event, or
t_msgs          deletion
data).

## Drivers

Action
Action ID                                      Action text
description

Driver ‘%s’ was
bind_unit_driver              Drivers
assigned at ‘%s’.

Driver ‘%s’ was
unbind_unit_driver            Drivers
separated at ‘%s’.

create_driver                 Drivers          Driver ‘%s’ created.

update_driver                 Drivers          Driver ‘%s’ updated.

delete_driver                 Drivers          Driver ‘%s’ deleted.

driver_reset_image            Drivers          Driver ‘%s’ updated.

Message dated %s
delete_driver_msg             Drivers          from driver ‘%s’
deleted.

Action
Action ID                                     Action text
description

Group of drivers
create_drivers_group            Drivers
‘%s’ created.

Group of drivers
update_drivers_group            Drivers
‘%s’ updated.

Group of drivers
delete_drivers_group            Drivers
‘%s’ deleted.

Unit attached to
the resource of
drivers ‘%s’.
Unit removed
update_driver_units
Change of       from the
(updating the list of drivers
group           resource of
that should be assigned to
members         drivers ‘%s’.
units automatically)
Automatic
assignment list
of drivers
updated.

## Trailers

Action
Action ID                                     Action text
description

Trailer ‘%s’ was
bind_unit_trailer               Trailers
assigned at ‘%s’.

Action
Action ID                                      Action text
description

Trailer ‘%s’ was
unbind_unit_trailer              Trailers
separated at ‘%s’.

create_trailer                   Trailers      Trailer ‘%s’ created.

update_trailer                   Trailers      Trailer ‘%s’ updated.

delete_trailer                   Trailers      Trailer ‘%s’ deleted.

trailer_reset_image              Trailers      Trailer ‘%s’ updated.

Message dated %s
delete_trailer_msg               Trailers      from trailer ‘%s’
deleted.

Group of trailers
create_trailers_group            Trailers
‘%s’ created.

Group of trailers
update_trailers_group            Trailers
‘%s’ updated.

Group of trailers
delete_trailers_group            Trailers
‘%s’ deleted.

update_trailer_units             Change of
(updating the list of trailers   group            Unit attached to
the resource of
that should be assigned to       members
trailers ‘%s’.
units automatically)
Unit removed
from the
resource of
trailers ‘%s’.

Automatic
assignment list

Action
Action ID                                         Action text
description

of trailers
updated.

## Passengers

Action
Action ID                           Action text
description

bind_unit_ta                        Passenger ‘%s’ was assigned at
Passengers
g                                   ‘%s’.

unbind_unit_                        Passenger ‘%s’ was separated at
Passengers
tag                                 ‘%s’.

create_tag     Tags                 Passenger ‘%s’ created.

update_tag     Tags                 Passenger ‘%s’ updated.

tag_reset_im
Tags                 Passenger ‘%s’ updated.
age

delete_tag     Tags                 Passenger ‘%s’ deleted.

delete_tag_m                        Message dated %s from
Tags
sg                                  passenger ‘%s’ deleted.

update_tag_u                        Automatic assignment list of
Tags
nits                                passengers updated.

## User settings

Action
Action ID                                  Action text
description

update_hosts_mas                           Host mask changed to
User settings
k                                          ‘%s’.

update_user_pass    User settings          User password changed.

update_user_flag
User settings          User flags changed.
s

update_user_loca
User settings          First day of week changed.
le

create_user_noti
User settings          Notice to the user: ‘%s’.
fy

delete_user_noti                           User notification ‘%s’
User settings
fy                                         deleted.

## Unit groups

Action
Action ID                                          Action text
description

units_group                    Change of
Unit added to
(adding/removing units         group members
the group ‘%s’.
to/from a unit group)
Unit removed
from the group
‘%s’.

Action
Action ID                                            Action text
description

Units in group
updated.

## Geofences

Action
Action ID                                 Action text
description

create_zone       Geofences               Geofence ‘%s’ created.

update_zone       Geofences               Geofence ‘%s’ updated.

delete_zone       Geofences               Geofence ‘%s’ deleted.

import_zones      Geofences               Geofences imported.

create_zones_gr                           Group of geofences ‘%s’
Geofences
oup                                       created.

update_zones_gr                           Group of geofences ‘%s’
Geofences
oup                                       updated.

delete_zones_gr
Geofences               Group of geofences deleted.
oup

zone_reset_imag
Geofences               Geofence ‘%s’ updated.
e

## Jobs

Action ID      Action description             Action text

create_job     Jobs                           Job ‘%s’ created.

switch_job     Jobs                           Job ‘%s’ switched on/off.

update_job     Jobs                           Job ‘%s’ updated.

delete_job     Jobs                           Job ‘%s’ deleted.

## Notifications

Action
Action ID                                  Action text
description

create_notif
Notifications               Notification ‘%s’ created.
y

switch_notif                               Notification ‘%s’ switched
Notifications
y                                          on/off.

update_notif
Notifications               Notification ‘%s’ updated.
y

delete_notif
Notifications               Notification ‘%s’ deleted.
y

## Report templates

Action
Action ID                                    Action text
description

create_repor
Report templates          Report template ‘%s’ created.
t

update_repor                                 Report template ‘%s’
Report templates
t                                            updated.

delete_repor
Report templates          Report template ‘%s’ deleted.
t

## Retranslators

Action
Action ID                                    Action text
description

create_retransla
Retranslators          Retranslator ‘%s’ created.
tor

update_retransla
Retranslators          Properties updated.
tor

units_retranslat
Retranslators          Units updated.
or

switch_retransla
Retranslators          Started/Stopped.
tor

msgs_history_ret                             Past period retranslator
Retranslators
ranslator                                    started/stopped.

## Routes

Action
Action ID                                     Action text
description

create_route         Routes                   Route ‘%s’ created.

update_route_point
Routes                   Check points updated.
s

update_route_cfg     Routes                   Properties updated.

create_round         Routes                   Ride ‘%s’ created.

update_round         Routes                   Ride ‘%s’ updated.

delete_round         Routes                   Ride ‘%s’ deleted.

create_schedule      Routes                   Schedule ‘%s’ created.

Schedule ‘%s’
update_schedule      Routes
updated.

delete_schedule      Routes                   Schedule ‘%s’ deleted.

## Accounts

Action
Action ID                                  Action text
description

Account changed from ‘%s’
change_account       Account
to ‘%s’.

Action
Action ID                                  Action text
description

Account
switch_account       Account
blocked/unblocked.

update_dealer_righ                         Dealer rights
Account
ts                                         enabled/disabled.

Payment or days
do_payment           Account
registered.

update_account_fla
Account               Account flags changed.
gs

update_account_blo                         Balance to block account
Account
ck_balance                                 changed.

update_account_den                         Balance to limit activity
Account
y_balance                                  changed.

update_account_min                         Minimum days counter
Account
_days                                      changed.

update_account_pla                         Billing plan changed to
Account
n                                          ‘%s’.

update_account_his                         History period changed to
Account
tory_period                                ‘%s’.

update_account_sub
Account               List of subplans changed.
plans

update_service       Account               Service ‘%s’ updated.

## Orders

Action
Action ID                                   Action text
description

create_order        Orders                  Order ‘%s’ created.

update_order        Orders                  Order ‘%s’ updated.

delete_order        Orders                  Order ‘%s’ deleted.

create_order_rout                           Order route ‘%s’
Orders
e                                           created.

update_order_rout                           Order route ‘%s’
Orders
e                                           updated.

delete_order_rout                           Order route ‘%s’
Orders
e                                           deleted.

## Criteria

Action ID            Action description          Action text

criteria_updated     Criteria                    Criteria updated.

## Unit deactivation and activation

Action
Action description              Action text
ID

0: Unit was deactivated.

set_acti                                        1: Unit was activated.
Activation/Deactivation
ve
2: Unit was activated
automatically.

set_active is written for the unit specified by itemId; the newValue
parameter (log p1) stores the activation state: 0 = deactivated, 1 =
activated, 2 = automatically activated.

## Notices about expiring activation codes

Action ID      Action description                      Action text

create_no      Creating a notice about the             Notice ‘%s’ created
tice           activation code expiration              for the user.

update_no      Updating a notice about the             Notice ‘%s’ updated
tice           activation code expiration              for the user.

delete_no      Deleting a notice about the
Notice ‘%s’ deleted.
tice           activation code expiration

The actions with notices about the expiration of activation codes are
recorded in the log of each notice recipient. For each action, the
item/add_log_record request is sent with the following parameters:

action             itemId                     newValue          oldValue

create_notice      Recipient user ID          Notice name       "" (empty)

update_notice      Recipient user ID          New notice name   "" (empty)

delete_notice      Recipient user ID          Notice name       "" (empty)

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_ITEM_MANAGE_LOG). |
| 4 | Wrong input parameters. |

## delete_item

The delete_item function is used to delete an item.

### Endpoint

To delete objects in Wialon Hosting or Local, use the following signature:

```http
svc=item/delete_item
&params={
    "itemId": <long>
}
```

To delete 10 or more units in Wialon Hosting, use the signature

```http
svc=item/delete_item
&params={
    "itemId": <long>,
    "reasons": [{"reason_key"}]
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| itemId | ID of the item you want to delete. |
| reasons | Array of unit deletion reasons. A reason is required when deleting 10 or more units in Wialon Hosting. For keys of deletion reasons and their descriptions, see account/delete_account. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_ITEM_DELETE) or billing account not allowed. |
| 4 | Wrong input parameters. |

## get_backup

The get_backup function is used to get an automatic backup file for a
specified element.

```http
svc=item/get_backup&params={"itemId":<long>,
                                                         "fileId":
<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Item ID. |
| fileId | File ID. |

## Returned result

```json
{
          "result": {
                             "date":"<text>",               /* date */
                             "t":<uint>,                    /* createtime */
                             "unitId":<long>,      /* unit ID */
                             "id":<long>,          /* file ID */
                             "name":                        /* file name */
                             "content":                     /* backupfile contents */
                   },
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |
| 4          Wrong input parameters or failed to fetch the item with the | desired ACL: |
| Unit/Unit group — ADF_ACL_ITEM_DELETE, | ADF_ACL_ITEM_EDIT_AFIELDS, ADF_ACL_ITEM_EDIT_CFIELDS, ADF_ACL_ITEM_EDIT_FILE, ADF_ACL_ITEM_EDIT_IMAGE, ADF_ACL_ITEM_EDIT_NAME, ADF_ACL_ITEM_EDIT_OTHER, ADF_ACL_AVL_UNIT_EDIT_CMD_ALIASES, ADF_ACL_AVL_UNIT_EDIT_COUNTERS, ADF_ACL_AVL_UNIT_EDIT_HW, ADF_ACL_AVL_UNIT_REG_EVENTS, ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS, |
| ADF_ACL_AVL_UNIT_EDIT_SENSORS, | ADF_ACL_AVL_UNIT_EDIT_MAINTENANCE; Resource — ADF_ACL_ITEM_DELETE, ADF_ACL_ITEM_EDIT_FILE, ADF_ACL_AVL_RES_EDIT_DRIVERS, ADF_ACL_AVL_RES_EDIT_JOBS, ADF_ACL_AVL_RES_EDIT_NF, ADF_ACL_AVL_RES_EDIT_POI, ADF_ACL_AVL_RES_EDIT_REPORTS, ADF_ACL_AVL_RES_EDIT_TRAILERS, ADF_ACL_AVL_RES_EDIT_ZONES; User — ADF_ACL_ITEM_DELETE, ADF_ACL_USER_SET_ITEMS_ACCESS, ADF_ACL_USER_OPERATE_AS, ADF_ACL_USER_EDIT_FLAGS; Route — ADF_ACL_ITEM_DELETE, ADF_ACL_AVL_ROUTE_EDIT_SETTINGS; Retranslator — ADF_ACL_ITEM_DELETE, ADF_ACL_AVL_RETR_EDIT_SETTINGS, ADF_ACL_AVL_RETR_EDIT_UNITS; Other — ADF_ACL_ITEM_DELETE, ADF_ACL_ITEM_EDIT_NAME, ADF_ACL_ITEM_EDIT_CFIELDS, ADF_ACL_ITEM_EDIT_OTHER, ADF_ACL_ITEM_EDIT_SUB_ITEMS, ADF_ACL_ITEM_EDIT_AFIELDS, ADF_ACL_ITEM_EDIT_FILE, ADF_ACL_AVL_UNIT_EDIT_HW, ADF_ACL_AVL_UNIT_EDIT_SENSORS, ADF_ACL_AVL_UNIT_EDIT_COUNTERS, ADF_ACL_AVL_UNIT_EDIT_MAINTENANCE, ADF_ACL_AVL_UNIT_EDIT_CMD_ALIASES, ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS. |

## list_backups

The list_backups function is used to see all the automatic backup files.

```http
svc=item/list_backups&params={"itemId":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Item ID. |

## Returned result

```json
{
        "result": [
                 {
                       "date":"<text>",                  /* date */
                       "t":<uint>,                       /* creation time */
                       "unitId":<long>,          /* unit ID */
                       "id":<long>,              /* file ID */
                       "name":                           /* file name */
                 },
                 ...
        ]
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 7 | Failed to fetch the item with the desired ACL: |
| Unit/Unit proup — ADF_ACL_ITEM_DELETE, | ADF_ACL_ITEM_EDIT_AFIELDS, ADF_ACL_ITEM_EDIT_CFIELDS, ADF_ACL_ITEM_EDIT_FILE, ADF_ACL_ITEM_EDIT_IMAGE, ADF_ACL_ITEM_EDIT_NAME, ADF_ACL_ITEM_EDIT_OTHER, ADF_ACL_AVL_UNIT_EDIT_CMD_ALIASES, ADF_ACL_AVL_UNIT_EDIT_COUNTERS, ADF_ACL_AVL_UNIT_EDIT_HW, ADF_ACL_AVL_UNIT_REG_EVENTS, ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS, ADF_ACL_AVL_UNIT_EDIT_SENSORS, ADF_ACL_AVL_UNIT_EDIT_MAINTENANCE; |
| Resource — ADF_ACL_ITEM_DELETE, | ADF_ACL_ITEM_EDIT_FILE, ADF_ACL_AVL_RES_EDIT_DRIVERS, ADF_ACL_AVL_RES_EDIT_JOBS, ADF_ACL_AVL_RES_EDIT_NF, ADF_ACL_AVL_RES_EDIT_POI, ADF_ACL_AVL_RES_EDIT_REPORTS, ADF_ACL_AVL_RES_EDIT_TRAILERS, ADF_ACL_AVL_RES_EDIT_ZONES; |
| User — ADF_ACL_ITEM_DELETE, | ADF_ACL_USER_SET_ITEMS_ACCESS, ADF_ACL_USER_OPERATE_AS, ADF_ACL_USER_EDIT_FLAGS; Route — ADF_ACL_ITEM_DELETE, ADF_ACL_AVL_ROUTE_EDIT_SETTINGS; Retranslator — ADF_ACL_ITEM_DELETE, ADF_ACL_AVL_RETR_EDIT_SETTINGS, ADF_ACL_AVL_RETR_EDIT_UNITS; |
| Other — ADF_ACL_ITEM_DELETE, | ADF_ACL_ITEM_EDIT_NAME, ADF_ACL_ITEM_EDIT_CFIELDS, ADF_ACL_ITEM_EDIT_OTHER, ADF_ACL_ITEM_EDIT_SUB_ITEMS, ADF_ACL_ITEM_EDIT_AFIELDS, ADF_ACL_ITEM_EDIT_FILE, ADF_ACL_AVL_UNIT_EDIT_HW, ADF_ACL_AVL_UNIT_EDIT_SENSORS, ADF_ACL_AVL_UNIT_EDIT_COUNTERS, |
| ADF_ACL_AVL_UNIT_EDIT_MAINTENANCE, | ADF_ACL_AVL_UNIT_EDIT_CMD_ALIASES, ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS. |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## restore_icons

The restore_icons function is used to restore the icons of an item.

```http
svc=item/restore_icons&params={"resId":<long>,
                                                      "trailerIcons":
{<long>:"<text>"},
                                                      "driverIcons":
{<long>:"<text>"},
                                                      "zoneIcons":{<long>:"<text>"},
                                                      "unitIcons":{<long>:"<text>"}}
```

is the item/propitem ID.
is the icon URL on the backup server.

You can restore icons for several items at a time,
separating their ID-URL pairs by commas.

### Parameters

| Name | Description |
| --- | --- |
| resId | Resource ID. |
| trailerIcons | Trailer icon parameters. |
| driverIcons | Driver icon parameters. |
| zoneIcons | Geofence icon parameters. |
| unitIcons | Unit icon parameters. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the resource with the desired ACL | (ADF_ACL_AVL_RES_EDIT_ZONES or 7 ADF_ACL_AVL_RES_EDIT_DRIVERS or ADF_ACL_AVL_RES_EDIT_TRAILERS). |
| 4 | Wrong input parameters. |

## update_admin_field

The update_admin_field function is used to create, update, or delete
admin fields.

```http
svc=item/update_admin_field&params={"itemId":<long>,
                                                                           "id":<long>,
                                                                           "callMode":"<text>",

"n":"<text>",

"v":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Item ID. |
| id | Admin field ID. It is not taken into account during the creation, the admin field IDs are generated by the system. |
| Action: |  |
| callMo | create; de               update; |
| delete. |  |
| The following parameters are only required to create and update admin | fields: |
| Name | Description |
| n | Admin field name. |
| v | Admin field value. |

## Returned result

When creating or updating admin fields, the returned result is as follows:

```json
[
        <long>,                               /* admin field ID */
        {
                  "id":<long>,      /* admin field ID */
                  "n":"<text>",               /* name */
                  "v":"<text>"                /* value */
        }
]
```

When deleting admin fields, the returned result is as follows:

```json
[
        <long>,           /* administrative field ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| 7         Failed to fetch the item with the desired ACL | (ADF_ACL_ITEM_VIEW_AFIELDS, |
| ADF_ACL_ITEM_EDIT_AFIELDS). |  |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_custom_field

The update_custom_field function is used to create, update, or delete
custom fields.

```http
svc=item/update_custom_field&params={"itemId":<long>,

"id":<long>,

"callMode":"<text>"

"n":"<text>",

"v":"<text>"}
```

### Parameters

Name       Parameter

itemId     Item ID.

Custom field ID. It is not taken into account during the
id
creation, the custom field IDs are generated by the system.

Action:

create;
callMo
de              update;
delete.

The following parameters are only required to create and update custom
fields:

Name                      Parameter

n                         Custom field name.

v                         Custom field value.

## Returned result

When creating or updating custom fields, the returned result is as follows:

```json
[
        <long>,            /* custom field ID */
        {
                  "id":<long>,      /* custom field ID */
                  "n":"<text>",     /* name */
                  "v":"<text>"      /* value */
        }
]
```

When deleting custom fields, the returned result is as follows:

```json
[
        <long>,             /* custom field ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired ACL | 7         (ADF_ACL_ITEM_VIEW_CFIELDS, ADF_ACL_ITEM_EDIT_CFIELDS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_custom_property

The update_custom_property function is used to create a custom
property for an item or to update an existing one.

```http
svc=item/update_custom_property&params={"itemId":<long>,

"name":"<text>",

"value":"<text>"}
```

To delete a custom property, use the same function but with an empty
value parameter:

```http
svc=item/update_custom_property&params={"itemId":<long>,

"name":"<text>",

"value":""}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Item ID. |
| name | Custom property name. |
| value | Custom property value. |

## Returned result

```json
{
        "n":"<text>",     /* custom property name */
        "v":"<text>"      /* custom property value */
}
```

Possible error codes:

| Name | Description |
| --- | --- |
| Failed to fetch the item with the desired ACL | 7 (ADF_ACL_ITEM_EDIT_OTHER). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_fleetio_tokens

To update fleetio tokens, use the item/update_fleetio_tokens method:

svc=item/update_fleetio_tokens&params={

```json
"itemId": long,
"auth_token": "text",
"account_token": "text"
```

}
&sid= text

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Account ID. |
| auth_token | Authorization token. |
| account_token | Fleetio account token. |

### Example

Below is an example of the item/update_fleetio_tokens request.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=item/update_fleetio_tokens&params={"itemId":912,"auth_token":"auth_token value","account_token":"account_token value"}&sid=f0c4b586ec1ebb4bc2694766effbc1b3
```

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{   "auth": "auth_token",   "act": "account_token"}
```

Otherwise, error code 7 is returned, indicating that the user doesn’t have
the required access right to the account
(ADF_ACL_AVL_RES_MANAGE_ACCOUNT).

## update_ftp_property

The update_ftp_property function is used to update custom FTP settings.

```http
svc=item/update_ftp_property&params={"itemId":<long>,

"host":"<text>",

"login":"<text>",

"pass":"<text>",

"path":"<text>",
```

"check":<uint>,

"hostingFtp":<uint>}

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| host | FTP URL. |
| login | FTP login. |
| pass | FTP password. |
| path | Directory path. |
| Valid FTP settings: |  |
| check                   0 — no; | 1 — yes. |
| Send data to the Wialon Hosting FTP: |  |
| hostingFtp              0 — no; | 1 — yes. |
| To send data to custom FTP, the “hostingFtp” value should | be 0, the “check” value — 1. |

## Returned result

```json
{
    "hs":"<text>",          /* FTP URL */
    "lg":"<text>",          /* FTP login */
    "pt":"<text>",          /* directory path */
    "ch":<uint>, /* valid FTP settings */
    "tp":<uint>   /* send data to the Wialon Hosting FTP */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired | 7 ACL(ADF_ACL_ITEM_EDIT_OTHER). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## update_measure_units

The update_measure_units function is used to change the measurement
system of an item.

```http
svc=item/update_measure_units&params={"itemId":<long>,

"type":<uint>,

"flags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Item ID. |
| Target measurement system: |  |
| type | 0 — Metric; 1 — U. S.; 2 — Imperial. |
| flags | 0 — set the unit of measurement; 1 — convert the values and set the unit of measurement. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired ACL | 7        (ADF_ACL_ITEM_EDIT_OTHER), failed to fetch the user or "not a top user" error. |
| 6 | New type == old type or undefined error. |
| 4 | Wrong input parameters. |

## update_name

The update_name function is used to rename an item.

svc=item/update_name&params={"itemId":<long>,

```json
"name":"<text>"}
```

### Parameters

Name            Desription

itemId          Item ID.

name            The new name (4-50 characters).

## Returned result

{

```json
       "nm":"<text>"     /* new item name */

}
```

Possible error codes:

Code      description

Failed to fetch the item with the desired ACL
7
(ADF_ACL_ITEM_EDIT_NAME).

6         Undefined error.

4         Wrong input parameters.

## update_profile_field

The update_profile_field function is used to update profile fields.

```http
svc=item/update_profile_field&params={"itemId":<long>,

"n":"<text>",

"v":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Item ID. |
| n | Profile field name. |
| v | Profile field value. |
| You can use the following profile fields: |  |
| Name | Description |
| vehicle_type | Vehicle type. |
| vehicle_class | Vehicle class. |
| vin | VIN. |
| registration_plate | Registration plate. |
| brand | Brand. |
| model | Model. |
| year | Year. |
| color | Colour. |
| engine_model | Engine model. |
| engine_power | Engine power, kW. |
| engine_displacement | Engine displacement, ccm. |
| primary_fuel_type | Primary fuel type. |
| co2_emission | Average CO2 emission. |
| cargo_type | Cargo type |
| carrying_capacity | Carrying capacity, t. |
| width | Width, mm. |
| height | Height, mm. |
| depth | Depth, mm. |
| effective_capacity | Effective capacity. |
| gross_vehicle_weight | Gross vehicle weight. |
| axles | Axles. |

## Returned result

```json
[
        <long>,            /* field ID */
        {
                   "id":<long>,      /* field ID */
                   "n":"<text>",     /* field name */
                   "v":"<text>"      /* field value */
        }
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch item with desired ACL | 7         (ADF_ACL_ITEM_VIEW_CFIELDS, ADF_ACL_ITEM_EDIT_CFIELDS). |
| 6 | Undefined error. |
| 3 | AVL server item not found or type library plugin not enabled. |
| 4 | Wrong input parameters. |
