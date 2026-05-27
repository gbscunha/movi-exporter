# events

This section provides all the methods for working with events.

## check_updates

To get all event updates of all units added into the session, use
the events/check_updates request.

```http
svc=events/check_updates&params={
      "lang": <text>,
      "measure": <uint>,
      "detalization": <uint>
}
```

### Parameters

All parameters are optional.

Default

| Parameter | Description |
| --- | --- |
| value |  |
| lang | Language (2-symbol code).                   en |
| Measurement system: |  |
| 0 for SI; | measure                                                      0 1 for US; |
| 2 for imperial. |  |
| Output flags (see below). Must be | detalization                                                 0x7 specified in decimal format. |

## Output flags

| Flag | Description |
| --- | --- |
| 0x1 | Basic JSON: event start - event end. |
| 0x2 | Specified detector data. |
| 0x4 | User parameters (which user specified for this event) |
| 0x10 | Full JSON. Every detector treats it in its own way. |
| 0x20 | Formatted value. |

## Sensor type

Type
Description                          Event registration
value

Switcher sensors:

engine operation;
digital;

engine efficiency;               Events are registered from the
1                                             ON state
private mode;
to the OFF state.
alarm trigger;
counter (switch to
ON/OFF).

2        Instant sensors:                     Events are registered from the
first non-
odometer;                        zero value to the last non-zero
relative engine                  one.
hours;

instant fuel
consumption;
counter (instant).

Differential sensors:

mileage;
engine hours;
impulse fuel
consumption;
Events are registered from the
absolute fuel
3                                              start of value increasing to the
consumption;
end of it.
counter (differential,
differential with
overflow);
fuel level impulse
sensor.

Analog sensors:

temperature;
engine revolutions;
voltage;

4             weight;                          Events are not registered.
accelerometer;

temperature
coefficient;
custom sensor.

### Response

The response depends on the flag.

## 0x1 flag

Returns basic JSON (for all sensor groups).

"<type_name>": {
"<sensor_id>": {

```json
"from": {
"t": <uint>, /* time (UNIX time) */
"y": <double>, /* latitude */
"x": <double> /* longitude */
},
"to": {
"t": <uint>, /* time (UNIX time) */
"y": <double>, /* latitude */
"x": <double> /* longitude */
},
"m": <uint>, /* last message time */
"f": <uint> /* service flag */
}
}
```

## 0x2 flag

Returns specified detector data.

```json
"ignition": {
"<sensor_id>": {
"state": <uint>, /* state: 0 for off, 1 for on */
"type": 1, /* sensor type: switcher sensor */
"hours": <uint>, /* engine hours for all history, in seconds */
"switches": <uint>, /* number of switches for all history */
"value": <bool> /* current value */
}
...
}
```

All sensor types for sensors:

```json
"sensors": {
"<sensor_id1>":
{
"state":<uint>, /* state: 0 for off, 1 for on */
"type": 1, /* sensor type: switcher sensor */
"hours":<uint>, /* engine hours for all history, s */
"switches":<uint>, /* number of switches for all history */
"value":<bool> /* current value */
},
"<sensor_id2>":
{
"type": 2, /* sensor type: instant sensor */
"counter":<uint>, /* message sequence counter in the event */
"summary":<uint>, /* sum of values in the event */
"total_counter":<uint>, /* number of messages in the history */
"total_summary"<uint>, /* sum of values in the history */
"value":<double> /* last value; if it's -348201.3876, the value isunknown */
},
"<sensor_id3>":
{
"type": 3, /* sensor type: differential sensor */
"counter":<uint>, /* value sum in the event */
"total_counter":<uint>, /* value sum in the history */
"value":<double> /* last value; if it's -348201.3876, the value isunknown */
},
"<sensor_id4>":
{
"type": 4, /* sensor type: analog sensor */
"value":<double> /* last value; if it's -348201.3876, the value isunknown */
}
}

"lls": {
    "<sensor_id>":
              {
                  "value":<double>,          /* last message value with the calculated "level" */
                  "level":<double>,          /* average median value
(FLS filtering value is used) */
                  "filled":<double>          /* fuel filled */
              }
}

"trips": {
          "state":<bool>,        /* state: 0 for a parking interval,
1 for a trip, 2 for a stop */
          "max_speed":<uint>,    /* maximum speed in the trip */
          "curr_speed":<uint>,   /* current speed */
          "avg_speed":<uint>,    /* average speed according to "distance" */
          "distance":<uint>,     /* GPS mileage in trip */
          "odometer":<uint>,     /* distance for all trips */
          "course":<uint>,   /* movement direction*/
          "altitude":<uint> /* altitude */
}

"counters": {
    "engine_hours": <uint>,      /* engine hours counter */
    "mileage": <uint>,           /* mileage counter */
    "bytes": <uint>              /* GPRS traffic counter */
}
```

## 0x4 flag

Returns user parameters. The response depends on user definitions for the
current event.

"<type_name>": {
"<sensor_id>": {

```json
          "p":{    /* user-defined object content */
               "test":2,
               "foo":"bar",
               "trips":1
          }
      }
}
```

## 0x10 flag

Returns the full JSON.

For sensors with both ‘‘type=2’’ and ‘‘type=3’’ (except fuel level sensors),
the following response is returned:

```json
"sensors": {
"<sensor_id>":
{
"msgs": [
{
"tm":<uint>, /* message time, UNIX-time */
"v":<double> /* value */
},
...
]
},
...
}
```

For fuel level sensors, the following response is returned:

"lls": {
"<sensor_id>": {

```json
"msgs": [
         {
         "tm":<uint>,     /* message time, UNIX-time */
         "v":<double>, /* value */
         "l":<double>   /* average median value     (FLS filtra
```

tion value is used) */

```
               },
               ...
           ]
      }
},
...
```

}

## 0x20 flag

## Returns formatted values

"ignition": {

```json
"sensor_id": {
      "format": {
               "value":<text>        /* formatted value   (usually "O
```

n"/"Off") */

```
      }
}
```

}

"sensors": {

```json
"sensor_id": {
      "format": {
               "value":<text>        /* formatted value, depends on t
```

he sensor type and format */

```
       }
}
```

}

"trips": {

```json
"format": {
       "distance":<text>,            /* distance according to the pre
```

vious message */

```json
"avg_speed":<text>            /* average speed according to "d
```

istance"       */

```
}
```

}

"lls": {

```json
"sensor_id": {
       "format": {
                "value":<text>,      /* formatted value, depends on t
```

he sensor type and format */

```json
                "filled":<text>      /* fuel filled */
       }
}
```

}

"counters": {

```json
"format": {
"engine_hours":<uint>,       /* formatted value of the engine
```

hours counter */

```json
"mileage":<text>,            /* formatted value of the mileage
```

counter */

```json
"bytes":<uint>               /* formatted value of the GPRS tr
```

affic counter */

```
        }

}
```

### Error codes

If the request is not completed, an error code is returned.

Error
Description
code

1             Invalid or obsolete request SID.

4             Parameter validation error.

The adf_avl_events library wasn't loaded, or failed to
7
fetch the JSON writer.

## load

To load events for a specified period into the session for later processing,
use the events/load request.

```http
svc=events/load&params={"itemId":<long>,
             "ivalType":<int>,
             "timeFrom":<uint>,
             "timeTo":<uint>,
             "detectors":[
                 {
                      "type":<text>,
                      "filter1":<uint>
                 },

                 ...
          ]}
```

### Parameters

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| ivalType | Algorithm type (see below). |
| timeFrom | Interval beginning (UNIX time) if 1, 4, 5 or 6 is specified in ivalType. Number of requested messages if 2 or 3 is specified in ivalType. |
| timeTo | Interval end (UNIX time). |
| type | Sensors group: lls, sensors, ignition, trips. See more. |
| filter1 | Sensor ID. Specify 0 to add all sensors according to the selected type. |
| Measurement system: |  |
| 0 for SI; |  |
| measure | 1 for US; 2 for imperial. |
| The default value is 0. |  |
| lang | Language (2-symbol code). The default value is en. |
| If you need to load events for another period into the session, first use the | events/unload request and then events/load. |

## ivalType

Value     Description

1         Requests messages (events) from timeFrom to timeTo.

Requests the number of messages specified in timeFrom,
2
beginning from timeTo.

Requests the number of messages specified in timeFrom,
3
up to timeTo.

Requests messages from timeFrom to timeTo, including
4
one message before timeFrom.

Requests messages from timeFrom to timeTo, including
5
one message after timeTo.

Requests messages from timeFrom to timeTo, including
6         one message before timeFrom and one message after
timeTo.

### Response

If the request is completed successfully, the following response is returned:

```json
{
"events":{
"counters":{
"0":<uint> /* The number of events, that is, counter value updatesin the history request. */

},
"ignition":{
"<sensor_id1>":<uint>, /* The number of events in the history request for the specified sensor. */...
},
"lls":{
"<sensor_id2>":<uint>, /* The number of events in the history request for the specified sensor */...
},
"sensors":{
"<sensor_id3>":<uint>, /* The number of events in the history request for the specified sensor */...
"trips":{
"0":<uint> /* The number of events in the history request for trips */
}
},
"selector":[
{
...
}, /* Selection results. If the "selector" parameter was skipped,
then {} is returned. You can see the server response in "events/get". */...
]
}
```

If the request is not completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| Code | Description |
| One of the following errors: |  |
| error validating parameters, | 4 error fetching the history loader, empty list of detectors. |
| 5 | Events are disabled or initializing. |
| 6 | Failed to load events or fetch the JSON writer. |
| The adf_avl_events library wasn’t loaded or failed to fetch | 7        the item with the required access right (ADF_ACL_ITEM_EXECUTE_REPORTS). |

## unload

To unload all events from the session, execute the events/unload request.

```http
svc=events/unload&params={}
```

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 4 | Parameter validation error. |
| 7 | Failed to load the adf_avl_events library. |

## update_units

For adding units into the session, use the events/update_units request.

```http
svc=events/update_units&params={"mode":"add",
                 "units":[
                          {
                          "id":<long>,
                          "detect":
                                {
                                      "trips":<uint>,
                                      "lls":<uint>,
                                      "sensors":<uint>,
                                      "ignition":<uint>,
                                      "counters":<uint>
                                }
                          },
                          ...
                 ]}
```

To remove specific units from the session, use the following signature:

```http
svc=events/update_units&params={"mode":"remove",
                 "units":[<long>]}
```

To remove all units from the session, use the following signature:

```http
svc=events/update_units&params={"mode":"clear"}
```

### Parameters

| Parameter | Description |
| --- | --- |
| mode | Mode: add, remove, clear. |
| id | Unit ID. |
| detect | Sensor types (what to monitor). |
| trips | Trips (see below). |
| lls | Fuel level sensor (see below). |
| ignition | Ignition sensor (see below). |
| sensors | Other sensors not mentioned above (see below). |
| counters | Counters. |
| evt_flags | Event flags. See the Event flags section. |
| To work with the “detect” elements (trips, lls, sensors, ignition) use a | specific sensor ID or indicate 0 to add all the sensors of a certain type. For trips, always use 0 as there is no trip sensor. |
| To add all unit sensors, use: |  |

```json
"detect":{"*":0}
```

## Example 1

To add all ignition sensors and other sensors, use:

```json
"detect":{"ignition":0,"sensors":0}
```

## or

```json
"detect":{"ignition,sensors":0}
```

## Example 2

To add all fuel level sensors with ID 2 and other sensor with ID 6:

```json
"detect":{"lls":2,"sensors":6}
```

## Event flags

The evt_flags parameter controls which event processing mode is used
when events/check_updates is called.

Value       Name      Description

check_u   Default mode. The events/check_updates method
0
pdates    polls detectors and returns event data.

Alternative processing mode. When this bit is set,
events/check_updates returns an empty result {}
evt_evt
0x200                 immediately (events are delivered through a
s
different channel). The lower 9 bits (bits 0-8) are
reserved for detail flags.

Detail flags are combinable via bitwise OR and used in the lower 9 bits
when 0x200 is set. The following detail flags are available:

Flag                        Value             Description

AVL_EVENTS_HISTORY_BASE
0x1               Event start and end time
_JSON

AVL_EVENTS_HISTORY_DETE
0x2               Base detector data
CTOR_JSON

AVL_EVENTS_HISTORY_MSGS
0x4               Additional message parameters
_PARAMS_JSON

AVL_EVENTS_HISTORY_EXTE                       Extended information beyond
0x8
NDED_JSON                                     base data

AVL_EVENTS_HISTORY_FULL
0x10              Full history JSON
_JSON

AVL_EVENTS_HISTORY_FORM                       Format event values as human-
0x20
AT_TEXT                                       readable text

Flag                          Value           Description

AVL_EVENTS_HISTORY_GROU
0x40            Group results by intervals
P_INTERVALS

AVL_EVENTS_HISTORY_SUMM
0x80            Include summary calculations
ARY

AVL_HISTORY_EXTENDED_EV
0x100           Extended events
ENTS

For example, evt_flags = 0x207 means using the evt_evts mode (0x200)
with the base, detector, and message parameter detail flags enabled (0x1 |
0x2 | 0x4 = 0x7).

### Response

If the request is completed successfully, the following response is returned:

```json
{
      units:<uint>         /* number of units added into session */
}
```

Otherwise, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 4 | Parameter validation error. |
| 7 | Failed to load the adf_avl_events library. |

## get

After loading the events into the session, you can view them by executing
the events/get method.

```http
svc=events/get&params={
    "selector": {
         "type": <text>,
         "expr": <text>,
         "timeFrom": <uint>,
         "timeTo": <uint>,
         "detalization": <uint>
    },
    ...
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| type | Sensor group: lls, trips, ignition, sensors, counters. To specify all the groups, use the asterisk (*). |
| expr | Interval group expression. Used instead of the type parameter to get custom event intervals. See below. |
| timeFrom | Interval start, UNIX-time. |
| timeTo | Interval end, UNIX-time. |
| Parameter | Description |
| detalization | Output flags (see below). |
| indexFrom | Index of the first requested event. |
| indexTo | Index of the last requested event. |
| filter1 | Sensor ID. |

### Flags

| Flag | Description |
| --- | --- |
| 0x1 | Basic JSON: event start and end. |
| 0x2 | Data of a specific detector. |
| 0x4 | User parameters (that the user specified for this event). |
| 0x8 | Track data in the trips parameter. |
| 0x10 | Full JSON. Every detector interprets it in its own way. |
| 0x20 | Formatted value. |
| Grouping the intersections of intervals with the tf and tt | 0x40 parameters. |
| 0x80 | Summary. |

## Custom event intervals

To get custom event intervals, specify an expression
in the “expr”: parameter instead of using the type parameter. You can
use the following expression formats:

Operator      Description                                Example

Used for selecting intervals with the
specified value of the detalization
{}            parameter. See the example for             trips{s>100}
selecting trip intervals in which the
speed value exceeds 100.

Used for specifying a custom interval      1451953325-
-
in the start-end format, UNIX-time.        1451953525

(1615849200-
Used as a separator when specifying        1615935599|161
|
multiple custom intervals.                 5935601-
1616022000)

Sensor ID. If no ID is specified, the
[]                                                       sensors[3]
first sensor is used.

### Response

If the request is completed successfully, you will receive the response
corresponding to the sensor group specified in the type parameter.
Otherwise, an error code is returned.

## 0x1 flag

Returns basic JSON (the same for all sensor groups).

"<type_name>": {
"<sensor_id>": {

```json
         "from": {
              "t": <uint>,   // Time (UNIX time)
              "y": <double>,// Latitude
              "x": <double> // Longitude
         },
         "to": {
              "t": <uint>,   // Time (UNIX time)
              "y": <double>,// Latitude
              "x": <double> // Longitude
         },
         "m": <uint>,        // Last message time
         "f": <uint>         // Service flag
     }
}
```

## 0x2 flag

Returns data of a specific detector.

```json
"ignition": {
     "<sensor_id>": {
         "state": <uint>,        // State: 0 — off, 1 — on
         "type": 1,             // Sensor type: switcher sensor
         "hours": <uint>,        // Engine hours for all history (in seconds)
         "switches": <uint>, // Number of switches for all history
         "value": <bool>         // Current value
     }
}
```

Below are the possible sensor types for sensors.

"sensors": {
"<sensor_id1>": {

```json
"state": <uint>,        // State: 0 — off, 1 — on
"type": 1,              // Sensor type: switcher sensor
"hours": <uint>,        // Engine hours for all history (in se
```

conds)

```json
     "switches": <uint>,     // Number of switches for all history
     "value": <bool>         // Current value
},
"<sensor_id2>": {
     "type": 2,              // Sensor type: instant sensor
     "counter": <uint>,      // Number of sequential messages in th
```

e event

```json
"summary": <uint>,      // Sum of values in the event
"total_counter": <uint>,// Total number of messages in all his
```

tory

```json
"total_summary": <uint>,// Total value sum in all history
"value": <double>       // Last value; if -348201.3876, the va
```

lue is unknown

```json
},
"<sensor_id3>": {
     "type": 3,              // Sensor type: differential sensor
     "counter": <uint>,      // Sum of values in the event
     "total_counter": <uint>,// Sum of values in the history
     "value": <double>       // Last value; if -348201.3876, the va
```

lue is unknown

```json
},
"<sensor_id4>": {
     "type": 4,              // Sensor type: analog sensor
     "value": <double>       // Last value; if -348201.3876, the va
```

lue is unknown

```
}
```

}

"lls": {
"<sensor_id>": {

```json
"value": <double>, // Last message value with the calculated l
```

evel

```json
"level": <double>, // Average median value (after FLS filtrati
```

on)

```json
    "filled": <double> // Amount of fuel filled
}
```

}

"trips": {

```json
"state": <bool>,         // Trip state: 0 — parking, 1 — trip, 2 —
```

stop

```json
"max_speed": <uint>,     // Maximum speed during the trip
"curr_speed": <uint>,    // Current speed
"avg_speed": <uint>,     // Average speed based on distance
"distance": <uint>,      // GPS mileage during the trip
"odometer": <uint>,      // Total distance for all trips in the hi
```

story

```json
"course": <uint>,        // Course
"altitude": <uint>       // Altitude
```

}

"counters": {

```json
"engine_hours": <uint>, // engine hours counter
"mileage": <uint>,        // mileage counter
"bytes": <uint>           // GPRS traffic counter
```

}

"speedings": {

```json
"max_speed": <uint>,    // Speed at the time of the maximum speedi
```

ng — the moment of the greatest difference between permitted and a
ctual speed

```json
"last_speed": <uint>, // Speed from the last message within the
```

interval

```json
    "limit": <uint>             // Road speed limit
}
```

## 0x4 flag

Returns user parameters. The response depends on the parameters the
user has specified for the event.

"<type_name>": {
"<sensor_id>": {

```json
        "p": {                   // User-defined object content
            "test": 2,
            "foo": "bar",
            "trips": 1
        }
    }
}
```

## 0x8 flag

Returns JSON with additional parameters. For trips, returns a unit track in
Google notation.

```json
{
    "trips": {
        "0": [
            {
                "track": "wspnGgvcv@??oey@kwl@~dtBkeRwjzF??~ja@_qo]??g~g
^????????????~bV???????"
            }
        ]
    }
}
```

## 0x10 flag

Returns full JSON.

For sensors with type=2 and type=3 (except fuel level sensors), the response
looks as follows:

```json
"sensors": {
     "<sensor_id>": {
          "msgs": [
              {
                   "tm": <uint>,   // Message time (UNIX time)
                   "v": <double>   // Value
              },
              ...
          ]
     },
     ...
}
```

For a fuel level sensor, the response looks as follows:

```json
"lls": {
     "<sensor_id>": {
          "msgs": [
              {
                   "tm": <uint>,   // Message time (UNIX time)
                   "v": <double>, // Value
                   "l": <double>   // Average median value (FLS filtration applied)
              },
              ...
          ]
     }
},
...
```

## 0x20 flag

Returns formatted values.

"ignition": {
"<sensor_id>": {

```json
    "format": {
        "value": <text>   // Formatted value (usually "On"/"Off")
    }
}
```

}

"sensors": {
"<sensor_id>": {

```json
"format": {
    "value": <text>   // Formatted value, depends on the sensor t
```

ype and format

```
    }
}
```

}

"trips": {

```json
"format": {
    "distance": <text>,      // Distance based on the previous messag
```

e

```json
"avg_speed": <text>      // Average speed in relation to "distanc
```

e"

```
}
```

}

"lls": {
"<sensor_id>": {

```json
"format": {
    "value": <text>,       // Formatted value, depends on the sensor
```

type and format

```json
        "filled": <text>       // Fuel filled
    }
}
```

}

"counters": {

```json
"format": {
    "engine_hours": <uint>,        // Formatted value of the engine hour
```

s counter

```json
"mileage": <text>,             // Formatted value of the mileage cou
```

nter

```json
"bytes": <uint>                // Formatted value of the GPRS traffi
```

c counter

```
}
```

}

## 0x40 flag

"selector": [

```json
{
    "tf": <uint>,      // Intersection interval start (UNIX time)
    "tt": <uint>,      // Intersection interval end (UNIX time)
    "d": {
        "<type_name>": {
            "<sensor_id>": [
                { }
            ]
        }
    }
}
```

]

## 0x80 flag

"selector": {
"<type_name>": {
"<sensor_id>": [

```json
        { }
    ]
}
```

},

"summary": {
"<type_name>": {
"<sensor_id>": {
"<summary_param_value>": <uint>,       // Summary; meaning varies
for different detectors

```json
"format": {
    "value": <text>   // Formatted value, depends on the sensor
```

type and format

```
        }
    }
}
```

}

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 4 | Parameter validation error. |
| 7 | Failed to load the adf_avl_events library. |
