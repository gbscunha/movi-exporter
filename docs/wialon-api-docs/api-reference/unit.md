# unit

This section describes the methods for working with units. The creation of
units is described here.

## activity_settings

The default source of driver activity are assignments and trips. To set a
different source, use the unit/update_activity_settings method.

```http
svc=unit/update_activity_settings&params={"itemId":<long>,
                                                "type":<int>}
```

### Parameters

| Parameter | Description |
| --- | --- |
| itemId | Unit ID |
| Source type. The following types can be used: |  |
| type | 0 - none 1 - assignments 2 - tachograph |

### Response

If the request is completed successfully, the response is empty.

```json
{ }
```

Otherwise, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 6 | Failed to set a new type. |
| Failed to fetch the item because the user doesn't have the | 7         required access right to it (ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS) |

## Getting the selected source

To get the selected activity source, use the
unit/get_activity_settings method.

```http
svc=unit/get_activity_settings&params={"itemId":<long>}
```

### Response

If the request is completed successfully, the response contains the source
type.

```json
{
"type": <int>             /* selected source */
}
```

Otherwise, the response contains error code 7: failed to fetch the
report object and resource because the used doesn’t have the required
access right to them (ADF_ACL_ITEM_VIEW_PROPERTIES).

## add_video_packets

To add video traffic packages to a unit, use
the unit/add_video_packets method. Dealer rights are required to
complete the request.

```http
svc=unit/add_video_packets&params={
        "units":[<long>,...],
        "packets":<int>
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| units | Array of unit IDs. |
| packets | Number of added packages. |

### Example

```http
svc=unit/add_video_packets&params={"units":[5523461,1548776],"packets":1}
```

### Response

If the request is completed successfully, unit IDs with response codes are
returned. The value 0 in the code means that the changes have been
applied.

```json
[
          {result:{5523461:{code:0}}},
          {result:{1548776:{code:0}}}
]
```

If the request hasn’t been completed, an error code is returned.

### Error codes

Error code         Description

4                  Invalid input parameters.

7                  Video monitoring service not enabled.

## calc_last

To get the last known sensor values and key indicators for units, use the
unit/calc_last method.

### Endpoint

```http
svc=unit/calc_last&params={
    "itemIds": [<long>]
}
```

### Parameters

The request must contain the parameter itemIds specifying the array of
unit IDs for which you want to retrieve the last known sensor values and
indicators.

### Example

Below is an example of the unit/calc_last request.

```http
svc=unit/calc_last&params={
    "itemIds": [16091323, 16454260]
}
```

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
[
    {
        "i": <long>,           // Unit ID.

     "mileage": {            // Mileage counter.
          "value": <double>,
          "format": {
               "value": <text>     // Formatted value with units of
```

measurement (e.g., "24498.82 km").

```json
     }
},
"engine_hours": {       // Engine hours counter.
     "value": <double>,
     "format": {
          "value": <text>     // Formatted value with units of
```

measurement (e.g., "0.00 h").

```json
     }
},
"pos": {                // Last known position.
     "y": <double>,     // Latitude.
     "x": <double>,     // Longitude.
     "c": <int>,        // Course.
     "z": {             // Altitude.
          "value": <double>,
          "format": {
              "value": <text>         // Formatted value with units
```

of measurement (e.g., "139.00 m").

```json
     }
},
"s": {             // Speed.
     "value": <double>,
     "format": {
         "value": <text>         // Formatted value with units
```

of measurement (e.g., "75.00 km/h").

```json
          }
     },
     "sc": <int>        // Number of satellites.
},
"sensors": {            // Sensor values.
     "<sensor_id>": {
          "value": <double|text>,           // Raw sensor value.
          "format": {
              "value": <text>              // Formatted sensor val
```

ue with units of measurement.

```
                   }
             }
         }
    }
]
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4                 Invalid input parameters.

No View object and its basic properties access right
7
to units.

## calc_last_message

To get a sensor value from the last message, use the
unit/calc_last_message method:

```http
svc=unit/calc_last_message&params={"unitId":<long>,
                                         "sensors":[<long>],
                                         "flags":<uint>}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| unitId* | Unit ID. |
| sensors | Array of sensor IDs. If this parameter is not specified or empty, the values of all sensors are returned. |
| flags | Flags. If this parameter is set to 1, the sensor value is calculated using the last valid parameter value. |

### Response

If the request is completed successfully, the sensor value is returned.

```json
{
         <text>:<double|text>,      /* sensor ID: sensor value */...
}
```

Otherwise, an error code is returned.

### Error codes

| Parameter | Description |
| --- | --- |
| Failed to fetch the unit because the user doesn't have | 4               the required access right (ADF_ACL_AVL_UNIT_VIEW_SENSORS). |
| 7 | Failed to fetch the unit sensors. |

## calc_sensors

To get sensor values, use the unit/calc_sensors method.

```http
svc=unit/calc_sensors&params={"source":<text>,
                               "indexFrom":<uint>,
                               "indexTo":<uint>,
                               "unitId":<long>,
                               "sensorId":<long>,
                               "width":<uint>}
```

### Parameters

| Parameter | Description |
| --- | --- |
| source | Source of messages (layer name). If this parameter is empty, the message loader is used by default. |
| m | indexFro Index of the first message. |
| indexTo | Index of the last message. |
| unitId | Unit ID. |
| sensorId | Sensor ID. If set to 0, the values of all sensors are returned. |
| width        Number of items to return. Optional. | This parameter is used when you need a fixed number of aggregated (i.e., preprocessed) sensor values. This is particularly useful for generating and zooming in on charts with preprocessed data. The process works as follows: |
| 1. The system retrieves all messages within the | specified bounds. 2. The system divides the entire interval into the number of subintervals specified in the width parameter. 3. Within each subinterval, the system identifies the first recorded sensor value (left), the last recorded value (right), the minimum value (bottom), and the maximum value (top). These values are then combined into the final server response. |
| If the source parameter is specified, the unitId parameter | must be specified too. If source is not specified, you can set unitId to any value. In this case, unitId is not used and messages are obtained directly from the message loader. |

### Response

If the request with no specified width is completed successfully, a
response of the following format is returned:

```json
[       /* array of message data */
        {                 /* values of sensors from one message */
                 <text>:<double|text>,       /* sensor ID: sensor value
*/...
        }
]
```

If width is specified, a response of the following format is returned:

```json
[
       [
           {
                 "name": <sensor_name>,         /* Sensor name */
                 "data": [
                     {
                           "left": [<unix_time1>, <value1>],        /* First recorded sensor value in the subinterval and its time */
                           "right": [<unix_time2>, <value2>],       /* Last recorded sensor value in the subinterval and its time */
                           "bottom": [<unix_time3>, <value3>], /* Minimumsensor value in the subinterval and its time */
                           "top": [<unix_time4>, <value4>]          /* Maximumsensor value in the subinterval and its time */
                     },
                     ...
                 ]
           },
           ...
       ]
]
```

If the request hasn’t been completed, an error code is returned.

### Error codes

Error
Description
code

One of the following errors:

Invalid input data.
4
Failed to fetch the unit messages.
Failed to fetch the unit sensors.

Failed to fetch the specified unit because the user doesn't
7          have the required access right
(ADF_ACL_AVL_UNIT_VIEW_SENSORS).

## create_task

To create a new task for a unit, use the unit/create_task method.

### Endpoint

```http
svc=unit/create_task&params={
    "itemId": <long>,
    "props": <object>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | ID of the unit for which you want to create a task. |
| props | Task properties as a JSON object. Includes the task subtype, event name, and optionally, description, assignee, priority, status, timestamps, coordinates, and specific parameters. |

## Task property parameters

The required parameters are marked with an asterisk (*).

Property
Type              Description
parameter

Task subtype. Allowed values:

21 – custom task
Integer               22 – filling
task_sub_type*
(uint8)
23 – battery
26 – maintenance

task_evt_name*         String            Event name.

task_description       String            Text description.

ID of the user to whom the task
should be assigned. Requires the
task_assignee          Long
OPERATE_AS access right to this
user.

Task priority. Allowed values:

1 – low
Integer
task_priority
(uint8)               2 – medium (default)
3 – high

Integer           Task status. Must be 1
task_status
(uint8)           (TASK_STATUS_NEW) or omitted.

task_create_time       Unsigned          UNIX timestamp of the task
integer           creation (seconds). The default
value is the current server time.
You can’t specify a future
timestamp in this parameter. If

Property
Type             Description
parameter

you do so, the task will be
created with the current server
time.

Unsigned         UNIX timestamp of the task
task_update_time
integer          update(seconds).

task_address_x                        Coordinates. Both must be
Double
task_address_y                        specified or both omitted.

Additional task parameters.
Supported keys:

filled — amount of fuel filled
charged — amount of energy
charged
task_params          Object
cost — task cost
engine_hours — vehicle
engine hours

mileage — vehicle mileage.

This parameter is ignored if
task_id                               sprecified. The server always
generates the ID automatically.

task_tags                             This parameter must be empty.

task_comments                         This parameter must be empty.

This parameter must be zero or
task_done_rejected
omitted.

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "svc_result": {},
    "svc_error": 0
}
```

If the request fails, an error code is returned.

### Error codes

Error code       Description

1                Invalid input parameters.

2                Missing Edit tasks access right to the unit.

3                Missing OPERATE_AS access right to the specified user.

4                Specified unit not found.

7                Unknown error.

## exec_cmd

To send a method to a unit, use the unit/exec_cmd request.

