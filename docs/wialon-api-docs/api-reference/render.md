# render

In this section, you can find the methods for working with different graphic
layers and receiving information from them.

## calculate_polygon

The calculate_polygon function is used to get a polygon area or/and
perimeter.

```http
svc=render/calculate_polygon&params={"p":[
                                                 {
                                                      "x":<double>,
                                                      "y":<double>
                                                 },
                                                 ...
                                            ],
                                            "flags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| p | The array of polygon points. |
| x | Longitude. |
| y | Latitude. |
| Displaying the flags: |  |
| flags | 0x1 — show area; 0x2 — show perimeter; 0x3 — show both parameters. |

## Returned result

```json
{
    "area":<double>,         /* area */
    "perimeter":<double>     /* perimeter */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 4 | Wrong input parameters. |

## calculate_polyline

The calculate_polyline function is used to get a polyline area and/or
perimeter.

```http
svc=render/calculate_polyline&params={"p":[
                                                    {
                                                          "x":<double>,
                                                          "y":<double>
                                                    },
                                                    ...
                                               ],
                                               "flags":<uint>,
                                               "w":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| p | The array of coordinate points. |
| x | Longitude. |
| y | Latitude. |
| Displaying the flags: |  |
| flags | 0x1 — show area; 0x2 — show perimeter; 0x3 — show both parameters. |
| w | Line width, meters. |

## Returned result

```json
{
       "area":<double>,        /* area */
       "perimeter":<double>    /* perimeter */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 4 | Wrong input parameters. |

## create_messages_layer

The create_messages_layer function is used to create a graphic layer
using the coordinates from messages.

svc=render/create_messages_layer&params={"layerName":"<text>",

"itemId":<long>,

"timeFrom":<uint>,

"timeTo":<uint>,

"tripDetector":<bool>,

"trackColor":"<text>",

"trackWidth":<int>,

"arrows":<bool>,

"points":<bool>,

"pointColor":"<text>",

"annotations":<bool>,

"flags":<uint>}

You can't execute this request simultaneously with the
following requests:

report/exec_report;
report/export_result;

report/get_result_chart;

report/get_result_map;
messages/load_interval;

resource/get_driver_bindings;
resource/get_trailer_bindings;
the requests from the exchange section;
account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| me | layerNa Layer name. |
| itemId | The ID of the unit, the messages of which should be requested. |
| m | timeFro The beginning of the interval. |
| timeTo | The end of the interval. |
| The trip detection usage: |  |
| ctor | tripDete         0 — no; 1 — yes. |
| lor | The colour of the track in the ARGB format (A is the alpha trackCo channel or the transparency level) or "trip" for colouring tracks by trips ("tripDetector":1 is required). |
| dth | trackWi Track width in pixels. |
| The arrows of movement direction: |  |
| arrows | 0 — no; |
| 1 — yes. |  |
| Points at the places where messages were received: |  |
| points        0 — no; | 1 — yes. |
| lor | pointCo The colour of the points. |
| The annotations for the points: |  |
| ions | annotat       0 — no; 1 — yes. |
| flags | The flags for displaying markers (optional parameter). |
| The trackColor parameter examples: |  |
| Colour | Name                                   ARGB code |
| Opaque red. | "FFFF0000" |
| Semi-transparent green. | "7F00FF00" |
| Strongly-transparent blue. | "500000FF" |
| Marker flags: |  |
| Flag | Value |
| 0x0001 | Grouping markers. |
| 0x0002 | Numbering for markers. |
| 0x0004 | Event markers. |
| 0x0008 | Fuel filling markers. |
| 0x0010 | Image markers. |
| 0x0020 | Parking markers. |
| 0x0040 | Speeding markers. |
| 0x0080 | Stop markers. |
| 0x0100 | Fuel drain markers. |
| 0x0800 | Video markers. |

## Returned result

```json
{
        "name":"<text>",          /* layer name */
        "bounds":[                /* layer bounds */
               <double>,          /* minimum latitude */
               <double>,          /* minimum longitude */
               <double>,          /* maximum latitude */
               <double>           /* maximum longitude */
        ],
        "units":[                 /* array of units */

                {
                        "id":<long>,                        /* unit ID
```

*/

```json
"msgs":{                                        /*
```

information about messages */

```json
"count":<uint>,             /* message
```

s count */

```json
"first":{                               /*
```

first message */

```json
"time":<uint>,   /* time */
"lat":<double>, /* latitud
```

e */

```json
"lon":<double>   /* longitu
```

de */

```json
},
"last":{                                /*
```

last message */

```json
"time":<uint>,   /* time */
"lat":<double>, /* latitud
```

e */

```json
"lon":<double>   /* longitu
```

de */

```json
        }
},
"mileage":<double>,                 /* mileage
```

for interval (meters) */

```json
"max_speed":<unit>                  /* maximum
```

speed for interval */

```json
                }
     ],
     "trips":[          /* only if tripDetector is 1 */
                {
                        "first":{ /* first message */
                                "time":<uint>, /* time */
                                "lat":<double>, /* latitude */
                                "lon":<double> /* longitude */
                        },
                        "last":{ /* last message */
                                "time":<uint>, /* time */
                                "lat":<double>, /* latitude */

                                    "lon":<double> /* longitude */
                            },
                            "mileage":<double>, /* mileage for interval (meters) */
                            "max_speed":<unit> /* maximum speed for interval */
                            "color":"<text>" /* interval colour in '#R
RGGBB' format */
                   }
        ]
}
```

See also avl_render.

Possible error codes:

| Code | Description |
| --- | --- |
| 1004 | The limit of messages has been reached. |
| 1003 | The limit of layers has been reached. |
| 1001 | No messages to process. |
| Failed to fetch the resource with the desired ACL | 7 (ADF_ACL_ITEM_EXECUTE_REPORTS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## create_zones_layer

The create_zones_layer function is used to create a graphic layer with
geofences.

```http
svc=render/create_zones_layer&params={"layerName":"<text>",

"flags":<uint>,

"zones":[

{

"resourceId":<long>,

"zoneId":[<long>]

}

]}
```

### Parameters

| Name | Description |
| --- | --- |
| layerName | Layer name. |
| Flags: |  |
| flags                   0x1 — show the names of geofences; | 0x2 — group geofences. |
| zones | The array of geofences. |
| resourceId | Resource ID. |
| zoneId | Geofence ID. |

## Returned result

```json
{
        "name":"<text>",              /* layer name */
        "bounds":[
                 <double>,            /* minimum latitude */
                 <double>,            /* minimum longitude */
                 <double>,            /* maximum latitude */
                 <double>             /* maximum longitude */
        ]
}
```

See also avl_render.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## delete_message

The delete_message function is used to delete messages.

```http
svc=render/delete_message&params={"layerName":"<text>",

"msgIndex":<uint>,

"unitId":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| layerName | Layer name. |
| msgIndex | Message index. |
| unitId | Unit ID. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired ACL | 7 (ADF_ACL_AVL_UNIT_DEL_MSGS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## enable_layer

The enable_layer function is used to make a graphic layer active or
inactive.

```http
svc=render/enable_layer&params={"layerName":"<text>",
                                                                      "enable":<bool>}
```

### Parameters

| Name | Description |
| --- | --- |
| layerName | Layer name. |
| Make the layer active: |  |
| enable | 0 — no; |
| 1 — yes. |  |

## Returned result

```json
{
        "enabled":<int> /* state: 0—           inactive; 1 — active */
}
```

See also avl_render.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## get_messages

The get_messages function is used to get messages from a layer.

```http
svc=render/get_messages&params={"layerName":"<text>",
                                                                             "indexFrom":<uint>,
                                                                             "indexTo":<uint>,
                                                                             "unitId":<long>
                                                                             "calcSensors": <text>}
```

### Parameters

| Name | Description |
| --- | --- |
| layerName | Layer name. |
| indexFrom | The index of the first requested message. |
| indexTo | The index of the last requested message. |
| unitId | Unit ID. |
| calcSensors | Sensor values. If set to a non-empty value (“1”, “yes”, “true”, or any other text), sensor values will be calculated and included in the response. If empty or omitted, sensor values are not calculated. |

## Returned result

```json
[                           /* array of messages */
         {
                 ...
         }
]
```

The message formats are described here.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## remove_all_layers

The remove_all_layers function is used to delete all graphic layers.

```http
svc=render/remove_all_layers&params={}
```

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |

## remove_layer

The remove_layer function is used to delete layers.

```http
svc=render/remove_layer&params={"layerName":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| layerName | Layer name. |

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## render_json

Can only be used in Wialon Hosting and Wialon Local 2204.

The render_json function is used to get a chart’s JSON.

```http
svc=report/render_json&params={"uintId":<long>,
                                                               "width":<uint>,
                                                               "useCrop":<uint>,
                                                               "cropBegin":<uint>,
                                                               "cropEnd":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| uintId | Unit ID. |
| width | Chart window width. According to this parameter, the optimum number of pixels for the chart is returned. |
| Сrop the time interval: |  |
| useCrop           1 — yes; | 0 — no. |
| in | cropBeg The beginning of the interval, Unix time. |
| cropEnd | The end of the interval, Unix time. |

## Returned result

```json
{
          "data":{
                    "PARAM_NAME_1": {
                             "x": [<double>,...],
                             "y": [<double>,...],
                    },
                    "PARAM_NAME_2": { ... }
          },
          "possitions": {
                    "time": [<double>,...],
                    "lat": [<double>,...],
                    "lon": [<double>,...],
          }
}
```

Instead of the PARAM_NAME there should be the name of a message
parameter.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## set_locale

The set_locale function is used to set the time zone, language, date
format, or tile density for the layers.

```http
svc=render/set_locale&params={"tzOffset":<uint>,
                                                   "language":"<text>",
                                                   "flags":<uint>,
                                                   "formatDate":"<text>",
                                                   "density":<uint
>}
```

### Parameters

| Name | Description |
| --- | --- |
| tzOffset | Time zone. |
| language | Language (two-lettered code). |
| Measurement system flags (optional): |  |
| flags | 0 — metric; 1 — U.S.; 2 — imperial. |
| formatDate | Date and time format (see below). |
| density | Tile size (optional). |
| Date and time format: |  |
| Parameter | Description |
| The hour of the day with a leading 0 if necessary (from | %H "00" to "23"). |
| %B | The full month name (from "January" to "December"). |
| %b | The abbreviated month name (from "Jan" to "Dec"). |
| The month of the year with a leading 0 if necessary | %m (from "01" to "12"). |
| %l | The month of the year (from "1" to "12"). |
| The format of the Persian calendar ("01 Farvardin 1392 | %P 00:00:00"). |
| The day of the week full name (from "Monday" to | %A "Sunday"). |
| %a | The abbreviated day name (from "Mon" to "Sun"). |
| The day of the month with a leading 0 if necessary | %E (from "01" to "31"). |
| %e | The day of the month (from "1" to "31"). |
| The hour of the day with a leading 0 if necessary (from | %I "01" to "12") |
| The minute of the hour with a leading 0 if necessary | %M (from "00" or "59") |
| The seconds of the minute with a leading 0 if necessary | %S ("00" to "59"). |
| %p | The A.M./P.M. designator ("AM" or "PM"). |
| %Y | The full four digit year ("1999" or "2008"). |
| %y | The year as a two-digit number ("99" or "08"). |
| Example: |  |

```json
"formatDate":"%Y-%m-%E %H:%M:%S"
```

Result:

#### 2013-01-26 12:34:56

Density:

Value                  Tile size                       Ratio

1                      256*256                         1

2                      378*378                         1.5

3                      512*512                         2

4                      768*768                         3

5                      1024*1024                       4

The default tile size is 256*256.

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

If not, an error code is returned. Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |
