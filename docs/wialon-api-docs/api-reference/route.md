# route

This section describes the methods that can be applied to routes. To create
a route, see the core/create_route method.

## get_all_rounds

To get information about rides for a specified time interval, use the
route/get_all_rounds method:

```http
svc=route/get_all_roundsparams={
    "itemId": <long>,
    "timeFrom": <uint>,
    "timeTo": <uint>,

    "fullJson": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| timeFrom | Interval beginning. |
| timeTo | Interval end. |
| fullJson | Response format. Pass 1 for detailed information, or 0 for basic information. |

### Response

If the request is completed successfully, the response contains either basic
or detailed information about rides, depending on the value of the fullJson
parameter.

A response with basic information is returned in the following format:

```json
{
    "actual": [    /* Rides with the "in progress" and "finished" states. */
         {
             ...
         }
    ],

  "history": [ /* Rides with the "history" state. */
       {
           ...
       }
  ],
  "virtual": [ /* Rides with the "estimated" state. */
       {
           "time": <uint>,        /* Ride beginning. */
           "schedule": {
             "id": <long>,            /* Schedule ID. */
             "n": <text>,             /* Schedule name. */
             "f": <uint>,             /* Type. */
             "tz": <uint>,            /* Timezone. */
             "cfg": {                 /* Custom configuration. It is passed fro
```

m the schedule object without changes. */

```json
"autoName": <uint>,                  /* Generate ride names automa
```

tically: 0 —              no, 1 —   yes. */

```json
"enabled": 1,                        /* Automatic creation of ride
```

s: 1 —         enable, 0 —       disable. */

```json
     "name": <text>,                      /* Ride name. */
     "description":<text>, /* Description. */
     "roundFlags": <uint>,                /* Ride flags. */
     "units": [<long>],                   /* Array of unit IDs. */
     "validityPeriod": <uint>             /* Validity period. */
},
"tm": [ /* Time of passing checkpoints. */
     {
         "at": <uint>,     /* Arrival time. */
         "ad": <uint>,     /* Deviation from the arrival time. */
         "dt": <uint>,     /* Departure time. */
         "dd": <uint>      /* Deviation from the departure time.
```

*/

```json
                  }
             ],
             "sch": {
                  "f1": <uint>,       /* Beginning of interval 1. */
                  "f2": <uint>,       /* Beginning of interval 2. */
                  "t1": <uint>,       /* End of interval 1. */
                  "t2": <uint>,       /* End of interval 2. */
                  "m": <uint>,        /* Mask of days of month. */

                    "y": <uint>,   /* Mask of months */
                    "w": <uint>    /* Mask of days of the week. */
                }
            }
        }
    ]
}
```

The format of the actual and history arrays is similar to the one described
on the load_rounds page (basic information).

Schedule types are described on the update_schedule page.

A response with detailed information is similar to the one with basic
information, except that the format of elements in the actual and history
arrays is the same as the one described on the get_round_data page.

## get_round_data

To get detailed information about rides, use the route/get_round_data
method:

```http
svc=route/get_round_dataparams={
    "itemId": <long>,
    "col": [<long>]
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| Parameter | Description |
| col | Array of ride IDs. |

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
[
     {
         "id": <long>,             // Ride ID.
         "n": <text>,              // Name.
         "d": <text>,              // Description.
         "tz": <uint>,             // Timezone.
         "u": <long>,              // Assigned unit ID (if not specified, uses the first unit from "cu" that leaves the first checkpoint).
         "cu": [<long>],           // Array of unit IDs.
         "pt": [                   // Checkpoints.
              {
                  "n": <text>,     // Name.
                  "f": <uint>,     // Type.
                  "u": <long>,     // Unit ID (0 if not of the "checkpointfrom unit" type).
                  "y": <double>,   // Latitude.
                  "x": <double>,   // Longitude.
                  "r": <uint>      // Radius.
              }
         ],
         "sh": {                   // Schedule.
              "id": <long>,        // Schedule ID.
              "n": <text>,         // Name.
              "f": <uint>,         // Type.
              "tz": <uint>,        // Timezone.
              "cfg": {             // Custom configuration. It is passed from the schedule object without changes.

           "enabled": <byte>,            // Automatic creation of rides:
```

1 — enabled, 0 — disabled.

```json
          "name": <text>,               // Ride name.
          "description": <text>,        // Description.
          "roundFlags": <uint>,         // Ride flags.
          "units": [<long>],            // Unit IDs.
          "validityPeriod": <uint>      // Validity period.
     },
     "tm": [                  // Time of passing checkpoints.
          {
              "at": <uint>,    // Arrival time.
              "ad": <uint>,    // Deviation from the arrival time.
              "dt": <uint>,    // Departure time.
              "dd": <uint>     // Deviation from the departure time.
          }
     ],
     "sch": {                  // Time restrictions.
          "f1": <uint>,        // Start of interval 1.
          "f2": <uint>,        // Start of interval 2.
          "t1": <uint>,        // End of interval 1.
          "t2": <uint>,        // End of interval 2.
          "m": <uint>,         // Day-of-month mask.
          "y": <uint>,         // Month mask.
          "w": <uint>          // Day-of-week mask.
     }
},
"at": <uint>,                  // Activation time.
"vt": <uint>,                  // Start of validity period.
"vp": <uint>,                  // Validity period.
"f": <uint>,                   // Ride flags.
"st": {                       // Ride state.
     "st": {                  // General ride state.
          "pi": <uint>,        // Checkpoint index (4294967295 means th
```

e ride has not started).

```json
        "ps": <uint>,        // State flags and event flags.
        "ut": <uint>         // Time of the last event.
   },
   "pts": {                  // State by individual checkpoint.
        "<text>": {
            "st": <uint>,    // Event flags.

                "tm": <uint>     // Time of the last event.
            }
            // ... more checkpoints
        }
    }
}
```

]

Checkpoint types are described on the update_checkpoints page.

Schedule types are described on the update_schedule page.

## Ride flags

| Flag | Description |
| --- | --- |
| 0x0 | Checkpoint order: strict. |
| 0x2 | Remove finished rides from the timeline. |
| 0x10 | Checkpoint order: skipping is possible. |
| 0x20 | Allows running reports on rides. |
| 0x40 | Checkpoint order: arbitrary. |

## Ride state flags

| Flag | Description |
| --- | --- |
| 0x010000 | Not active. |
| Flag | Description |
| 0x020000 | Finished. |
| 0x040000 | Expecting arrival. |
| 0x080000 | Expecting departure. |
| 0x200000 | Behind schedule. |
| 0x400000 | Ahead of schedule. |
| 0x800000 | Stopped. |
| 0x0100000 | Aborted. |

## Event flags

| Flag | Description |
| --- | --- |
| 0x1 | The ride started. |
| 0x2 | The ride finished. |
| 0x4 | The ride was aborted. |
| 0x8 | The unit arrived at a checkpoint. |
| 0x10 | The unit passed a checkpoint. |
| 0x20 | The unit departed from a checkpoint. |
| Flag | Description |
| 0x40 | The unit arrived late. |
| 0x80 | The unit arrived ahead of time. |
| 0x100 | The unit passed a checkpoint on time. |
| 0x200 | The arrival was postponed. |

## get_schedule_time

To get the start time of rides for a specified interval, use the
route/get_schedule_time method:

```http
svc=route/get_schedule_timeparams={
    "itemId": <long>,
    "scheduleId": <long>,
    "timeFrom": <uint>,
    "timeTo": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| Parameter | Description |
| scheduleId | Schedule ID. |
| timeFrom | Interval beginning. |
| timeTo | Interval end. |

### Response

If the request is completed successfully, the response contains the start
time of the rides.

```json
[
    {
        "time": <uint>   // Time of ride beginning (Unix timestamp).
    }
]
```

The maximum number of entries that can be returned is 100. The number
of rides is limited to one ride per day.

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4                Invalid input parameters.

Error
Description
code

Internal error or missing ADF_ACL_ITEM_VIEW access
7
right to the route.

## load_rounds

To load the rides of a certain route for a specified period, use the
route/load_rounds method:

svc = route/load_rounds

```json
params = {
    "itemId": <long>,
    "timeFrom": <uint>,
    "timeTo": <uint>,
    "fullJson": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| timeFrom | Interval beginning. |
| timeTo | Interval end. |
| Parameter | Description |
| fullJson | Response format. Pass 1 for detailed information, or 0 for basic information. |

### Response

If the request is completed successfully, the response contains either basic
or detailed information about the route rides, depending on the value of the
fullJson parameter.

A response with basic information is returned in the following format:

```json
[
    {
        "id": <long>,          // Ride ID.
        "ct": <long>,          // Ride creation time (UNIX).
        "mt": <long>,          // Ride update time (UNIX).
        "n": <text>,           // Ride name.
        "d": <text>,           // Description.
        "sh": <text>,          // Schedule name.
        "f": <uint>,           // Ride flags.
        "tz": <uint>,          // Timezone.
        "u": <long>,           // Unit assigned to this ride.
        "at": <uint>,          // Activation time (Unix timestamp).
        "vt": <uint>,          // Start of the validity period (Unix timestamp).
        "vp": <uint>,          // Validity period (seconds).
        "sts": <uint>,         // Ride state flags.

        "st": {                // Ride state.
          "st": {              // General ride state.
            "pi": <uint>,      // Checkpoint index (4294967295 if not started).
            "ps": <uint>,      // State flags and event flags.
            "ut": <uint>       // Last event time (Unix timestamp).

              },
              "pts": {                 // State by individual checkpoint.
                   "<checkpoint_id>": {
                       "st": <uint>,   // Event flags.
                       "tm": <uint>    // Last event time.
                   }
                   // ... additional checkpoints
              }
         }
    }
]
```

You can find state flags and event flags on the get_round_data page.

A response with detailed information has the same format as the one
described on the get_round_data page.

## optimize

To solve the travelling salesman problem, that is, to build the best route for
passing all the specified checkpoints and get the time of arrival at each of
them, use the route/optimize method:

```http
svc=route/optimize&params={
    "pathMatrix": [
         [<uint>, ...],
         ...
    ],
    "pointSchedules": [
         {
              "from": <uint>,
              "to": <uint>,
              "waitInterval": <uint>
         },
         ...
    ],

   "flags": <uint>
```

}

### Parameters

| Parameter | Description |
| --- | --- |
| pathMatrix | Matrix specifying the movement time (in minutes) between the points (see below). |
| Schedule specifying the visit and wait time for each | pointSchedules         point. The number of elements must equal the number of elements in the pathMatrix parameter. |
| from                   Parameters defining the time interval (in minutes) | to                     within which the courier should visit the point. |
| waitInterval | Time (in minutes) the courier should wait at a point after arrival. |
| flags | Problem condition flags (see below). |

## pathMatrix

The pathMatrix parameter must always be a square matrix, where the
size corresponds to the number of the specified points.

Example:

"pathMatrix": [[0, 1, 2], [3, 0, 4], [5, 6, 0]]

This input defines the movement time (in minutes) between three points. In
other words, it shows how long it takes to travel from one point to another.

Let’s analyze each row of the matrix.

The first row [0, 1, 2] means:

From point 1 to point 1: 0 minutes
From point 1 to point 2: 1 minute

#### From point 1 to point 3: 2 minutes

The second row [3, 0, 4] means:

#### From point 2 to point 1: 3 minutes

From point 2 to point 2: 0 minutes
From point 2 to point 3: 4 minutes

The third row [5, 6, 0] means:

From point 3 to point 1: 5 minutes
From point 3 to point 2: 6 minutes

#### From point 3 to point 3: 0 minutes

There is always a zero in each row because it represents the travel time
from a point to itself.

### Flags

Problem condition flags are represented as hexadecimal values.

| Flag | Description |
| --- | --- |
| 0x01 | The pointSchedules data becomes a mandatory condition. |
| 0x08 | It is mandatory to start the route from the first point. |
| 0x10 | It is mandatory to end the route in the last point. |

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "success": <bool>,        /* A value of 1 means the problem is solvedand all conditions (defined by the flags) are met. A value of 0 means the problem is not solved, or solved with not all of the conditions being met. */
    "order": [
        {
             "tm": 0,              /* Arrival time in seconds. */
             "tmf": "<text>",      /* Formatted arrival time. Example: "hours:minutes". */
             "id": 0               /* Matrix point index, starting from 0. */
        },
        ...                     /* Results for other points. */
    ]
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

4                 Internal error.

Validation error (invalid matrix structure, different number
7                 of elements in the pointSchedules and pathMatrix
parameters, and so on).

## update_checkpoints

To update the list of the route checkpoints, use the update_checkpoints
method:

```http
svc=route/update_checkpointsparams={
    "itemId": <long>,
    "checkPoints": [
        {}
    ]
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| checkPoints | Array of checkpoints. |
| The checkpoint format varies depending on the checkpoint type, that is, on | whether it is a checkpoint from the map, a geofence or a unit. |

## Checkpoints from the map

The format of checkpoits from the map is as follows:

```json
{
    "f": 1,        // Point type.
    "n": <text>,   // Name.

    "y": <double>, // Latitude.
    "x": <double>, // Longitude.
    "r": <uint>         // Radius.
}
```

## Checkpoints from geofences

For checkpoints from geofences, two formats are possible:

format 1: with the indication of the gz field, containing the geofence
data;
format 2: with the indication of the resource ID and the geofence ID.

## Format 1

```json
{
    "f": 2,             // Point type.
    "n": <text>,        // Name.
    "gz": {            // Geofence information.
      "n": <text>,          // Geofence name.
      "d": <text>,          // Geofence description.
      "id": <long>,         // Geofence ID.
      "t": <byte>,          // Geofence type: 1 = line, 2 = polygon, 3 =circle.
      "w": <uint>,          // Line width or circle radius.
      "f": <uint>,          // Geofence flags.
      "c": <uint>,          // Color (ARGB).
      "b": {                // Bounding box parameters.
           "min_x": <double>, // Minimum longitude.
           "min_y": <double>, // Minimum latitude.
           "max_x": <double>, // Maximum longitude.
           "max_y": <double>, // Maximum latitude.
           "cen_x": <double>, // Center longitude.
           "cen_y": <double>       // Center latitude.
      },
      "p": [                // Array of geofence points.
           {
               "x": <double>, // Longitude.

                "y": <double>, // Latitude.
                "r": <uint>    // Radius.
            }
        ]
    }
}
```

## Format 2

```json
{
    "f": 2,                      // Point type.
    "n": <text>,                // Name.
    "resource": <long>,          // ID of the resource containing the geofence.
    "zone": <long>               // Geofence ID within the resource.
}
```

## Checkpoints from units

The format of checkpoits from units is as follows:

```json
{
    "f": 4,              // Point type.
    "u": <long>,         // Unit ID.
    "r": <uint>          // Radius.
}
```

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "rpts": [                      // Array of checkpoints.
        {
            "n": <text>,           // Name.
            "f": <uint>,           // Type.
            "u": <long>,           // Unit ID (0 if the type is not a checkpoint from a unit).
            "y": <double>,         // Latitude.
            "x": <double>,         // Longitude.
            "r": <uint>            // Radius.
        }
    ]
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
Code

Invalid input parameters, or failed to update the
4
checkpoints.

6                Internal error.

Internal error or missing
7                ADF_ACL_AVL_ROUTE_EDIT_SETTINGS access right to the
route.

## update_config

To update the route configuration, use the update_config method:

```http
svc=route/update_configparams={
    "itemId": <long>,
    "config": {
        "color": <uint>,
        "descr": <text>,
        "units": [<long>]
    }
}
```

You can create a route using the core/create_route method.

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| config | Configuration. |
| color | Color (ARGB). |
| descr | Description. |
| units | Array of unit IDs. |

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "rcfg": {               // Route configuration.
        "color": <uint>,    // Color (ARGB).
        "descr": <text>,    // Description.
        "units": [<long>]   // Array of unit IDs.
    }
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
Code

Invalid input parameters, or failed to update the
4
configuration.

6              Internal server error.

Internal error or missing
7              ADF_ACL_AVL_ROUTE_EDIT_SETTINGS access right to the
route.

## update_round

To create, edit or delete rides, use the route/update_round method:

```http
svc=route/update_roundparams={
    "itemId": <long>,
    "id": <long>,
    "callMode": <text>,

    "n": <text>,
    "d": <text>,
    "u": <long>,
    "at": <uint>,
    "vt": <uint>,
    "vp": <uint>,
    "sh": <long>,
    "cu": [<long>],
    "f": <uint>,
    "tz": <uint>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| id | Ride ID. |
| callMode | Action: create, update, delete. |
| sh | Schedule ID. Required if the action is create or update. |
| For the description of the other parameters, see get_round_data. |  |

### Response

If the request is completed successfully, the response format depends on
the action specified in the callMode parameter.

The response to the request for creating or updating a ride is returned in
the following format:

```json
[
    <long>,                          // Ride ID.
    {
        "id": <long>,                // Ride ID.
        "ct": <long>,                // Ride creation time (UNIX).
        "mt": <long>,                // Ride update time (UNIX).
        "n": <text>,                 // Name.
        "d": <text>,                 // Description.
        "sh": <text>,                // Schedule name.
        "f": <uint>,                 // Ride flags.
        "tz": <uint>,                // Timezone.
        "u": <long>,                 // Assigned unit. If not specified, this field shows the first unit from the "cu" array that departs fromthe first checkpoint.)
        "at": <uint>,                // Activation time.
        "vt": <uint>,                // Start of the validity period.
        "vp": <uint>,                // Validity period.
        "sts": <uint>,               // Ride state flags.

        "st": {                      // Ride state.
            "st": {                  // General ride state.
                 "pi": <uint>,       // Checkpoint index (4294967295 if notstarted).
                 "ps": <uint>,       // State flags and event flags.
                 "ut": <uint>        // Last event time.
            },
            "pts": {                 // State by checkpoint.
                 "<checkpoint_id>": {
                     "st": <uint>,   // Event flags.
                     "tm": <uint>    // Last event time.
                 }
                 // ... additional checkpoints
            }
        }

    }
]
```

Ride state and event flags are described on the get_round_data page.

The response to the request for deleting a ride is returned in the following
format:

```json
[
    <long>,   // Ride ID.null
]
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

One of the following errors:

invalid JSON parameters;
invalid callMode parameter;
4
missing required unit or units which can be assigned
to the ride;

invalid or missing schedule parameters.

6               Internal error.

7               Internal error.

## update_schedule

To create, edit or delete schedules, use the route/update_schedule
method:

svc=route/update_schedule
params={

```json
 "itemId": <long>,
 "id": <long>,
 "callMode": <text>,
 "n": <text>,
 "f": <uint>,
 "tz": <uint>,
 "u": <long>,
 "tm": [
      {
          "at": <uint>,
          "ad": <uint>,
          "dt": <uint>,
          "dd": <uint>
      }
 ],
 "sch": {
      "f1": <uint>,
      "f2": <uint>,
      "t1": <uint>,
      "t2": <uint>,
      "m": <uint>,
      "y": <uint>,
      "w": <uint>
 },
 "cfg": {
      "name": <text>,
      "units": [<long>],
      "enabled": <byte>,
      "roundFlags": <uint>,
      "autoName": <byte>,
      "validityPeriod": <uint>

    }
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemID | Route ID. |
| id | Schedule ID. |
| callMode | Action: create, update, delete. |
| The other parameters are required only for creating and editing. For their | description, see get_round_data. |
| The values of the f1, t1, f2, t2 parameters must be lower or equal to | 0xFFFF. |

### Response

If the request is completed successfully, the response format depends on
the action specified in the callMode parameter.

The response to the request for creating or updating a schedule is
returned in the following format:

```json
[
    <long>,    // Schedule ID
    {
        "id": <long>,           // Schedule ID.
        "n": <text>,            // Name.

       "f": <uint>,                // Schedule type (see below).
       "tz": <uint>,              // Timezone.
       "cfg": {                   // Custom configuration (example).
            "autoName": <byte>,        // Use an automatically generated na
```

me: 1 = yes, 0 = no.

```json
"enabled": <byte>,        // Create rides automatically: 1 = y
```

es, 0 = no.

```json
         "name": <text>,           // Ride name.
         "description":<text>,     // Description.
         "roundFlags": <uint>,      // Ride flags.
         "units": [<long>],        // Array of unit IDs.
         "validityPeriod": <uint> // Validity period.
    },
    "tm": [                    // Time of passing the checkpoints.
         {
             "at": <uint>,      // Arrival time.
             "ad": <uint>,      // Deviation from the arrival time.
             "dt": <uint>,      // Departure time
             "dd": <uint>       // Deviation from the departure time.
         }
    ],
    "sch": {                  // Time limitations.
         "f1": <uint>,         // Start of interval 1.
         "f2": <uint>,         // Start of interval 2.
         "t1": <uint>,         // End of interval 1.
         "t2": <uint>,         // End of interval 2.
         "m": <uint>,          // Day-of-month mask
         "y": <uint>,          // Month mask
         "w": <uint>           // Day-of-week mask
    }
}
```

]

## Schedule types

| Flag | Description |
| --- | --- |
| 0x1 | Relative to activation. |
| 0x2 | Relative to day. |
| 0x4 | Absolute. |
| The response to the request for deleting a schedule is returned in the | following format: |

```json
[
    <long>,   // Schedule ID.null
]
```

If the request fails, an error code is returned.

### Error codes

Error
Description
Code

Invalid input parameters (including invalid callMode,
4
missing required parameters, or invalid schedule times).

Failed to find the created schedule, or failed to update or
6
delete the schedule.

Internal error or missing
7              ADF_ACL_AVL_ROUTE_EDIT_SETTINGS access right to the
route.