```http
svc=unit/exec_cmd&params={"itemId":<long>,
                             "commandName":<text>,

                              "linkType":<text>,
                              "param":<text>,
                              "timeout":<uint>,
                              "flags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Unit ID. |
| commandName | Command name. |
| linkType | Link type (see update_command_definition). |
| param | Parameters (if necessary). |
| timeout | Timeout for the command to be in the command queue, in seconds. |
| Flags for selecting a phone number to execute the | command: |
| 0 — use any (primary, then secondary); | flags                  0x1 — use primary; |
| 0x2 — use secondary; | 0x10 — send param in JSON format. |

### Response

If the request is completed successfully, an empty response is returned.

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

5           Failed to execute the command.

Failed to fetch the unit because the user doesn’t have the
7
required access right (ADF_ACL_AVL_UNIT_EXEC_CMDS).

## get_activity_settings

To find out the source of driver activity, use
the unit/get_activity_settings request.

```http
svc=unit/get_activity_settings&params={"itemId":<long>}
```

### Parameters

The request must contain the itemId parameter, which specifies the unit
ID.

### Example

Below is an example of the unit/get_activity_settings request.

```http
svc=unit/get_activity_settings&params={"itemId": 200393}
```

### Response

If the request is completed successfully, the response contains the selected
source of driver activity.

```json
{
        "type": <int> /* selected source */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4            Invalid input parameters.

6            Error specifying the settings.

The user doesn't have the required access
7
right (ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS).

## get_billing_code

To retrieve the activation code of a unit, use the unit/get_billing_code
method.

```http
svc=unit/get_billing_code&params={"itemId":<long>}
```

### Parameters

The request must include the itemId parameter, which specifies the unit
ID.

### Example

Below is an example of the unit/get_billing_code request.

```http
svc=unit/get_billing_code&params={"itemId":1133}
```

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{"guid":"bf6364e80170cbd4a42bfa8eb446deff","uid":1133,"tmc":173192
5774,"tma":1732090760,"tme":1763194760}
```

If no active codes are assigned to the unit, the last expired code is fetched.

In case the request fails, the response contains error code 7, indicating that
the user doesn’t have the required access right
(ADF_ACL_AVL_UNIT_VIEW_HW).

## get_command_definition_data

To get the command definition data, use
the unit/get_command_definition_data request.

```http
svc=unit/get_command_definition_data&params={"itemId":<long>,
                                                 "col":[<long>]}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Unit ID. |
| col | Array of command IDs. If this parameter is specified, the response is filtered by IDs. |

### Response

If the request is completed successfully, the response contains the
command definition data.

```json
[
     <long>,        /* Command ID */
     {
         "id":<long>,     /* Command ID */
         "n":<text>,      /* Command name */
         "c":<text>,      /* Command type */
         "l":<text>,      /* Link type */
         "p":<text>,      /* Parameters */

          "a":<uint>,     /* Access level */
           "f":<uint>,    /* Flags */
           "jp":<uint>    /* JSON parameters */
    }
]
```

If the request fails, the response contains error code 7, indicating that the
user does not have the required access rights
(ADF_ACL_AVL_UNIT_VIEW_CMD_ALIASES) to the unit.

## get_delete_reasons

To obtain the reasons for deleting units in Wialon Hosting, use
the unit/get_delete_reasons method. A similar method for Wialon Local
is unit/get_deleted_reasons

### Endpoint

```http
svc=unit/get_deleted_reasons
&params={
       "lang": "string"
}
&sid
```

### Parameters

No parameters are required. You can specify the optional lang parameter,
indicating the language in which you want to receive the response (en, ru,
es, and so on).

### Example

```http
svc=unit/get_deleted_reasons&params={"lang":"en"}&sid=fb1dcad80e79
266044a3a5db5d9f68f3
```

### Response

If the request is completed successfully, a response with unit deletion
reasons is returned.

```json
{
    "delayed_resolution_of_reported_bugs_partner": {    // Reason key.
        "name": "Delays in fixing reported bugs", // Reason name.
        "category": "Our initiative (the fleet remains with us)", // Reason category.
        "sub-category": "Software-related", // Reason sub-category.
        "position": 1   //Sorting index used on the front-end to determine the display order of reasons.
    }
}
```

## get_deleted_reasons

To obtain the reasons for deleting units in Wialon Local, use
the unit/get_deleted_reasons method. A similar method for Wialon
Hosting is unit/get_delete_reasons

### Endpoint

```http
svc=unit/get_deleted_reasons
&params={
}
```

### Parameters

This request contains empty parameters.

### Example

```http
svc=unit/get_deleted_reasons&params={}
```

### Response

If the request is completed successfully, a response with unit deletion
reasons is returned.

```json
{
        "reasons": [
                 1,
                 2,
                 3,
                 4,
                 5,
                 6,
                 7,
                 8,
                 9,
                 10
        ]
}
```

Unit deletion reasons include the following:

Value        Description

1            High prices

2            Lack of functionality

3            Difficult to use

4            Transfer to competitive systems

5            Contract expiration

6            Local regulations and monopolies

7            Unstable political and economic situations

8            Tender-based units

9            Seasonal units

10           Custom reason

If the request fails, the response contains error code 6, indicating that the
user ID is invalid or the user has signed out.

## get_trips

To get information about trips for a specified period, upload unit messages
and execute the unit/get_trips command.

```http
svc=unit/get_trips&params={"itemId":<long>,
                                                        "msgsSource":<text>,
                               "timeFrom":<uint>,
                               "timeTo":<uint>}
```

This request can’t be executed simultaneously with the following requests:

…/report/exec_report,

…/report/export_result,
…/report/get_result_chart,

…/report/get_result_map,
…/render/create_messages_layer,
…/messages/load_interval,
…/resource/get_driver_bindings,
…/resource/get_trailer_bindings,
all requests from the section exchange,
…/account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| itemId | Unit ID. |
| timeFrom | Interval beginning. |
| timeTo | Interval end. |
| msgsSource | Message layer name (only one layer is available). Specify 1 to use the message loader. |

### Response

If the request is completed successfully, the response contains information
about trips.

```json
[
        {
                "from": { /* Starting point of the trip */
                           "i": <unit>,      /* Message index */
                           "t": <unit>,      /* Time */

                           "p": {               /* Location */
                                      "y": <double>,      /* Latitude */
                                      "x": <double>       /* Longitude */
                           }
                  },
                  "to": { /* Ending point of the trip */
                           "i": <unit>,         /* Message index */
                           "t": <unit>,         /* Time */
                           "p": {               /* Location */
                                      "y": <double>,      /* Latitude */
                                      "x": <double>       /* Longitude */
                           }
                  },
                  "m": <double> /* Mileage (meters) */
         }
]
```

If the request fails, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 4 | Invalid item ID or input format. |
| 6 | Failed to fetch unit messages. |
| The user doesn't have the required access rights to the unit | 7 (ADF_ACL_ITEM_EXECUTE_REPORTS). |

## get_device_methods_extended_new

To obtain methods from flespi, use
the unit/get_device_methods_extended_new command.

```http
svc=unit/get_device_commands_extended_new&params={"protocolId":<uint>, "deviceTypeId":<uint>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| protocolId | Protocol ID |
| deviceTypeId | Device type ID |

### Example

Below is an example of
the unit/get_device_commands_extended_new request.

```http
svc=unit/get_device_commands_extended_new&params={"protocolId":1,
"deviceTypeId":411}
```

### Response

If the request is completed successfully, commands from flespi are
returned.

{
"result": [
{
"settings": [],
"commands": [
{
"address": ["connection"],
"examples": [
{
"description": "Send script remote command",
"properties": {
"output": 13,
"payload": "616E792062696E617279207061796C6F6164"
}
}
],
"name": "custom",
"schema": {
"additionalProperties": false,
"description": "Send custom command to device",
"properties": {
"output": {
"maximum": 14,
"minimum": 0,
"title": "Output ID",
"type": "integer"
},
"payload": {
"maxLength": 2700,
"minLength": 2,
"pattern": "^(?:[0-9A-Fa-f]{2})+$",
"title": "Hex data to be sent to the device",
"type": "string"
},
"ttl": {
"default": 86400,
"maximum": 864000,
"minimum": 10,
"title": "Command time to live in seconds",

```json
"type": "integer"
}
},
"required": ["output", "payload"],
"title": "Custom command",
"type": "object",
"x-view-order": ["output", "ttl", "payload"]
},
"tags": {
"custom": 1
}
}
]
}
]
}
```

If the request fails, an error code is returned.

### Error codes

Error code               Description

One of the following errors:

invalid format
4
invalid unit ID

#### invalid flespi device

6                        Invalid device type.

## get_drive_rank_settings

To obtain eco driving settings, use the unit/get_drive_rank_settings
command.

```http
svc=unit/get_drive_rank_settings&params={"itemId":<long>}
```

### Parameters

The request must contain the itemId parameter, which specified the unit
ID.

### Response

If the request is completed successfully, the response contains the list of
eco driving criteria and their parameters.

```json
{
        "acceleration":[...],
        "brake":[...],
        "global":{...},
        "turn":[...],
        "sensor":[...],
        "speeding":[...],
        "harsh":[...]
    }
```

For all eco driving criteria and parameters, see update_drive_rank_settings.

If no criteria are configured, an empty object is returned.

In case the request fails, the response contains error code 7, indicating that
the user doesn’t have the required access right to the unit

(ADF_ACL_ITEM_VIEW_PROPERTIES).

## get_fuel_settings

To obtain the fuel consumption settings of a unit, use the
unit/get_fuel_settings command.

```http
svc=unit/get_fuel_settings&params={"itemId":<long>}
```

### Parameters

The request must contain the itemId parameter, which specifies the unit
ID.

### Response

If the request is completed successfully, the response contains the fuel
consumption settings.

```json
{
         "calcTypes": <uint>, /* Method of calculating fuel consumption (see below) */
         "fuelLevelParams": { /* Detection of fuel fillings and drains */
                 "flags": <uint>, /* Flags for detecting fillings and drains (see below) */
                 "ignoreStayTimeout": <uint>, /* Ignore messages after the start of motion (seconds) */
                 "minFillingVolume": <double>, /* Minimum fuel filling volume (liters) */
                 "minTheftTimeout": <uint>, /* Minimum idle time todetect a fuel drain (seconds) */
                 "minTheftVolume": <double>, /* Minimum fuel drainvolume (liters) */
                 "filterQuality": <ubyte>, /* Filtering level (rang
```

e: 0-255) */

```json
"fillingsJoinInterval": <uint>, /* Timeout to sepa
```

rate consecutive fillings (seconds) */

```json
"theftsJoinInterval": <uint>, /* Timeout to separa
```

te consecutive drains (seconds) */

```json
"extraFillingTimeout": <uint> /* Timeout to detect
```

the final filling volume (seconds) */

```json
},
"fuelConsMath": { /* Fuel consumption calculation by mathe
```

matical formulas */

```json
"idling": <double>, /* Idling fuel consumption (li
```

ters per hour) */

```json
"urban": <double>, /* Urban cycle consumption (lit
```

ers per 100 km) */

```json
"suburban": <double> /* Suburban cycle consumption
```

(liters per 100 km) */

```json
},
"fuelConsRates": { /* Fuel consumption by seasonal rates
```

*/

```json
"consSummer": <double>, /* Summer consumption (lit
```

ers per 100 km) */

```json
"consWinter": <double>, /* Winter consumption (lit
```

ers per 100 km) */

```json
"winterMonthFrom": <uint>, /* Start of winter peri
```

od (month: 0-11) */

```json
"winterDayFrom": <uint>, /* Start of winter period
```

(day: 1-31) */

```json
"winterMonthTo": <uint>, /* End of winter period
```

(month: 0-11) */

```json
"winterDayTo": <uint> /* End of winter period (da
```

y: 1-31) */

```json
},
"fuelConsImpulse": { /* Impulse fuel consumption sensors
```

*/

```json
"maxImpulses": <uint>, /* Maximum number of impuls
```

es */

```json
                "skipZero": <uint> /* Skip the first zero value */
     }

}
```

Method of calculating fuel consumption:

| Flag | Description |
| --- | --- |
| 0x0 | Do not use fuel consumption in reports. |
| 0x01 | Calculate consumption mathematically. |
| 0x02 | Fuel level sensors. |
| 0x04 | Replace invalid values with those calculated mathematically. |
| 0x08 | Absolute fuel consumption sensors. |
| 0x10 | Impulse fuel consumption sensors. |
| 0x20 | Instant fuel consumption sensors. |
| 0x40 | Consumption by rates. |
| Flags of fuel fillings and drains: |  |
| Flag | Description |
| 0x01 | Merge values of fuel level sensors with the same name. |
| 0x02 | Filter values of fuel level sensors. |
| Merge values of fuel consumption sensors with the same | 0x04 name. |
| 0x08 | Detect fuel fillings only during stops. |
| 0x10 | Calculate fuel consumption by time. |
| Ignore sensor filtering when calculating the amount of filled | 0x40 fuel. |
| Ignore sensor filtering when calculating the amount of | 0x80 drained fuel. |
| 0x100 | Detect fuel drains in motion. |
| 0x100 | Replace invalid values with those calculated mathematically. 0 |
| 0x200      Return default fuel settings if configured (adaptive and | 0          median filtering). |
| 0x400 | Adaptive filtering. 0 |
| If the request fails, the response contains error code 7, indicating that the | user doesn’t have the required access right to the unit (ADF_ACL_ITEM_VIEW). |

## get_messages_filter

To get settings for filtering location data in unit messages, use the
unit/get_messages_filter command.

```http
svc=unit/get_messages_filter&params={"itemId":<long>}
```

### Parameters

The request must contain the itemId parameter, specifying the unit ID.

### Response

If the request is completed successfully, the response contains filtering
settings.

```json
{
          "enabled":<uint>,                      /* 1 - enable filteringof location data in unit messages, 0 - disable */
          "skipInvalid":<uint>,          /* Skip invalid messages */
          "minSats":<uint>,                      /* Minimum number of satellites */
          "maxHdop":<double>,                    /* Maximum HDOP value
*/
          "maxSpeed":<uint>,                     /* Maximum speed value
*/
          "lbsCorrection":<uint>,        /* Allow positioning by cellular base stations */
          "wifiCorrection":<uint>,       /* Allow positioning by Wi-Fi spots */
          "minWifiPoints":<uint>,        /* Minimum number of Wi-Fi points */
          "maxWifiPoints":<uint>,        /* Maximum number of Wi-Fi points */
          "wifiAccuracy":<double>        /* Location accuracy, m */
}
```

If the request fails, the response contains error code 7, indicating that the
user doesn’t have the required access right to the
unit (ADF_ACL_ITEM_VIEW_PROPERTIES).

## get_report_settings

To obtain the parameters used in reports, use the
unit/get_report_settings command.

```http
svc=unit/get_report_settings&params={"itemId":<long>}
```

### Parameters

The request must contain the itemId parameter, specifying the unit ID.

### Response

If the request is completed successfully, the response contains the
parameters used in reports.

```json
{
          "speedLimit":<uint>,                   /* Speed limit, km/h
*/
          "maxMessagesInterval":<uint>,       /* Maximum interval between messages, seconds */
          "dailyEngineHoursRate":<uint>,      /* Daily rate of engine hours, seconds */
          "urbanMaxSpeed":<uint>,                /* Urban speed limit,
km/h */
          "mileageCoefficient":<uint>,        /* Mileage coefficient */
          "fuelRateCoefficient":<uint>,       /* Fuel rate */
          "speedingTolerance":<uint>,            /* Allowed speeding, km/h (used if speedingMode = 1) */
          "speedingMinDuration":<uint>,       /* Minimum speeding time,
seconds */
          "speedingMode":<uint>               /* Speeding detection mode: 0 - use speedLimit, 1 - use map data */
}
```

If speedingMode = 0 and speedLimit = 0, the Speedings table is not
generated.

If the request fails, the response contains error code 7, indicating that the
user doesn’t have the required access
right (ADF_ACL_ITEM_VIEW_PROPERTIES).

## get_speed_settings

To get speed parameters, use the get_speed_settings request.

```http
svc=unit/get_speed_settings&params={
    "itemId":<long>
    }
```

### Parameters

The request must contain the itemId parameter, specifying the unit ID.

### Response

If the request is completed successfully, the following result is returned:

```json
{
    "speedParameter": "speeds2",
    "speedMeasure": 1
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             Wrong input parameter.

The user doesn’t have the required access right to the unit
7
(ADF_ACL_ITEM_VIEW_PROPERTIES).

## get_trip_detector

To obtain trip detection settings, use the
unit/get_trip_detector command.

```http
svc=unit/get_trip_detector&params={"itemId":<long>}
```

### Parameters

The request must contain the itemId parameter, specifying the unit ID.

### Response

If the request is completed successfully, the response contains trip
detection settings.

```json
{
           "type":<uint>,                    /* Type of movement detection (see below) */
           "gpsCorrection":<uint>,           /* Allow GPS correction: 0
- no, 1 - yes */
           "minSat":<uint>,                  /* Minimum number of satellites */

          "minMovingSpeed":<uint>,            /* Minimum moving speed, km/h */
          "minStayTime":<uint>,               /* Minimum parking time, seconds */
          "maxMessagesDistance":<uint>,       /* Maximum distance between messages, meters */
          "minTripTime":<uint>,               /* Minimum trip time, seconds */
          "minTripDistance":<uint>            /* Minimum trip distance,
meters */
}
```

Types of movement detection:

Value                Description

1                    GPS speed

2                    GPS coordinates

3                    Engine ignition sensor

4                    Mileage sensor

5                    Relative odometer

If the request fails, the response contains error code 7, indicating that the
user doesn’t have the required access right to the
unit (ADF_ACL_ITEM_VIEW_PROPERTIES).

## get_video_settings

Can only be used in Wialon Hosting.

To obtain unit video settings, execute the unit/get_video_settings
command. To do this, the View detailed object properties access right
to the unit is required.

```http
svc=unit/get_video_settings&params={"itemId":long}
```

### Parameters

The request must contain the itemId parameter, which specifies the unit
ID.

### Example

```http
svc=unit/get_video_settings&params={"itemId":200334}
```

### Response

If the request is completed successfully, the response contains the video
settings.

```json
{
        "settings": [
                {
                         "flags": 1,        /* If flags = 1, then the camera is active. */
                         "name": "cam"      /* Camera name */
                },
                {
                         "flags": 3,        /* If flags = 3, then the camera and video saving are active. */
                         "name": "cam1"      /* Camera name */
                }

                   ...
          ]
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4              Invalid input parameters.

The user doesn't have the required access right to the unit
7
(ADF_ACL_ITEM_VIEW_PROPERTIES).

## get_vin_info

Can only be used in Wialon Hosting.

To get the unit VIN information, use the unit/get_vin_info command.

```http
svc=unit/get_vin_info&params={"vin":<text>}
```

### Parameters

The request must contain the vin parameter, specifying the VIN number.

### Response

If the request is completed successfully, the unit VIN information is
returned.

```json
{
    {
         "vin_lookup_result":{
             "pflds":[             /* Profile fields */
                   {
                           "n":<text>,       /* Field name */
                           "v":<text>        /* Field value */
                   },
                   ...
             ]
         }
    }
}
```

If the request fails, a response of the following format is returned:

```json
{
    "vin_lookup_result":{
         "error":<bool>,           /* True if there is an error */
         "message":<text>,         /* Error message */
         "reasons":[               /* Error reasons */
             <text>,
             ...
         ]
    }
}
```

### Error codes

Error code         Description

6                  Failed to obtain VIN information.

7                  Access to the avl_vin billing service denied.

## get_vrt_command_queue

To get virtual commands, use the unit/get_vrt_command_queue request.

```http
svc=unit/get_vrt_command_queue&params={"itemId": <long>}
```

### Parameters

The request must contain the itemId parameter, specifying the unit ID.

### Example

```http
svc=unit/get_vrt_command_queue&params={"itemId": 132343}
```

### Response

If the request is completed successfully, the response contains virtual
commands.

```json
[{"cmd_alias":"","cmd_hex":"4040FF001167165F9E0040313233343A726562
6F6F74BE0C","cmd_name":"custom_msg","cmd_param":"@1234:reboot","cmd_tm_add":"1729519518","l_add_params":[{"pname":"cmd_seq_n","ptype":"int","pval":"0"}]},{"cmd_alias":"","cmd_hex":"4040FF0011671678
A70040313233343A7265626F6F749D52","cmd_name":"custom_msg","cmd_param":"@1234:reboot","cmd_tm_add":"1729525927","l_add_params":[{"pname":"cmd_seq_n","ptype":"int","pval":"0"}]}]
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4            Invalid input parameters.

The user doesn't have the required access right to the
7
unit (ADF_ACL_ITEM_EDIT_PROPERTIES).

## registry_charge_event

To register a battery charge, use the
unit/registry_charge_event command.

```http
svc=unit/registry_charge_event&params={
        "date": <uint>,
        "volume": <double>,
        "cost": <double>,
        "location": "<text>",
        "x": <double>,

          "y": <double>,
          "description": "<text>",
          "itemId": <long>
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| date | Date. |
| volume | Amount of energy used to recharge the battery, in kWh. |
| cost | Cost. |
| location | Unit location. |
| x | Longitude. |
| y | Latitude. |
| description | Description. |
| itemId | Unit ID. |

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

If the request fails, an error code is returned.

### Error codes

| Parameter | Description |
| --- | --- |
| 4 | This user can't execute the request. |
| 6 | Failed to register a battery charge. |
| The user doesn't have the required access right to the | 7 unit (ADF_ACL_AVL_UNIT_REG_EVENTS). |

## registry_custom_event

To register a custom event, use the
unit/registry_custom_event command.

```http
svc=unit/registry_custom_event&params={
    "date":<uint>,
    "x":<double>,
    "y":<double>,
    "description":<text>,
    "violation":<uint>,
    "itemId":<long>,
    "nt":<text>,
    "nct":<text>
}
```

### Parameters

The required parameters are marked with an asterisk (*):

| Parameter | Description |
| --- | --- |
| date* | Date. |
| x* | Longitude. |
| y* | Latitude. |
| description* | Description. |
| violation* | Violation: 0 - common event, 1 - violation. |
| itemId* | Unit ID. |
| nt | Notification text. |
| nct | Notification creation time. |
| The nt and nct parameters must be used simultaneously. |  |
| These parameters are passed when registering an event for an online | notification, and the triggered notification text is assigned to them. |

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             The user ID is invalid or the user has signed out.

6             Failed to register the event.

The user doesn't have the required access right to the unit
7
(ADF_ACL_AVL_UNIT_REG_EVENTS).

## registry_fuel_filling_event

To register a fuel filling, use the unit/registry_fuel_filling method.

```http
svc=unit/registry_fuel_filling_event&params={
       "date": <uint>,
       "volume": <double>,
       "cost": <double>,
       "location": <text>,
       "deviation": <uint>,
       "x": <double>,
       "y": <double>,
       "description": <text>,
       "itemId": <long>
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| date | Date. |
| volume | Amount of fuel filled. |
| cost | Cost. |
| location | Unit location. |
| deviation | Time deviation, min. |
| x | Longitude. |
| y | Latitude. |
| description | Description. |
| itemId | Unit ID |

### Response

If the request is completed successfully, an empty object is returned.

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4           The user ID is invalid or the user has signed out.

6           Failed to register the event.

The user doesn’t have the required access right to the unit
7
(ADF_ACL_AVL_UNIT_REG_EVENTS).

## registry_maintenance_event

To register maintenance work, use the unit/registry_maintenance_event
request.

svc=unit/registry_maintenance_event&params={

```json
"date": <uint>,
"info": <text>,
"duration": <int>,
"cost": <double>,
"location": <text>,
"x": <double>,
"y": <double>,
"description": <text>,
"mileage": <double>,
"eh": <int>,
"done_svcs": <text>,
"itemId": <long>
```

}

### Parameters

| Parameter | Description |
| --- | --- |
| date | Date. |
| info | Type of maintenance work. |
| duration | Duration. |
| cost | Cost. |
| location | Unit location. |
| x | Longitude. |
| y | Latitude. |
| description | Description. |
| mileage | Mileage. |
| eh | Engine hours. |
| done_svcs | List of services (comma-separated). |
| itemId | Unit ID |

### Response

If the request is completed successfully, an empty object is returned.

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

One of the following errors:

4               the user ID is invalid or the user has signed out,
overflow check error (duration, mileage, engine hours).

6            Failed to register the event.

The user doesn’t have the required access right to the unit
7
(ADF_ACL_AVL_UNIT_REG_EVENTS).

## registry_status_event

To register a unit status, use the unit/registry_status_event command.

```http
svc=unit/registry_status_event&params={
    "date":<uint>,
    "description":<text>,
    "itemId":<long>
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| date | Date |
| description | Description |
| itemId | Unit ID |

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, the response contains an error code.

### Error codes

| Parameter | Description |
| --- | --- |
| 4 | The user ID is invalid or the user has signed out. |
| 6 | Failed to register the unit status. |
| The user doesn't have the required access right to the | 7 unit (ADF_ACL_AVL_UNIT_REG_EVENTS). |

## reset_vrt_command_queue

To reset the queue of virtual commands, use the
unit/reset_vrt_command_queue command.

```http
svc=unit/reset_vrt_command_queue&params={"itemId": <long>}
```

### Parameters

The request must contain the itemId parameter, specifying the unit ID.

### Example

Below is an example of the unit/reset_vrt_command_queue request.

```http
svc=unit/reset_vrt_command_queue&params={"itemId": 132343}
```

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4           Invalid input parameters

The user doesn’t have the required access right to the unit
7
(ADF_ACL_ITEM_EDIT_PROPERTIES).

## send_cmd

To send a command to the unit, use the unit/send_cmd command.

```http
svc=unit/send_cmd&params={
    "itemId": <long>,
    "commandType": <text>,
    "commandName": <text>,
    "linkType": <text>,
    "param": <text>,
    "timeout": <uint>,
    "flags": <uint>
}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| itemId* | Unit ID. |
| Name | Description |
| commandType* | Command type. See below. |
| commandName | Command name. If not specified, the command type is used as a name. |
| Channel via which the command should be sent. | linkType* See below. |
| param* | Command parameters. |
| Timeout for the command to wait in the queue, in | timeout* seconds. |
| flags | Flags for selecting a phone number to execute the command: 0 - use any (primary, then secondary) 0x1 - use primary 0x2 - use secondary 0x10 - send param in JSON format. |

## Command types

Command type               Description

block_engine               Block the engine.

unblock_engine             Unblock the engine.

custom_msg                 Send a custom message.

driver_msg                 Send a message to the driver.

Command type          Description

download_msgs         Download messages.

query_pos             Request the unit location.

query_photo           Request a photo.

output_on             Activate an output.

output_off            Deactivate an output.

send_position         Send coordinates.

set_report_interval   Set a data transfer interval.

upload_cfg            Upload a configuration.

upload_sw             Upload firmware.

## Channels

Value                               Channel

Empty string                        Auto

tcp                                 TCP

udp                                 UDP

vrt                                 Virtual

Value                                        Channel

gsm                                          SMS

### Example

Below is an example of the unit/send_cmd request.

```http
svc=unit/send_cmd&params={"itemId":1351,"commandName":"pin","linkType":"","param":"pin 0000","timeout":60,"flags":0}
```

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4            Invalid input parameters.

Error
Description
code

5           Error sending the command.

The user doesn’t have the required access rights to the
unit, specifically:
7           ADF_ACL_AVL_UNIT_VIEW_CMD_ALIASES
ADF_ACL_AVL_UNIT_EDIT_CMD_ALIASES
ADF_ACL_AVL_UNIT_EXEC_CMDS

## set_active

To deactivate or activate a unit, use the unit/set_active command.

```http
svc=unit/set_active&params={
    "itemId": <long>,
    "active": <bool>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| active | Required action: 0 — deactivation, 1 — activation. |

### Response

If the request is completed successfully, the following response is returned:

```json
{
     "active":<bool>,   /* 0 — unit deactivated, 1 — unit activated
*/
}
```

Otherwise, an error code is returned.

### Error codes

Error code           Description

4                    Invalid input format

One of the following errors:

User not found.
6
Failded to change the unit staus

See the reason field for details.

One of the following errors:

Permission denied.

7                        Limit of deactivated units reached.

Account disabled.

See the reason field for details.

## update_access_password

To change the access password for a unit, use the
unit/update_access_password command.

```http
svc=unit/update_access_password&params={
    "itemId": <long>,
    "accessPassword": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| accessPassword | New access password. |

### Response

If the request is completed successfully, the response contains the new
access password.

```json
{
    "psw":<text>
}
```

In case the request fails, an error code is returned.

### Error codes

Error
Description
code

6            Failed to change the password.

The user doesn’t have the required access right to the unit
7
(ADF_ACL_AVL_UNIT_EDIT_HW).

## update_activity_settings

The default source of driver activity is iButton. To set another activity
source, use the unit/update_activity_settings command.

```http
svc=unit/update_activity_settings&params={
    "itemId": <long>,
    "type": <int>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID |
| Parameter | Description |
| Driver activity source: |  |
| type | 0 — none 1 — assignments 2 — tachograph |

### Example

Below is an example of the unit/update_activity_settings request.

```http
svc=unit/update_activity_settings&params={
      "itemId": 20334,
      "type": 1
}
```

### Response

If the request is completed successfully, an empty object is returned.

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4           Invalid input parameters.

5           Error updating the settings.

The user doesn’t have the required access rights to the unit
7
(ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS).

## update_billing_code

To assign a new activation code to a unit or unassign an old one, use the
unit/update_billing_code method.

```http
svc=unit/update_billing_code&params={
    "itemId": <long>,
    "code": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| code | Activation code to be assigned or unassigned. |

### Example

Below is an example of the unit/update_billing_code request.

```http
svc=unit/update_billing_code&params={
    "itemId": 1133,
    "code": "bf6364e80170cbd4a42bfa8eb446deff"
}
```

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{"code": "bf6364e80170cbd4a42bfa8eb446deff"}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

6            Error updating the code.

The user doesn’t have the required access rights to the
7
unit (ADF_ACL_AVL_UNIT_VIEW_HW).

## update_calc_flags

To update calculation parameters for counters, use the
unit/update_calc_flags command.

```http
svc=unit/update_calc_flags&params={
    "itemId": <long>,
    "newValue": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| newValue | New counter calculation flags (see below). |

## Calculation flags

| Flag | Description |
| --- | --- |
| 0x000 | Mileage counter: GPS. |
| 0x001 | Mileage counter: Mileage sensor. |
| 0x002 | Mileage counter: Relative odometer. |
| Flag | Description |
| 0x003 | Mileage counter: GPS + engine ignition sensor. |
| 0x010 | Engine hours counter: Engine ignition sensor. |
| 0x020 | Engine hours counter: Absolute engine hours sensor. |
| 0x040 | Engine hours counter: Relative engine hours sensor. |
| 0x100 | Automatic calculation of mileage based on new messages. |
| messages | Automatic calculation of engine hours based on new 0x200 |
| 0x400 | Automatic calculation of GPRS traffic. |

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
      /* Flags applied. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

6          Error updating the flags.

The user doesn’t have the required access rights to the unit
7
(ADF_ACL_AVL_UNIT_EDIT_COUNTERS).

## update_command_definition

To create, edit or delete a command, use the
unit/update_command_definition method.

svc=unit/update_command_definition&params={

```json
"itemId": <long>,
"id": <long>,
"callMode": <text>,
"n": <text>,
"c": <text>,
"l": <text>,
"p": <text>,
"a": <long>
```

}

### Parameters

If you want to create or edit a command, the request must contain the
following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| id | Command ID. |
| callMode | Required action. For creation, specify create, for editing, update. |
| n | Command name. |
| c | Command type (see below). |
| l | Link type (see below). |
| p | Parameters. |
| a | Access rights that the user must have to execute this command (see check_items_billing ). |

## Command types

Value                           Command type

block_engine                    Block the engine

unblock_engine                  Unblock the engine

custom_msg                      Send a custom message

driver_msg                      Send a message to the driver

Value                 Command type

download_msgs         Download messages

query_pos             Request coordinates

query_photo           Request a photo

output_on             Activate an output

output_off            Deactivate an output

send_position         Send coordinates

set_report_interval   Set a data transfer interval

upload_cfg            Upload the configuration

upload_sw             Upload the firmware

## Link types

Value                               Link Type

Empty string                        Auto

tcp                                 TCP

udp                                 UDP

vrt                                 Virtual

gsm                                 SMS

If you want to create a command by copying it from another unit, the
request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| id | Command ID. |
| callMode | Required action. For creation, specify create. |
| oldItemId | ID of the unit from which you want to copy the command. |
| oldCmdId | ID of the command you want to copy |
| If you want to delete a command, the request must contain the following | parameters: |
| Parameter | Description |
| itemId | Unit ID. |
| id | Command ID. |
| callMode | Required action. For deletion, specify delete. |

### Response

If the request to create or edit a command is completed successfully, a
response in the following format is returned:

```json
[
    <long>,         /* Command ID. */
    {
           "id":<long>,   /* Command ID. */
           "n":<text>,    /* Command name. */
           "c":<text>,    /* Command type. */
           "l":<text>,    /* Link type. */
           "p":<text>,    /* Parameters. */
           "a":<uint>,    /* Access level. */
           "f":<uint>, /* Flags. */
           "jp":{...} /* JSON parameters (only if exist). */
    }
]
```

If the request to delete a command is completed successfully, a response
in the following format is returned:

```json
[
    <long>,          /* Command ID. */null
]
```

If the request fails, an error code is returned.

### Error codes

Error code                 Description

4                          Wrong input format.

6                          Failed to delete the command.

## update_device_type

To update the device (hardware) type and the unique ID of a unit, use the
unit/update_device_type method.

```http
svc=unit/update_device_type&params={
    "itemId": <long>,
    "deviceTypeId": <long>,
    "uniqueId": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| deviceTypeId | New device type. |
| uniqueId | New unique ID. |
| You can get all available device types using the core/get_hw_types method. |  |

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
{

      "uid": <text>, /* Unique ID. */
      "hw": <long>     /* Device type. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4                  Wrong device type ID.

6                  Failed to update the device type.

No ADF_ACL_AVL_UNIT_EDIT_HW access right to the
7
unit.

1002               An item with the specified property already exists.

## update_drive_rank_settings

To update eco driving criteria, use the update_drive_rank_settings
method.

```http
svc=unit/update_drive_rank_settings&params={
      "itemId": <long>,
      "driveRank": {
          "acceleration": [
              {
                    "flags": <uint>,
                    "min_value": <double>,

        "max_value": <double>,
        "min_speed": <uint>,
        "max_speed": <uint>,
        "min_duration": <uint>,
        "max_duration": <uint>,
        "validator_id": <long>,
        "name": <text>,
        "penalties": <uint>
  },
  ...
```

],
"brake": [

```json
{
      "flags": <uint>,
      "min_value": <double>,
      "max_value": <double>,
      "min_speed": <uint>,
      "max_speed": <uint>,
      "min_duration": <uint>,
      "max_duration": <uint>,
      "validator_id": <long>,
      "name": <text>,
      "penalties": <uint>
},
...
```

],
"turn": [

```json
{
      "flags": <uint>,
      "min_value": <double>,
      "max_value": <double>,
      "min_speed": <uint>,
      "max_speed": <uint>,
      "min_duration": <uint>,
      "max_duration": <uint>,
      "validator_id": <long>,
      "name": <text>,
      "penalties": <uint>
},
...
```

],
"sensor": [

```json
{
      "flags": <uint>,
      "min_value": <double>,
      "max_value": <double>,
      "min_speed": <uint>,
      "max_speed": <uint>,
      "min_duration": <uint>,
      "max_duration": <uint>,
      "validator_id": <long>,
      "sensor_id": <long>,
      "name": <text>,
      "penalties": <uint>
},
...
```

],
"speeding": [

```json
{
      "flags": <uint>,
      "min_value": <double>,
      "max_value": <double>,
      "min_speed": <uint>,
      "max_speed": <uint>,
      "min_duration": <uint>,
      "max_duration": <uint>,
      "validator_id": <long>,
      "name": <text>,
      "penalties": <uint>
},
...
```

],
"harsh": [

```json
{
      "flags": <uint>,
      "min_value": <double>,
      "max_value": <double>,
      "min_speed": <uint>,
      "max_speed": <uint>,
      "min_duration": <uint>,

                "max_duration": <uint>,
                "validator_id": <long>,
                "name": <text>,
                "penalties": <uint>
          },
          ...
     ],
     "global": {
          "accel_mode": <uint>
     }
 }
```

}

### Parameters

The request must contain the parameters:

| Parameter | Description |
| --- | --- |
| Penalty calculation method: |  |
| accel_mode | 0 — combined 1 — by speed in messages 2 — by accelerometer values |
| itemId | Unit ID. |
| driveRank | Object with parameters of eco driving criteria (see below). This object can be empty. |

## Eco driving criteria

| Parameter | Description |
| --- | --- |
| acceleration | Acceleration. |
| brake | Braking. |
| turn | Turn. |
| sensor | Custom criterion based on sensor readings. |
| speeding | Speeding. |
| harsh | Reckless driving. |
| idling | Idling. |
| global | Acceleration calculation method. |

## Criterion settings

| Parameter | Description |
| --- | --- |
| Flags: |  |
| 1 — penalty averaging by time, |  |
| flags               2 — penalty averaging by mileage, | 4 — use validator as a multiplier, |
| 8 — skip missing values. |  |
| min_value | Minimum value. |
| Parameter | Description |
| max_value | Maximum value (excluded). |
| min_speed | Minimum speed. |
| max_speed | Maximum speed (excluded). |
| min_duration | Minimum duration. |
| max_duration | Maximum duration (excluded). |
| validator_id | Validator sensor ID. |
| sensor_id | Sensor ID (used only for the sensor criterion) |
| name | Criterion name. |
| penalties | Penalty points. |
| Calculate acceleration by: |  |
| accel_mode | 0 — GPS + accelerometer 1 — GPS 2 — accelerometer |

### Response

If the request is completed successfully, an empty object is returned:

```json
{
    /* Settings saved. */

}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4            Wrong input in the driveRank parameter.

6            Failed to update eco driving criteria.

No ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS access
7
right to the unit.

## update_eh_counter

To set a new value for the counter of engine hours, use the
unit/update_eh_counter method.

```http
svc=unit/update_device_type & params = {
    "itemId": <long>,
    "deviceTypeId": <long>,
    "uniqueId": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| newValue | New value of the engine hours counter (h). Must be within the range of 0 to 0xFFFFFFFF. |

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
    "cneh": <uint> /* Value of the engine hours counter (h). */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             Wrong input parameters.

6             Failed to update the engine hours counter.

No ADF_ACL_AVL_UNIT_EDIT_COUNTERS access right to
7
the unit.

## update_event_data

To specify event parameters, use the unit/update_event_data method.

svc = unit/update_events & params = {

```json
{
    "itemId": <long>,
    "eventType": <text>,
    "timeFrom": <uint>,
    "timeTo": <uint>,
    "params": {
        "test1": <uint>,
        "test2": <text>
    }
}
```

}

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| Type of event. For example: |  |

#### lls — fuel level

theft — fuel drain
eventType
filling — fuel filling

sensors — sensor values
ignition — ignition state

| Parameter | Description |
| --- | --- |
| timeFrom | Event beginning. |
| timeTo | Event end. |
| params | Object with updated parameters. |

### Example

Below is an example of the unit/update_event_data request.

svc = unit/update_events & params = {

```json
    "events": [
        {
            "itemId": 1555,
            "resourceId": 123,
            "eventType": "lls",
            "timeFrom": 1689734883,
            "timeTo": 1689734883,
            "params": {
                  "test1": 1
            }
        }
    ]
}
```

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
    "msgs": 1 /* Number of updated events. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             Wrong input parameters.

No ADF_ACL_AVL_RES_EDIT_REPORTS access right to the
7
unit.

## update_events

To mark a fuel filling or drain as false, use the unit/update_events
method.

```http
svc=unit/update_events&params={
    "events": [
        {
            "itemId": <long>,
            "resourceId": <long>,
            "eventType": <text>,
            "timeFrom": <uint>,
            "timeTo": <uint>,
            "params": {
                  "mark": <uint>

            }
        }
    ]
```

}

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| resourceId | ID of the resource in which the executed report is stored. |
| Type of event: |  |
| eventType | lls — fuel level theft — fuel drain filling — fuel filling |
| timeFrom | Event beginning. |
| timeTo | Event end. |
| params | Object with updated parameters. |

### Example

Below is an example of the unit/update_events request.

```http
svc=unit/update_events&params={
    "events": [
            {
                 "itemId": 1555,
                 "resourceId": 123,
                 "eventType": "lls",
                 "timeFrom": 1689734883,
                 "timeTo": 1689734883,
                 "params": {
                     "mark": 1
                 }
            }
    ]
}
```

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
    "items": [
            {
                 "itemId": 1285,
                 "error": 0,     /* 0 - success, 7 - no access right */
                 "msgs": 1
            },
            {
                 "itemId": 1285,
                 "error": 0,
                 "msgs": 1
            }
    ]

}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4           Wrong input parameters.

5           Events are disabled for the unit.

No ADF_ACL_AVL_RES_EDIT_REPORTS access right to the
7           resource, or no ADF_ACL_ITEM_VIEW access right to the
unit.

## update_fuel_math_params

To update the parameters of mathematical calculation of fuel consumption,
use the unit/update_fuel_math_params method.

```http
svc=unit/update_fuel_math_params&params={
    "itemId": <long>,
    "idling": <double>,
    "urban": <double>,
    "suburban": <double>
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| idling | Idling, liters per hour. |
| urban | Urban cycle, liters per 100 km. |
| suburban | Suburban cycle, liters per 100 km. |

### Response

If the request is completed successfully, an empty object is returned:

```json
{
    /* Parameters updated. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

Failed to update the parameters of mathematical
6
calculation.

Error
Description
code

No ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS access
7
right to the unit.

## update_fuel_rates_params

To update the parameters of fuel consumption by rates, use the
unit/update_fuel_rates_params method:

```http
svc=unit/update_fuel_rates_params&params={
    "itemId": <long>,
    "consSummer": <double>,
    "consWinter": <double>,
    "winterMonthFrom": <ubyte>,
    "winterDayFrom": <ubyte>,
    "winterMonthTo": <ubyte>,
    "winterDayTo": <ubyte>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| consSummer | Summer fuel consumption, liters per 100 km. |
| consWinter | Winter fuel consumption, liters per 100 km. |
| Parameter | Description |
| winterMonthFrom | Starting month of the winter period (0–11). |
| winterDayFrom | Starting day of the winter period (1–31). |
| winterMonthTo | Ending month of the winter period (0–11). |
| winterDayTo | Ending day of the winter period (1–31). |

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

Failed to update the parameters of fuel consumption
6
rates.

No ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS access
7
right to the unit.

## update_health_check

The unit/update_health_check request is used to configure health check
settings for a unit.

```http
svc=unit/update_health_check&params={
    "itemId":<long>,
    "settings":<text>
    }
```

### Parameters

The following parameters are required:

| Name | Description |
| --- | --- |
| itemId | Unit ID. |
| settings | JSON with parameters of health check settings. See below. |

## JSON example

Below is an example of a JSON object with parameters of health check
settings.

```json
"settings": {
"low_battery": {
      "period": "1h",
      "unhealthy_conditions": [
          {
              "type": "less",   // less, greater, equal, not_equa
```

l, unchanged

```json
               "value": 20.0
           }
     ]
},
"max_messages_last_hour": {
     "period": "1m",
     "unhealthy_conditions": [
           {
               "type": "greater",      // less, greater, equal, not_e
```

qual, unchanged

```json
               "value": 1000.0
           }
     ]
},
"no_data": {
     "period": "1d"
},
"missing_position_data": {
     "period": "1m"
},
"insufficient_satellite_coverage": {
     "period": "1m",
     "unhealthy_conditions": [
           {
               "type": "less",     // less, greater, equal, not_equa
```

l, unchanged

```json
               "value": 4.0
           }
     ]
},
"max_distance_between_messages": {
     "period": "1h",
     "unhealthy_conditions": [
           {
               "type": "greater",      // less, greater, equal, not_e
```

qual, unchanged

```json
               "value": 100000.0 // m
           }
     ]

},
"sensor": {
     "items": [
        {
              "id": 1, // voltage
              "period": "1m",
              "unhealthy_conditions": [
                  {
                       "type": "less", // less, greater, equal, n
```

ot_equal, unchanged

```json
     "value": 12.0
},
{
     "type": "greater",   // less, greater, equa
```

l, not_equal, unchanged

```json
               "value": 13.0
          }
      ]
},
{
      "id": 3, // fuel
      "period": "1m",
      "unhealthy_conditions": [
          {
               "type": "unchanged",    // less, greater, eq
```

ual, not_equal, unchanged

```json
                     "value": 0.0 // do not parse
                }
            ]
      },
      {
            "id": 2, // digital (ignition)
            "period": "1m",
            "unhealthy_conditions": [
                {
                     "type": "equal", // equal, not_equal
                     "value": 0.0 // 0.0 - off, 1.0 - on
                }
            ]
      }

    ]
}
```

}

### Example

Below is an example of the unit/update_health_check request.

svc=unit/update_health_check&params={

```json
 "itemId": 1583,
 "settings": {
     "low_battery": {
          "period": "1h",
          "unhealthy_conditions": [
              {
                   "type": "less",
                   "value": 20.0
              }
          ]
     },
     "max_messages_last_hour": {
          "period": "1m",
          "unhealthy_conditions": [
              {
                   "type": "greater",
                   "value": 1000.0
              }
          ]
     },
     "no_data": {
          "period": "1d"
     },
     "missing_position_data": {
          "period": "1m"
     },
     "insufficient_satellite_coverage": {

"period": "1m",
"unhealthy_conditions": [
    {
         "type": "less",
         "value": 4.0
    }
]
```

},
"max_distance_between_messages": {

```json
"period": "1h",
"unhealthy_conditions": [
    {
         "type": "greater",
         "value": 100000.0
    }
]
```

},
"sensor": {

```json
  "items": [
      {
           "id": 1,
           "period": "1m",
           "unhealthy_conditions": [
               {
                    "type": "less",
                    "value": 12.0
               },
               {
                    "type": "greater",
                    "value": 13.0
               }
           ]
      },
      {
           "id": 3,
           "period": "1m",
           "unhealthy_conditions": [
               {
                    "type": "unchanged",
                    "value": 0.0

                            }
                        ]
                   },
                   {
                        "id": 2,
                        "period": "1m",
                        "unhealthy_conditions": [
                            {
                                "type": "equal",
                                "value": 0.0
                            }
                        ]
                   }
               ]
          }
      }
}
```

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4              Wrong input parameters.

Error
Description
code

The “Health check” service is not enabled or the user
7            doesn’t have the ADF_ACL_ITEM_EDIT_OTHER access right
to the unit.

6            Error updating health check settings.

## update_hw_params

To update hardware configuration, use the unit/update_hw_params
method:

svc=unit/update_hw_params&params={

```json
"hwId": <text>,
"action": <text>,
...
```

}

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| hwId | Device type ID. |
| action | Action: |

#### set — set the configuration

| Parameter | Description |
| --- | --- |
| for configuring | check_config — check if the device has parameters download_file — download the configuration file get — get the configuration |
| If action=set, specify the following additional parameters: |  |
| Parameter | Description |
| itemId | Unit ID. |
| params_data | Parameter data. |
| params | Array of parameter configurations. |
| name | Parameter name. |
| type | Parameter type (see below). |
| value | Parameter value. |
| reset | Flag: 1 — reset to the default value, 0 — do not reset. |
| set_psw | Flag (if the parameter type is password): 1 — change the password, 0 — do not change the password. |
| reset_all | Reset the device type configuration. |
| If 0 is passed, the parameter value stores the path of | full_data        the uploading file, if 1 is passed, it stores the HEX string. |

### Example

```json
{
    "itemId": <long>,
    "params_data": {
        "params": [
             {
                 "name": <text>,
                 "type": <text>,
                 "value": <text|int|double>,
                 "reset": <uint>,
                 "set_psw": <uint>
             }
        ],
        "reset_all": <uint>,
        "full_data": <uint>
    }
}
```

## Parameter types

#### text

file
long

double
int

bool
password

If the parameter is of the file type, use a POST request with multiple
contents (multipart/form-data) to upload the file. For example:

POST /wialon/ajax.html?svc=unit/update_hw_params&sid=<long> HTTP/
1.1
Host: <host>
Connection: keep-alive

Content-Length: <uint>
Cache-Control: max-age=0
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
UZNF25nwwhMzU9Me
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;
q=0.8
Accept-Encoding: gzip,deflate,sdch
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3

------WebKitFormBoundaryUZNF25nwwhMzU9Me
Content-Disposition: form-data; name="params"

```json
{"itemId":<long>,"hwId":<text>,"params_data":{"reset_all":0,"params":[
{"name":"custom_polls_file","type":"file","value":"cfg_param_custom_polls_file","data":"","reset":0}],
"full_data":0},"action":"set"}

------WebKitFormBoundaryUZNF25nwwhMzU9Me
Content-Disposition: form-data; name="cfg_param_custom_polls_file"; filename="file.txt"
Content-Type: text/plain

<binary data>
------WebKitFormBoundaryUZNF25nwwhMzU9Me--
```

If action=set, specify the following additional parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| field | Configuration file ID. |

### Example

```json
{
     "itemId":<long>,
     "fileId":<text>
}
```

If action=get, specify the following additional parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| fullData | Flag: 0 — request the configuration without files, 1 — request the configuration with files. |

### Example

```json
{
     "itemId":<long>,
     "fullData":<uint>
}
```

### Response

If the request is completed successfully, the response depends on the value
of the action parameter.

For action = set:

```json
{}
```

For action = check_config:

```json
{
     "error":<uint>       /* If the value is 0, the device has additional parameters. Any other value indicates no parameters. */
}
```

For action = download_file:

```json
{}
```

For action = get:

```json
[
     {                /* Parameter configuration.*/
         "default":<text|int|double>,         /* Default value. */
         "description":<text>,         /* Description. */
         "label":<text>,               /* Name. */
         "maxval":<int|double>,               /* Maximum value. */
         "minval":<int|double>,               /* Minimum value. */
         "name":<text>,                /* System name. */
         "readonly":<bool>,            /* Read only: 1 - yes, 0 - no.
*/
         "type":<text>,                /* Type. */
         "value":<text|int|double> /* Value. */
     }
]
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

6              Failed to update the hardware parameters.

The hw_config property value of hwId is empty. Only for
1005
the check_config action.

## update_image

To set or change a unit icon, execute the unit/update_image method.

To copy an icon from another unit, use the following signature:

```http
svc=unit/update_image&params={
      "itemId": <long>,
      "oldItemId": <long>
}
```

To use an icon from the library, use the following signature:

```http
svc=unit/update_image&params={
      "itemId": <long>,
      "libId": <long>,
      "path": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | ID of the unit to which you want to apply the icon. |
| olditemId | ID of the unit from which you want to copy the icon. |
| libId | ID of the resource in which the necessary image is stored. To use the default library, pass 0. |
| path | Path to the image file. |

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error code      Description

4               Wrong input parameters.

6               Failed to set or change the unit icon.

7               No ADF_ACL_ITEM_EDIT_IMAGE access right to the unit.

## update_messages_filter

To change the settings of location data filtering, use the
unit/update_messages_filter method.

```http
svc=unit/update_messages_filter&params={
    "itemId": <long>,
    "enabled": <bool>,
    "skipInvalid": <bool>,
    "minSats": <ubyte>,
    "maxHdop": <double>,
    "maxSpeed": <uint>,
    "lbsCorrection": <bool>,
    "wifiCorrection": <bool>,
    "minWifiPoints": <ubyte>,
    "maxWifiPoints": <ubyte>,
    "wifiAccuracy": <double>
}
```

### Parameters

The request can contain the following parameters. The required ones are
marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Unit ID. |
| enabled* | Location data filtering: 1 — enable, 0 — disable. |
| Skip invalid messages. Allows ignoring the GPS data | skipInvalid* identified by the device as invalid. |
| minSats*           The minimum number of satellites that should be | used to determine the coordinates in order for a |
| Parameter | Description |
| message to be considered valid. The recommended | number is at least four. The value can’t exceed 255. |
| The maximum HDOP value with which messages are | maxHdop* considered valid. The value can’t exceed 9,999. |
| The limit for speed values. If it is exceeded, the | message is considered invalid. You can’t indicate a maxSpeed* value greater than 9,999. If 0 is specified, this filtering criterion is not taken into account. |
| lbsCorrection | Allow positioning by cellular base stations. |
| wifiCorrection | Allow positioning by Wi-Fi points. |
| The minimum number of Wi-Fi points which should | be taken into account in order for the messages to minWifiPoints    be considered valid. You can indicate only an integer value. The minimum allowed value is 2, the maximum one is 255. |
| The maximum number of Wi-Fi points which should | be taken into account when determining the unit maxWifiPoints    location. You can indicate only an integer value. The minimum allowed value is 2, the maximum one is 255. |
| The location accuracy in meters. A message is | considered invalid if its accuracy value is greater wifiAccuracy     than the specified one. You can specify an integer or fractional number greater than or equal to zero. The maximum allowed value is 10,000. |

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4              Wrong input parameters.

Failed to change the settings of of location data
6
filtering.

No ADF_ACL_AVL_UNIT_EDIT_HW access right to the
7
unit.

## update_mileage_counter

To set a new value for the mileage counter, use the
unit/update_mileage_counter method.

```http
svc=unit/update_mileage_counter&params={
     "itemId": <long>,

    "newValue": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| newValue | New value of the mileage counter (km). |

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
    "cnm": <uint> /* Value of the mileage counter (km). */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             Wrong input parameters.

6             Failed to update the mileage counter.

No ADF_ACL_AVL_UNIT_EDIT_COUNTERS access right to
7
the unit.

## update_phone

To set a new phone number for a unit, use the unit/update_phone
method.

svc=unit/update_phone&params={

```json
"itemId": <long>,
"phoneNumber": <text>
```

}

The character + in the phone number must be replaced by the code %2B.

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| phoneNumber | New phone number. |

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
      "ph": <text>   /* Phone number. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             Wrong input parameters.

6             Failed to update the phone number.

7             No ADF_ACL_AVL_UNIT_EDIT_HW access right to the unit.

The new phone number matches the old one, or this
1002
number is already used for another unit.

## update_phone2

To update the second phone number for a unit, use the
unit/update_phone2 command.

```http
svc=unit/update_phone2&params={
      "itemId": <long>,

    "phoneNumber": <text>
}
```

The character + in the phone number must be replaced by the code %2B.

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| phoneNumber | New phone number. |

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
    "ph2": <text>    /* Phone number. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4               Wrong input parameters.

6               Failed to update the phone number.

7               No ADF_ACL_AVL_UNIT_EDIT_HW access right to the unit.

The new phone number matches the old one, or this
1002
number is already used for another unit.

## update_report_settings

To update parameters used in reports, use the
unit/update_report_settings method:

```http
svc=unit/update_report_settings&params={
    "itemId": <long>,
    "params": {
        "speedLimit": <uint>,
        "maxMessagesInterval": <uint>,
        "dailyEngineHoursRate": <uint>,
        "urbanMaxSpeed": <uint>,
        "mileageCoefficient": <double>,
        "fuelRateCoefficient": <double>,
        "maxDistanceBetweenCoordinates": <uint>,
        "maxMessagesSpeed": <uint>,
        "speedingTolerance": <uint>,
        "speedingMinDuration": <uint>,
        "speedingMode": <uint>
    }
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| speedLimit | Speed limit, km/h. |
| maxMessagesInterval | Maximum interval between messages, s. |
| dailyEngineHoursRate | Daily rate of engine hours, h. |
| urbanMaxSpeed | Urban speed limit, km/h. |
| mileageCoefficient | Mileage coefficient. |
| fuelRateCoefficient | Fuel rate. |
| maxDistanceBetweenCoordinates | Maximum distance between coordinates. |
| maxMessagesSpeed | Maximum speed. |
| speedingTolerance | Allowed speeding, km/h (used if speedingMode = 1). |
| speedingMinDuration | Minimum speeding time, s. |
| Speeding detection mode: | speedingMode                          0 – use speedLimit 1 – use map data |
| If speedingMode = 0 and speedLimit = 0, then no speeding table is | generated. |

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             Wrong input parameters.

Failed to update a parameter from the params section or
6
validate a specific parameter.

No ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS access
7
right to the unit.

## update_retranslation_property

To update the retranslation_property of the unit, use the
unit/update_retranslation_property method:

```http
svc=unit/update_report_settings&params={
     "itemId": <long>,
     "params": {

       "speedLimit": <uint>,
       "maxMessagesInterval": <uint>,
       "dailyEngineHoursRate": <uint>,
       "urbanMaxSpeed": <uint>,
       "mileageCoefficient": <double>,
       "fuelRateCoefficient": <double>,
       "maxDistanceBetweenCoordinates": <uint>,
       "maxMessagesSpeed": <uint>,
       "speedingTolerance": <uint>,
       "speedingMinDuration": <uint>,
       "speedingMode": <uint>
   }
```

}

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| route_data | Object with route parameters. |
| Type of vehicle. Possible values: |  |
| bus | trolleybus |
| tram | vehicle_type                tramway minibus route taxi |
| route | Route name. |

### Example

Below is an example of the unit/update_retranslation_property request:

```http
svc=unit/update_retranslation_property&params={"itemId":814743,"route_data":{"vehicle_type":"bus","route":"Somebody%20told%20me"}}
```

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
    "vehicle_type": "bus",
    "route": "Somebody%20told%20me"
}
```

Otherwise, an error code is returned.

### Error codes

Error code       Description

4                Wrong input parameters.

6                Failed to update parameters.

7                No ADF_ACL_ITEM_EDIT_OTHER access right to the unit.

## update_sensor

To create, edit or delete sensors, use the unit/update_sensor method:

```http
svc=unit/update_sensor&params={
    "itemId": <long>,
    "id": <long>,
    "callMode": <text>,
    "unlink": <uint>,
    "n": <text>,
    "t": <text>,
    "d": <text>,
    "m": <text>,
    "p": <text>,
    "f": <uint>,
    "c": <text>,
    "vt": <uint>,
    "vs": <long>,
    "tbl": [
        {
            "x": <double>,
            "a": <double>,
            "b": <double>
        }
    ]
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| id | Sensor ID. Pass 0 if you want to create a sensor. |
| Parameter | Description |
| callMode | Action: create, update, delete. |
| unlink | Delete links with other sensors and unit parameters: 1 — yes (default), 0 — no. |
| To create or update a sensor, the followig parameters are also required: |  |
| Parameter | Description |
| n | Name |
| t | Type (see below). |
| d | Description. |
| m | Metrics. |
| p | Parameter. |
| f | Sensor flags (see below). |
| c | Configuration (see below). |
| vt | Validation type (see below). |
| vs | Validating sensor ID. |
| tbl | Calculation table. |

## Sensor flags

| Flag | Description |
| --- | --- |
| 0x01 | Sensor type: instant. |
| 0x02 | Sensor type: differential. |
| 0x03 | Sensor type: differential with overflow (2 bytes). |
| 0x04 | Sensor type: switch from off to on. |
| 0x05 | Sensor type: switch from on to off. |
| Activate the With overflow option. | Can be used for the following sensors: |

#### mileage

absolute fuel consumption
engine hours
0x20

If flag 0x20 is not set, the sensor works as follows: the change
delta is calculated as abs(V2 - V1), where V2 is the value from
the new message, V1 is the value from the previous message,
and abs() denotes the absolute value. If the flag is set and V2
< V1, then the delta is equal to V2 (i.e., V1 is assumed to be
0).

Apply the lower and upper bounds after calculation. If the flag
is not set, then each bound is applied to raw data (in the case
0x40   of FLS, there are difficulties with setting lower and upper
bounds for raw data). If the flag is set, then each bound is
applied to calculated (processed) data.

## Sensor types

Value                        Sensor Type

absolute fuel consumption    Absolute fuel consumption sensor

accelerometer                Accelerometer

alarm trigger                Alarm trigger

counter                      Counter sensor

custom                       Custom sensor

digital                      Custom digital sensor

driver                       Driver assignment

engine efficiency            Engine efficiency sensor

engine hours                 Absolute engine hours

engine operation             Engine ignition sensor

engine rpm                   Engine revolutions sensor

fuel level impulse sensor    Impulse fuel level sensor

fuel level                   Fuel level sensor

impulse fuel consumption     Impulse fuel consumption sensor

instant fuel consumption     Instant fuel consumption sensor

mileage                      Mileage sensor

Value                                 Sensor Type

odometer                              Relative odometer

private mode                          Private mode

relative engine hours                 Relative engine hours

temperature coefficient               Temperature coefficient

temperature                           Temperature sensor

trailer                               Trailer assignment

voltage                               Voltage sensor

weight                                Weight sensor

For further information about sensor types, see Sensor types.

## Sensor configuration parameters

The following parameters are used to configure a sensor:

"{
\"act\": <bool>,
\"appear_in_popup\": <bool>,
\"ci\": <object>,
\"filter\": <long>,
\"mu\": <uint>,
\"pos\": <uint>,
\"show_time\": <text>,
\"unbound_code\": <text>,
\"validate_driver_unbound\": <bool>,
\"do_not_show\": <bool>,

\"timeout\": <uint>,
\"uct\": <bool>,
\"lower_bound\": <double>,
\"upper_bound\": <double>,
\"text_params\": <uint>

```
}"
```

The JSON object must be enclosed in double quotes because it is sent as a
string. All key and value double quotes must be escaped (").

| Parameter | Description |
| --- | --- |
| Sensor value calculation: 0 — based on | the last unit parameters, 1 — based on the last unit message. This option uses inverted logic: |
| act | Enabled state (value 0) refers to the older, historic logic version. Disabled state (value 1) refers to the newer logic version (data is used for popups, which is useful when important parameters are received infrequently). |
| By default, the older logic version is | selected. |
| appear_in_popup | True — enable the Visible option, false — disable. |
| ci | Custom intervals. |
| filter                         Allows redefining the filtering level. Valid | for the following sensors: |

#### Fuel level

#### Temperature

| Parameter | Description |
| --- | --- |
| Voltage | Engine revolutions Accelerometer |
| Custom | Weight |
| Measurement system: |  |

#### 0 — SI

mu                           1 — US
2 — imperial
3 — metric with gallons

pos                       Sensor position in the list (count from 1)

True — display the sensor value with the
time since which this value was received.
show_time                 False — don’t show time. For further
information, read about the Time option
on the Sensors page.

For the driver or ​trailer assignment
unbound_code              sensors, you can specify a custom
separation code.

validate_driver_unbound   Validate separation: 0 — no, 1 — yes.

This parameter is used to configure the
Private mode sensor. Set it to 1 to prevent
do_not_show               the unit location data from being
transmitted when the sensor is on, or 0 to
allow this data to be received.

| Parameter | Description |
| --- | --- |
| timeout | Timeout, seconds. |
| uct | Pass 0 to enable the Overflow by raw data option. Pass 1 to disable it. The option is available only for available only for the differential counter sensors with overflow. |
| lower_bound | Lower bound of valid sensor values for the calculation table. |
| upper_bound | Upper bound of valid sensor values for the calculation table. |
| text_params | Pass 1 to enable the Text parameters option, or 0 to disable it. |
| calc_fuel | Specify 1 to activate fuel consumption calculation in reports. |
| fuel_params | Fuel level sensor settings. |
| engine_sensors | IDs of engine sensors for a fuel level sensor to calculate proper consumption. |
| engine_efficiency | IDs of engine efficiency sensors for engine sensors. |
| Example of a sensor configuration: |  |

```json
"c":"{\"appear_in_popup\":true,\"pos\":1,\"ci\":{}}"
```

Example of passing fuel_params of a fuel level sensor:

"fuel_params":{\"flags\":1728,\"ignoreStayTimeout\":20,\"minFillin
gVolume\":21,\"minTheftTimeout\":0,\"minTheftVolume\":15,\"filterQ
uality\":0,\"fillingsJoinInterval\":300,\"theftsJoinInterval\":30
0,\"extraFillingTimeout\":0}

Example of passing fuel_params of an impulse fuel consumption sensor:

"fuel_params":{\"maxImpulses\":10, \"skipZero\":0}

## Validation types

Validation type flag     Description

0x01                     Logical AND

0x02                     Logical OR

0x03                     Math AND

0x04                     Math OR

0x05                     Sum up

0x06                     Subtract validator from sensor

0x07                     Subtract sensor from validator

0x08                     Multiply

0x09                     Divide sensor by validator

0x0A                     Divide validator by sensor

Validation type flag              Description

0x0B                              Not-null check

0x0C                              Replace sensor with validator in case of error

### Response

If the request to create or edit a sensor is completed successfully, a
response in the following format is returned:

```json
[
    <long>,        /* sensor ID */
    {
        "id": <long>,            /* Sensor ID */
        "n": "<text>",           /* Name */
        "t": "<text>",           /* Type */
        "d": "<text>",           /* Description */
        "m": "<text>",           /* Metrics */
        "p": "<text>",           /* Parameter */
        "f": <uint>,             /* Sensor flags */
        "c": <object>,           /* Configuration */
        "vt": <int>,             /* validation type */
        "vs": <long>,            /* Validating sensor ID */
        "tbl": [                 /* Calculation table */
            {
                "x": <double>,
                "a": <double>,
                "b": <double>
            }
        ]
    }
]
```

If the request to delete a sensor is completed successfully, a response in
the following format is returned:

```json
[
    <sensor_id>,   // sensor IDnull
]
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4            Wrong input parameters.

6            Failed to update a parameter from the params section.

7            No ADF_ACL_AVL_UNIT_EDIT_SENSORS access right to the unit.

Unable to delete the sensor because it is used in the
2015         advanced properties of the unit or in the properties of
another sensor.

## update_service_interval

To create, edit or delete service intervals, use the
unit/update_service_interval method:

```http
svc=unit/update_service_interval&params={
      "itemId":<long>,

    "id":<long>,
    "callMode":<text>,
    "n":<text>,
    "t":<text>,
    "im":<uint>,
    "it":<uint>,
    "ie":<uint>,
    "pm":<uint>,
    "pt":<uint>,
    "pe":<uint>,
    "c":<uint>
    }
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| id | Service interval ID. |
| callMode | Action: create, update, delete. |
| To create or update a service interval, the followig parameters are also | required: |
| Parameter | Description |
| n | Interval name. |
| t | Description. |
| Parameter | Description |
| im | Mileage interval. |
| it | Day interval. |
| ie | Engine hours interval. |
| pm | Last service for a mileage interval, km. |
| pt | Last service for a day interval, s (UTC). |
| pe | Last service for an engine hours interval, h. |
| c | Number of times the service was carried out. |

### Response

If the request to create or edit a service interval is completed
successfully, a response in the following format is returned:

```json
[
    <long>,    // Service interval ID.
    {
        "id": <long>,      // Service interval ID.
        "n": "<text>",     // Name.
        "t": "<text>",     // Description.
        "im": <uint>,      // Mileage interval.
        "it": <uint>,      // Day interval.
        "ie": <uint>,      // Engine hours interval.
        "pm": <uint>,      // Last service for a mileage interval, km.
        "pt": <uint>,      // Last service for a day interval, s (UT
C).
        "pe": <uint>,      // Last service for an engine hours interva

l, h.
        "c": <uint>          // Number of times the service was carriedout.
    }
]
```

If the request to delete a service interval is completed successfully, a
response in the following format is returned:

```json
[
        <long>,        /* Service interval ID. */null
]
```

### Error codes

Error
Description
code

Wrong input parameters or failed to update the service
4
interval.

6                  Failed to delete the service interval.

No ADF_ACL_AVL_UNIT_EDIT_SENSORS access right to
7
the unit.

## update_speed_settings

To set speed parameters, use the unit/update_speed_settings method:

svc=unit/update_speed_settings&params={"itemId":<long>,
"speedParameter":"<text>",
"speedMeasure":<uint>
}

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| speedParameter | Speed parameter (parameter code from the unit message). |
| Parameter of the units of measurement. | speedMeasure       Numerical. The value is the code of the units of measurement. |

### Example

Below is an example of the unit/update_speed_settings request.

svc=unit/update_speed_settings&params={

```json
"itemId": 1583,                      // Unit ID.
"speedParameter": "speed",          // Parameter used to determine
```

speed.

```json
"speedMeasure": 0                   // Speed measurement system (fo
```

r example, 0 for km/h, 1 for mph).
}

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

6               Failed to update speed parameters.

No ADF_ACL_ITEM_VIEW_PROPERTIES access right to the
7
unit.

## update_task

The unit/update_task request allows you to edit tasks.

```http
svc=unit/update_task&params={
         "itemId": <long>,
         "taskId": <text>,
         "props": {
                  "key1": <long>,
                  "key2": <text>,
                  .....
         }
}
```

Request example:

```http
https://hst-api.wialon.com/wialon/ajax.html?sid=5e860dbe24e3d704ffb196d0733ec714&svc=unit/update_task&params={
"itemId": 1514,
"taskId": "6f6aeeebad9ebe64bda86924f8d379d8e6b06bd690c53da4aab526c
5e221bdb266b52a50",
"props": {
"task_status": 2,
"task_priority": 3
}
}
```

### Parameters

The following parameters are required:

| Name | Description |
| --- | --- |
| itemId | The ID of the unit. |
| taskId | The ID of the task (a string hash). |
| The object of properties to be updated (key-value pairs). | Include only those properties that you want to update, props     because each update fully replaces the corresponding existing property. Below is the list of flags that you can include in this parameter to update the task properties. |

### Flags

| Flag | Description |
| --- | --- |
| The status of the task. Acceptable values are: |  |
| task_status | 1 (New) 2 (To do) 3 (In progress) 4 (Paused) 5 (Rejected) 6 (Done) |
| If you change the task status from Done or | Rejected to any other status, or from any other status to Done, Rejected, or Paused, a comment is required. |
| The priority of the task. Acceptable values are: |  |
| task_priority | 1 (Low) 2 (Medium) 3 (High) |
| task_assignee | The ID of the user to whom the task is assigned. |
| The array of task comments. The comment field | task_comments   must not be empty and must not exceed 500 characters. |
| task_params     A JSON object containing additional task | parameters. Supported keys: |
| filled — amount of fuel filled | charged — amount of energy charged |
| Flag | Description |
| cost — task cost | engine_hours — vehicle engine hours mileage — vehicle mileage. |
| If a value is already set, you can change it, but not | delete it. |
| The task_comments array must be structured as follows: |  |

```json
[
      {
           timestamp: 13243,
           assignee: 1564,
           comment: "Hello world"
      },
      {
           timestamp: 13244,
           assignee: 1564,
           comment: "Hello world 2"
      }
]
```

If a comment has been previously added to the task, but its ID is not
included in the array, the comment will be deleted.

## Adding a comment

To add a comment, pass a JSON of the following format in the comment
array:

```json
{ "comment": "your comment text" }
```

## Editing a comment

To edit a comment, specify its ID in the comment array and include the new
comment text:

```json
{ "id": 23, "comment": "new comment text" }
```

## Deleting a comment

To delete a comment, remove it from the comment array.

## Adding or editing additional parameters

To add or edit additional task parameters, include the task_params object in
the props parameter with the desired key-value pairs:

```json
{
    "itemId": 1514,
    "taskId": "6f6aeeebad9ebe64bda86924f8d379d8e6b06bd690c53da4aab
526c5e221bdb266b52a50",
    "props": {
        "task_params": {
            "filled": 50.5,
            "mileage": 125.8,
            "cost": 150
        }
    }
}
```

The filled and mileage values should be provided in the unit’s current
measurement system (SI, US, imperial, or metric with gallons).

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, an error code is returned. Example:

```json
{
      "error": 5
}
```

### Error codes

Error
Description
Code

1             Invalid input parameters.

No access to the unit. The following access rights are
required:

#### View object and its basic properties

2                   Request reports and messages
Edit tasks

Edit task status and manage comments (required only
for status updates and comment management).

Error
Description
Code

No access to the user. The Act on behalf of this user
3
access right to the task assignee is required.

4            Failed to find the task with the specified ID.

5            A comment is required.

6            Invalid comment ID.

7            Unknown error.

## update_traffic_counter

To set a new value for the GPRS traffic counter, use the
unit/update_traffic_counter method:

```http
svc=unit/update_traffic_counter&params={
    "itemId": <long>,
    "newValue": <uint>,
    "regReset": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| newValue | New value of the mileage counter (km). |
| regReset | Log changes: 0 — no, 1 — yes. |

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
    "cnkb": <uint> /* Value of the GPRS traffic counter. */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4             Wrong input parameters.

6             Failed to update the GPRS traffic counter.

Error
Description
code

No ADF_ACL_AVL_UNIT_EDIT_COUNTERS access right to
7
the unit.

## update_trip_detector

To update trip detection settings, use the unit/update_trip_detector
method:

```http
svc=unit/update_trip_detector&params={
    "itemId": <long>,
    "type": <ubyte>,
    "gpsCorrection": <bool>,            (true/false)
    "minSat": <uint>,
    "minMovingSpeed": <uint>,
    "minStayTime": <uint>,
    "maxMessagesDistance": <uint>,
    "minTripTime": <uint>,
    "minTripDistance": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| Parameter | Description |
| type | Type of movement detection (see get_trip_detector). |
| gpsCorrection | Allow GPS correction: 0 – no, 1 – yes. |
| minSat | Minimum number of satellites. |
| minMovingSpeed | Minimum moving speed, km/h. |
| minStayTime | Minimum parking time, seconds. |
| maxMessagesDistance | Maximum distance between messages, meters. |
| minTripTime | Minimum trip time, seconds. |
| minTripDistance | Minimum trip distance, meters. |

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4            Wrong input parameters.

6            Failed to update the trip detector.

No ADF_ACL_AVL_UNIT_EDIT_REPORT_SETTINGS access
7
right to the unit.

## update_unique_id2

For device types with two modems, you can specify a second unique ID. To
set a new value for the second unique ID, use the
unit/update_unique_id2 method:

svc = unit/update_unique_id2&params = {

```json
"itemId": <long>,
"uniqueId2": <text>
```

}

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| uniqueId2 | New value of the second unique ID. |

### Response

If the request is completed successfully, a response in the following format
is returned:

```json
{
      "uid2": <text>
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

4                Wrong input parameters.

6                Failed to update the second unique ID.

No ADF_ACL_AVL_UNIT_EDIT_HW access right to the
7
unit.

1002             This unique ID already exists.

## update_video_autopay

Can only be used in Wialon Hosting.

To enable the automatic purchase of traffic packages, use the
update_video_autopay method. This method required dealer rights.

svc = unit/update_unique_id2&params = {

```json
    "itemId": <long>,
    "uniqueId2": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| units | Array of unit IDs. |
| The maximum number of packages per month (the | uniqueId2         limit) that can be purchased for each unit automatically. |

### Example

Below is an example of the update_video_autopay request.

svc = unit/update_video_autopay&params = {

```json
"units": [5523461,1548776],
"value": 10
}
```

### Response

If the request is completed successfully, the response contains unit IDs with
response codes (code 0 means that the changes were applied). Example:

```json
[
      {result:{5523461:{code:0}}},
      {result:{1548776:{code:0}}}
]
```

Otherwise, error code 4 is returned, indicating that the input parameters
are invalid.

## update_video_settings

Can only be used in Wialon Hosting.

The unit/update_video_settings method is used to configure the live
stream name and unload video from cameras.

```http
svc=unit/update_video_settings&params={
    "itemId":long,
    "settings":[{"name":"text","flags":int},{"name":"text","flags":int}...]}

       To send a request, you should have the Edit notmentioned properties access right to the unit.
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Unit ID. |
| name | Camera name. |
| Unloading flag. If flags:1 is indicated for a camera, the | flags     video from this camera is unloaded. If flags:0 is indicated, it is not. |

### Example

Below is an example of the unit/update_video_settings request.

```http
svc=unit/update_video_settings&params={"itemId":45644,"settings":"settings":[{"name":"Camera 1","flags":1},{"name":"Camera 2","flags":1}]}
```

### Response

If the request is successful, an empty JSON is returned.

```json
{ }
```

Otherwise, the response contains an error code.

### Error codes

Error
Description
code

4             Wrong input parameters.

6             Failed to update the video settings.

Error
Description
code

No ADF_ACL_ITEM_EDIT_OTHER access right to the unit or
7
no Video monitoring service.

## update_video_status

Can only be used in Wialon Hosting.

To enable or disable video billing for a unit, use the
unit/update_video_status method. This method requires dealer rights.

```http
svc=unit/update_video_status&params={
       "units": [<long>, ...],
       "status": <int>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| units | Array of unit IDs. |
| status | Pass 0 to disable video billing or pass 1 to enable it. |

### Example

Below is an example of the unit/update_video_settings request.

```http
svc=unit/update_video_status&params={
    "units": [5523461, 1548776],
    "status": 1
}
```

### Response

If the request is completed successfully, the response contains unit IDs with
response codes (code 0 means that the changes were applied). Example:

```json
[
      {result:{5523461:{code:0}}},
      {result:{1548776:{code:0}}}
]
```

Otherwise, error code 4 is returned, indicating that the input parameters
are invalid.

## upload_file

To upload a file for a unit, use the unit/upload_file method:

```http
svc=unit/upload_file&params={
    "eventHash": <text>,
    "toHex": <uint>
}
```

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| toHex* | Use a bin to string parser: 0 — no, 1 — yes. |
| eventHash | Event name which will be generated after uploading the image. |

## Uploading the file

To upload a file, use a POST request with multiple contents (multipart/form-
data), where one part contains the parameters and the other contains the
file. For example:

Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=excha
nge/import_json&sid=8157df114c0e601f0f31091c3c2ac53d
Request Method: POST
Connection: keep-alive
Content-Length: 1901
Cache-Control: no-cache
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
hAXcAjtvh1D61XpC
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/
*;q=0.8
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3
Accept-Encoding: gzip,deflate,sdch
Accept-Language: ru,en-US;q=0.8,en;q=0.6

------WebKitFormBoundaryhAXcAjtvh1D61XpC
Content-Disposition: form-data; name="params"

```json
{"eventHash":"jUploadForm1372772377019"}
------WebKitFormBoundaryhAXcAjtvh1D61XpC

Content-Disposition: form-data; name="eventHash"

{"toHex":1}
------WebKitFormBoundaryhAXcAjtvh1D61XpC
Content-Disposition: form-data; name="toHex"

jUploadForm1372772377019
------WebKitFormBoundaryhAXcAjtvh1D61XpC
Content-Disposition: form-data; name="import_file"; filename="file.zip"
Content-Type: application/zip

------WebKitFormBoundaryhAXcAjtvh1D61XpC--
```

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

To make sure the file has been uploaded, use the requests/avl_evts
method.

If the request fails, error code 4 is returned, indicating that the input
parameters are invalid.

## upload_image

To upload an image for a unit, use the unit/upload_image method:

```http
svc=unit/upload_image&params={
     "itemId": <long>,
     "eventHash": <text>
}
```

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Unit ID. |
| eventHash | Event name which will be generated after uploading the image. |

## Uploading the image

To upload an image, use a POST request with multiple contents
(multipart/form-data), where one part contains the parameters and the
other contains the image. For example:

Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=unit/
upload_image&sid=8157df114c0e601f0f31091c3c2ac53d
Request Method: POST
Host: hst-api.wialon.com
Connection: keep-alive
Content-Length: 31720
Cache-Control: no-cache
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
ECovXn5tfw5muHk8
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/
*;q=0.8
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3
Accept-Encoding: gzip,deflate,sdch
Accept-Language: ru,en-US;q=0.8,en;q=0.6

------WebKitFormBoundaryECovXn5tfw5muHk8
Content-Disposition: form-data; name="params"

```json
{"itemId":911903,"eventHash":"jUploadForm1372769354768"}
------WebKitFormBoundaryECovXn5tfw5muHk8
Content-Disposition: form-data; name="eventHash"

jUploadForm1372769354768
------WebKitFormBoundaryECovXn5tfw5muHk8
Content-Disposition: form-data; name="icon_file"; filename="image.jpg"
Content-Type: image/jpeg

------WebKitFormBoundaryECovXn5tfw5muHk8--
```

### Response

If the request is completed successfully, an empty object is returned:

```json
{}
```

To make sure the image has been uploaded, use the requests/avl_evts
method.

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4                Wrong input parameters.

6                Failed to save the image.

Error
Description
code

No AADF_ACL_ITEM_EDIT_IMAGE access right to the
7
unit.
