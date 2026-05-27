# report

This section describes the methods that can be applied to reports.

## abort_report

The abort_report function is used to abort the execution of an
asynchronous report.

```http
svc=report/abort_report&params={}
```

## Returned result

If the request is successful, an empty JSON is returned.

```json
{ }
```

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |

## apply_report_result

Is only used for the reports requested with the
“remoteExec” parameter.

The remoteExec function is used to receive the result of the execution of
an asynchronous report.

```http
svc=report/apply_report_result&params={}

      The result can be received only after a successful executionof an asynchronous report (“status”:4 in the returned

      result for the get_report_status request).
```

## Returned result

The returned result is the same as in the exec_report request.

Possible error codes:

| Code | Description |
| --- | --- |
| The limit of messages has been reached. See | 1004 the reason field for details. |
| 1003 | The limit has been reached. See the reason field for details. |
| 6 | Undefined error. |

## cleanup_result

There can be only one report result in a session. The
cleanup_result function is used to clear the results of the previous
execution if a session contains any.

```http
svc=report/cleanup_result&params={}
```

## Returned result

```json
{
         "error":<int>      /* error code (0 — if successful) */

}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |

## exec_report

The exec_report function is used to execute a report.

```http
svc=report/exec_report&params={
    "reportResourceId": <long>,
    "reportTemplateId": <long>,
    "reportObjectId": <long>,
    "reportObjectSecId": <long>,
    "reportObjectIdList": [
         <uint>,
         ...
    ],
    "interval": {
         "from": <uint>,
         "to": <uint>,
         "flags": <uint>
    },
    "remoteExec": <uint>,
    "reportTemplate": <object>
}

   There can only be one report in a session at the same time.
   Therefore, if there is already some report result in asession, you should clear it before executing another one.
   To do this, use the cleanup_result function.

   You can’t execute this request simultaneously with thefollowing requests:

        report/export_result;
        report/get_result_chart;
        report/get_result_map;
        messages/load_interval;
        render/create_messages_layer;
        unit/get_trips;
        resource/get_driver_bindings;
        resource/get_trailer_bindings,
        the requests from the exchange section;
        account/get_account_history.
```

### Parameters

| Name | Description |
| --- | --- |
| reportR      Resource ID. The parameter is required. The report is | esource      executed on behalf of the resource creator if Id           the reportTemplateId is 0. |
| eId | reportT emplat       Template ID. |
| reportO | Item ID. bjectId |
| cId | reportO Subitem ID (driver, trailer, or their groups); 0 if the item bjectSe has no subitems. |
| ist | reportO bjectIdL        The array of extra item IDs (for the report on unit groups). |
| interval | The settings of report interval. |
| from | The beginning of the interval, Unix time. |
| to | The end of the interval, Unix time. |
| flags | Interval flags. |
| Exec | Specify 1 for this parameter to execute the report on the Webreport server. The parameter is optional and is only used if the report/get_report_status request is executed later. If the JSON response includes "remoteExec":1, it remote means the server has accepted the report for processing, and the execution timeout is 5 minutes. Specify 0 or omit this parameter to execute the report on the Web server. In this case, the execution timeout is 2 minutes. |
| reportT         The JSON of the report template, which you can get after | emplat          the get_report_data request. The parameter is optional and e               only used if the reportTemplateId is 0. |
| Interval flags: |  |
| of the | The value The value Flag   Description                      of the "to"   Comments "from" parameter parameter |
| Timestamp        Timestamp | 0x0    specified value in         value in 0      interval seconds.         seconds. |
| the | Any value introduced in Timestamp 0x0    starts 'From'                                  parameter is value in         0 1      until today                                    replaced seconds. with the current server time. |
| The | The           Any value 0x0    for previous 0                number of     introduced in 2      n days days.         the from param The           eter is 0x0    for previous                                   replaced 0                number of 4      n weeks                                        with the last weeks. full period or the current 0x0    for previous                                   server time if 0                number of 8      n month                                        the 0x20 flag months. is present. |
| The | 0x1    for previous 0                number of 0      n years years. |
| 0x2    including | 0      current |
| The | 0x4       for previous 0                 number of 0         n hours hours. |
| The | 0x8       for previous 0                 number of 0         n minutes minutes. |

## Returned result

{

```json
"reportResult":{                             /* report executio
```

n result */

```json
"msgsRendered":<int>,                /* messages loade
```

d: 0 — no, 1 — yes */

```json
"stats":[                                                 /*
```

the array of statistics parameters */

```json
["<text>","<text>"]                           /*
```

[parameter name, value] */

```json
        ],
"tables":[                            /* the array of tables */
    {
               "name":"<text>",              /* table type */
               "label":"<text>",             /* name */
               "grouping": {
                    "type":"<text>"         /* grouping type */
               },
               "flags":<uint>,               /* table flags (se
```

e below) */

```json
"rows":<uint>,                /* the number of l
```

ines */

```json
"level":<uint>,               /* the maximum lev
```

el in the table */

```json
"columns":<uint>,             /* columns count
```

*/

```json
"header":["<text>"],                   /* the arr
```

ay of table headers */

```json
"total":[                        /* total */
     "<text>"                              /* the arr
```

ay of cells */

```
],
"header_type" ["<text>"],            /* the array of t
```

able header types */
"totalRaw" [                     /* the array of val
ues of the line "Total" */

```json
{
"v":<double>,              /* origina
```

l cell value */

```json
"vt":<double>,             /* value t
```

ype */

```json
                   },
                        ...
              ]
          }
],

          "attachments":[                                /* the arr
```

ay of attachments (charts, photos) */

```json
{                                    /* for charts */
"name":"<text>",            /* name */
"type":"<text>",            /* type: chart, photo */
"datasets":["<text>"] /* the array with the names
```

of the chart's curved lines */

```json
"axis_y": ["<text>"]         /* the array with the labe
```

ls of 'Y' axes */

```json
"axis_x": "<text>",        /* the nam
```

e of the 'X' axis */

```json
"flags": <uint>,             /* axis format, see the de
```

scription below */

```json
     "p":"<text>",                /* chart settings */
},
              {                                                  /*
```

for photo and video */

```json
"name":"<text>",           /* name an
```

d following parameters separated by ";" */

```json
                                    "ftm":"<text>", /* formatted date

*/
                                     "uid":"<text>", /* unit ID */
                                     "tm":"<text>",   /* Unix time */
                                     "idx":"<text>", /* the index of the same-type attachments registered simultaneously */
                                     "lat":"<text>", /* latitude */
                                     "lon":"<text>", /* longitude */
                                     "type":"<text>",          /* attachment type */
                                     "zone":<JSON>,   /* geofence information */
                                     "tags":<JSON>,   /* information about tags */
                             }
                  ]
           },
           "reportLayer":{                     /* graphic layer */
                  "name":"<text>",                             /* layer name */
                  "bounds":[
                             <double>,                         /* minimumlatitude */
                             <double>,                         /* minimumlongitude */
                             <double>,                         /* maximumlatitude */
                             <double>                          /* maximumlongitude */
                  ]
           },
           "layerCount":<uint>       /* the number of layers to be merged in the report layer */
}
```

To get all available table types, use the get_report_tables function.

For the zone field details, see the get_zone_data page.

For the tags field details, see the update_tag page.

Table flags:

| Flag | Description |
| --- | --- |
| 0x1 | Grouping by days. |
| 0x2 | Time limitation. |
| 0x4 | Grouping by weeks. |
| 0x8 | Grouping by months. |
| 0x10 | Total. |
| 0x20 | Charts: split sensors. |
| 0x100 | Detalization: partial. |
| 0x200 | Charts: count from zero. |
| 0x400 | Accumulate intervals. |
| 0x800 | Detalization: full. |
| 0x1000 | Row numbering. |
| 0x2000 | Execute table only by report item (not subitems). |
| 0x4000 | Group records into shifts. |
| 0x8000 | Cut intervals in the table. |
| 0x200000 | Grouping by trips. |
| 0x400000 | Grouping by violation type. |
| 0x10000000 | Grouping by the day of the week. |
| 0x20000000 | Grouping by day of the month. |
| 0x40000000 | Grouping by years. |
| Chart flags: |  |
| flag | Additional Flag                           Description |
| 0x4 | Correct maximum for the Y axis. |
| The format specified in the template | 0x10 settings. |
| Additional for 0x10 (Set format to | 0x1 "H:M:S"). |
| Additional for 0x10 (Set format to "Y-m- | 0x2 E"). |
| 0x80 | Generic type. |
| 0x10 | 24-hour format. 0 |
| 0x20 | 24-hour format (additional for 0x100). |
| 0x2 | 12-hour format (additional for 0x20). |
| Display days of the week (additional for | 0x40 0x100). |
| Possible error codes: |  |
| Code | Description |
| Failed to fetch the report object and report resource with the | 7         desired ACL (ADF_ACL_ITEM_EXECUTE_REPORTS, ADF_ACL_AVL_RES_VIEW_REPORTS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## export_result

The export_result function is used to export report results to a file.

```http
svc=report/export_result&params={"format":<uint>,

"pageOrientation":"<text>",

"hideGoogleLinks":<uint>,

"pageSize":"<text>",

"pageWidth":"<text>",

"coding":"<text>",

"delimiter":"<text>",

"headings":"<text>",

"compress":"<text>",
```

"attachMap":"<text>",

"extendBounds":<bool>,

"hideMapBasis":"<text>",

"outputFileName":"<text>",

"splitChart":"<text>",

"appendTreeAnchorRows":"<text>"}

You can't execute this request simultaneously with the
following requests:

report/exec_report;
report/get_result_chart;

report/get_result_map;
messages/load_interval;

render/create_messages_layer;
unit/get_trips;

resource/get_driver_bindings;
resource/get_trailer_bindings;

the requests from the exchange section;
account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| format | File format (see below). |
| Optional parameters: |  |
| value | Default Name                  Description |
| Report file compression: |  |
| compress                 0 — no;                           1 | 1 — yes. |
| portrait | pageOrientatio        Page orientation (PDF): portrait, n                     landscape. |
| pageSize | Page format (PDF): a4, a3.           a4 |
| Page width (PDF): |  |
| 0 — fixed; | pageWidth                                                  0 1 — compact; 2 — no-wrap. |
| coding | Encoding (CSV): utf8, cp1251.        utf8 |
| delimiter | Delimiter (CSV): semicolon, colon.   colon |
| Displaying headers: |  |
| headings                 0 — no;                           0 | 1 — yes. |
| Attaching the map (PDF and HTML | only): |
| attachMap | 0 — no;                        0 |
| 1 — yes. |  |
| Extend the map to include | geofences: |
| extendBounds | 0 — no;                        0 |
| 1 — yes. |  |
| Hiding the map layer: |  |
| hideMapBasis        0 — no;                        0 | 1 — yes. |
| rt | Online_repo outputFileName   File name. |
| s | Hide google links in coordinate cells (PDF and XLSX): hideGoogleLink 0 — no;                        0 1 — yes. |
| splitChart | Splitting by day or week.         <empty> |
| horRows | Append tree anchor rows with an empty row: appendTreeAnc 0 — no;                        0 1 — yes. |
| According to the new logics for the “extendedBounds” parameter, by | default the map is zoomed to fit the tracks, markers, and icons. When the option is enabled, the map is also zoomed to fit the geofences. If there are no graphic elements (neither tracks, markers, icons for the default situation, nor geofences for the activated extended bounds option), the map isn’t displayed at all. |
| File formats: |  |
| 1 — HTML; | 2 — PDF; 4 — XLS; 8 — XLSX; 16 — XML; 32 — CSV. |

## Returned result

Returns a file of demanded format.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Failed to fetch the user. |
| 5 | Report file reading/writing error. |
| 4 | Wrong input parameters. |

## get_report_data

The get_report_data function is used to get the data of a report template.

```http
svc=report/get_report_data&params={"itemId":<long>,

"col":[<long>],

"flags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| col | The array of template IDs. |
| flags | Response flags. |
| Response flags: |  |
| Description | HEX         DEC flag        flag |
| 0x0 | 0            Full JSON (default). |
| 0x1 | 1            Basic information and assigned units/groups. |
| Basic information and short tables | 0x2         2 information. |
| 0x4 | 4            Basic information and full tables information. |

## Returned result

[

```json
{
          "id":<long>,                 /* template ID */
          "n":"<text>",                       /* name */
          "ct":"<text>",               /* type (see below) */
          "c":"<text>",                       /* data CRC16 */
          "p":"<text>",                       /* parameters */
          "tbl":[                             /* tables */
                    {
                             "n":"<text>",             /* table t
```

ype */

```json
"l":"<text>",             /* name */
"c":"<text>",             /* the lis
```

t of columns */

```json
"cl":"<text>",   /* the list of col
```

umn labels */

```json
"cp":"<text>",   /* the list of col
```

umns parameters */

```json
"s":"<text>",             /* the lis
```

t of columns (if it is a statistics table) */

```json
"sl":"<text>",   /* the list of col
```

umn labels (if it is a statistics table) */

```json
"filter_order":"<text>",               /*
```

filters order */

```json
"p":"<text>",             /* table p
```

arameters */

```json
"sch":{                   /* time li
```

mitation */

```json
"f1":<uint>,    /* the beg
```

inning of interval 1 */

```json
"f2":<uint>,    /* the beg
```

inning of interval 2 */

```json
"t1":<uint>,    /* the end
```

of interval 1 */

```json
"t2":<uint>,    /* the end
```

of interval 2 */

```json
"m":<uint>,                  /*
```

days of month mask */

```json
"y":<uint>,               /*
```

months mask */

```json
"w":<uint>                /*
```

days of week mask */

```json
"fl":<uint>               /*
```

incomplete interval (0 — don't cut off, 1 — show and cut off, 2 —
don't show in the report, 3 — show and mark as incomplete) */

```json
},
"f":<uint>                          /*
```

table flags */

```
            }
        ]
}
```

]

Template types:

avl_unit;

avl_unit_group;
storage_user;

avl_driver;
avl_trailer;

avl_resource;
avl_retranslator;

avl_route;
avl_drivers_group;

avl_trailers_group;
avl_tag;

avl_tags_group;
avl_geozone;

avl_geozones_group;

Table flags are described on the exec_report page.

To get the types of tables which can be included in reports, use the
get_report_tables function.

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the report object and the report resource with | 7 the desired ACL (ADF_ACL_AVL_RES_VIEW_REPORTS). |
| 4 | Wrong input parameters. |

## get_report_status

The get_report_status function with no parameters should be used after
executing the exec_report request with the parameter “remoteExec”:1.

```http
svc=report/get_report_status&params={}
```

## Returned result

```json
{"status":{code}}
```

Status code                         Description

1                                   In a queue.

2                                   Proceeding.

4                                   Done.

8                                   Cancelled.

Invalid report or
16
no such report.

After a successful result (“status”:“4” in the response), execute the
report/apply_report_result request with no parameters:

```http
svc=report/apply_report_result&params={}
```

The returned result with the information from the report is the same as
after the exec_report request.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Undefined error. |

## get_report_tables

The get_report_tables function is used to get the list of tables that can be
included in the reports.

svc=report/get_report_tables&params={}

## Returned result

[

```json
{
      "id":<uint>,                 /* table ID */
      "n":"<text>",                       /* system table na
```

me */

```json
"l":"<text>",                       /* default table n
```

ame */

```json
"t":"<text>",                       /* table type */
"ct":"<text>",               /* type of the template in
```

which this table can be used */

```json
"pt":"<text>",               /* text parameters */
"gt":"<text>",               /* advanced grouping setti
```

ngs */

```json
"col":[                             /* the array of co
```

lumns */

```json
{
         "n":"<text>",              /* system
```

column name */

```json
"l":"<text>",              /* default
```

column name */

```json
"sl":"<text>",   /* the list of col
```

umn headers (if it is a statistics table) */

```json
"t":"<text>",              /* column
```

type */

```json
"f":<uint>                 /* column
```

flags (see below) */

```
                }
      ]
}
```

]

The types of report templates are described on the get_report_data page.

Column flags:

| Flag | Description |
| --- | --- |
| 0x01 | Show as table column. |
| 0x02 | Show as statistics column. |
| 0x04 | Show as global switcher. |
| 0x08 | Show as column with position data. |
| 0x10 | Show as chart axis. |
| The values of the “pt” parameter: |  |
| Value | Description |
| geozones | Geofences/Units. |
| val | unfinished_i Unfinished interval. |
| duration | Duration. |
| mileage | Mileage. |
| sor | base_eh_sen Engine hours sensor. |
| s | engine_hour Engine hours. |
| speed | Speed. |
| trips | Trips. |
| stops | Stops. |
| parkings | Parkings. |
| sensors | Sensors. |
| e | sensor_nam Sensor mask. |
| driver | Driver. |
| trailer | Trailer. |
| fillings | Fillings. |
| thefts | Fuel drains. |
| mat | duration_for Duration format. |
| x | geozones_e Extended geofences/units. |
| username | Username mask. |
| route_points | Route points. |
| event_mask | Event mask. |
| rides | Rides, applicable for the Unit and Rides tables. |
| fields_config | Field type, applicable for the Custom fields tables. |
| units | Units, applicable for the Manoeuvres table. |
| interval | Tracing interval in minutes, applicable for the Unit → Sensor tracing table. |
| group_zones | The Consider group as a whole option is available. Applicable for the Unit group → Non-visited _pass geofences table. |
| routes | Applicable for the Route type tables. |
| last_location | The Consider report interval option is available. Applicable for the Unit latest data table. |
| hide_total | The Total checkbox is hidden for that table. |
| groupitem | The Group itself option is available. Applicable for the Unit group → Log and Custom fields tables. |
| noschedule | No Time limitation option available. Applicable for the Summary and Latest unit data tables. |
| hide_driver_    The Retrieve intervals checkbox is hidden in the | split           driver filter. |
| e | account_tre Account tree. |
| s_mask | custom_field Custom fields mask. |
| drv_activity | Driver activity. |
| movement_ | Movement chronology. chronology |
| sensor_val | Sensor value. |
| sor | timeout_sen Sensor timeout. |
| sor_name | custom_sen Custom sensor name. |
| ations | filter_notific Keep only messages with a notification text. |
| Possible error codes: |  |
| Code | Description |
| 6 | Undefined error. |

## get_result_chart

The get_result_chart function is used to get a chart.

```http
svc=report/get_result_chart&params={"attachmentIndex":<uint>,
                                                                        "action":<uint>,
                                                                        "width":<uint>,
                                                                        "height":<uint>,

                                                                    "a
```

utoScaleY":<uint>,
"p
ixelFrom":<int>,
"p
ixelTo":<int>,
"f
lags":<uint>}

You can't execute this request simultaneously with the
following requests:

report/exec_report;
report/export_result;
report/get_result_map;
messages/load_interval;

render/create_messages_layer;
unit/get_trips;
resource/get_driver_bindings;
resource/get_trailer_bindings;
the requests from the exchange section;
account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| attachmentIndex | Attachment index. |
| action | Actions: |
| 0 — set flags and render; | 1 — zooming; |
| 2 — automatic scale of the Y axis. |  |
| width | Width. |
| height | Height. |
| Automatic scale of the Y axis: |  |
| autoScaleY                    0 — disable; | 1 — enable. |
| pixelFrom | Zoom: from the current pixel. |
| pixelTo | Zoom: to the current pixel. |
| flags | Chart flags. |
| Chart flags: |  |
| Flag | Description |
| 0x01 | Place the header above the chart. |
| 0x02 | Place the header under the chart. |
| 0x04 | Don't show the header. |
| 0x40 | Set the X-axis captions direction from up to down. |
| 0x80 | Set the X-axis captions direction from down to up. |
| 0x100 | Place the chart legend above the chart. |
| 0x200 | Place the chart legend under the chart. |
| 0x400 | Place the chart legend to the left of the chart. |
| 0x800 | Place the chart legend to the right of the chart. |
| 0x1000 | Always show the legend, even in case of one dataset. |

## Returned result

The returned result contains a PNG image.

## get_result_map

The get_result_map function is used to get the map with tracks and
markers.

```http
svc=report/get_result_map&params={"width":<uint>,

"height":<uint>}

    You can't execute this request simultaneously with thefollowing requests:

        report/exec_report;
        report/export_result;

        report/get_result_chart;
        messages/load_interval;

        render/create_messages_layer;

        unit/get_trips;
        resource/get_driver_bindings;

        resource/get_trailer_bindings;
        the requests from the exchange section;
        account/get_account_history.
```

### Parameters

| Name | Description |
| --- | --- |
| width | Width. |
| height | Height. |

## Returned result

The returned result is the PNG image of the map with tracks and markers
rendered on it.

## get_result_photo

The get_result_photo function is used to get a photo from a report.

```http
svc=report/get_result_photo&params={"attachmentIndex":<uint>, // or [<uint>] to get many zipped images at once
                                                                     "border":<uint>,

"type":<ubyte>}
```

### Parameters

| Name | Description |
| --- | --- |
| dex | attachmentIn Attachment index. |
| Maximum photo size (0 — original size). | border           For Wialon Hosting and Wialon Local 2204 the maximum value is 1920. |
| Image type: |  |
| type | 0 — original image (default value); 1 — image with a description frame (timestamp + address). |
| The parameter is only used in Wialon Hosting and | Wialon Local 2204. |

## Returned result

The returned result for Wialon Local versions up to 1804 is a PNG image.
For versions 1904-2104 the returned result is a JPEG image.

For Wialon Hosting and Wialon Local 2204, the returned result is a JPEG
image if there is one value in the attachmentIndex parameter. If there is
more than one value, the returned result is a ZIP archive with images.

## get_result_rows

The get_result_rows function is used to get a specified quantity of rows
from a report table.

```http
svc=report/get_result_rows&params={"tableIndex":<uint>,
```

"indexFrom":<uint>,

"indexTo":<uint>}

The request returns the rows as an array, regardless of
their nesting level.

### Parameters

| Name | Description |
| --- | --- |
| tableIndex | The index of the report table. |
| indexFrom | The index of the first requested row. |
| indexTo | The index of the last requested row. |

## Returned result

[

```json
{
      "n":<uint>,       /* row index (from 0) */
      "i1":<uint>,      /* the number of the first message
```

in the specified interval */

```json
"i2":<uint>,      /* the number of the last message
```

in the specified interval */

```json
"t1":<uint>,      /* the time of the first message i
```

n the specified interval */

```json
"t2":<uint>,      /* the time of the last message in
```

the specified interval */

```json
              "d":<int>,        /* the quantity of rows with the n

ext nesting level */
                 "c":[             /* cells array */
                         {                  /* common cell type */
                                   "t":"<text>",            /* cell value */
                                   "y":<double>,    /* latitude */
                                   "x":<double>,    /* longitude */
                                   "v":<double> /* only for the date/time stamp cell values */
                         },
                         {         /* cell type: video or image */
                                   "t":"<text>", /* cell value text
*/
                                   "j":<JSON>, /* cell value in a JSO
N format */
                                   "v":<double>, /* cell value */
                                   "vt":<int> /* cell value type */
                         },
                         ...
                 ]
         }
]
```

The value types are described here.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Failed to fetch the user. |
| 5 | Failed to fetch the report result. |
| 4 | Wrong input parameters. |

## get_result_subrows

The get_result_subrows function is used to get nested rows of the next
level from a report table.

svc=report/get_result_subrows&params={"tableIndex":<uint>,

"rowIndex":<uint>}

The request allows receiving subrows up to the second
level only. If you need to get more nested rows, use the
report/select_result_rows request.

### Parameters

| Name | Description |
| --- | --- |
| tableIndex | Table index. |
| rowIndex | Row index. |

## Returned result

[

```json
{
      "n":<uint>,      /* row index (from 0) */
      "i1":<uint>,     /* the number of the first message
```

in the specified interval */

```json
"i2":<uint>,     /* the number of the last message
```

in the specified interval */

```json
                 "t1":<uint>,     /* the time of the first message in the specified interval */
                 "t2":<uint>,     /* the time of the last message inthe specified interval */
                 "d":<int>,       /* the quantity of rows with the next nesting level */
                 "c":[            /* cells array */
                          {       /* common cell type */
                                  "t":"<text>",    /* cell value */
                                  "y":<double>,    /* latitude */
                                  "x":<double>,    /* longitude */
                                  "v":<double>     /* only for the date/time stamp cell values */
                          },
                          {       /* cell type: video or image */
                                  "t":"<text>", /* cell value text
*/
                                  "j":<JSON>, /* cell value in JSONformat */
                                  "v":<double>, /* cell value */
                                  "vt":<int> /* cell value type */
                          },
                 ]
        }
]
```

If the specified row doesn’t contain any nested rows, the returned result is:

```json
{
        "error":0
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Failed to fetch the user. |
| 5 | Failed to fetch the report result. |
| 4 | Wrong input parameters. |

## get_result_video

The get_result_video function is used to get a video from a report.

```http
svc=report/get_result_video&params={"attachmentIndex":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| attachmentIndex | Attachment index. |

## Returned result

```json
{
        "video_uri": "<text>",     /* link to the video */
        "video_type": "<text>"     /* type of the video */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the unit with the desired ACL | 7 (ADF_ACL_ITEM_EXECUTE_REPORTS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## hittest_chart

The hittest_chart function is used to get information about a certain point
of a chart.

```http
svc=report/hittest_chart&params={"attachmentIndex":<uint>,

"datasetIndex":<uint>,

"valueX":<int>,

"valueY":<int>,

"flags":<int>
```

### Parameters

| Name | Description |
| --- | --- |
| attachmentIndex | Chart index. |
| datasetIndex | Dataset index (-1 — all datasets). |
| valueX | X-coordinate, pixels. |
| valueY | Y-coordinate, pixels. |
| flags | Flags. |
| Flags: |  |
| HEX flag | Description |
| 0x1 | Get help to the chart. |
| 0x2 | Get help to the marker. |
| 0x4 | Use the valueX as time. |

## Returned result

```json
{
        "x":<double>,                /* X-axis value */
        "textX":"<text>",                    /* text value for the X-coordinate */
        "axisX":"<text>",                    /* X-axis name */
        "y":[
              {
                  "y":<int>,         /* Y-coordinate */
                  "textY":"<text>",          /* coordinate is string */
                  "axisY":"<text>",          /* Y-axis */
                  "name":"<text>",           /* chart name */

                  "color":<uint>     /* colour */
            },
            ...
        ]
        "msg":{                      /* message */...
        }
}
```

The message formats are described on the messages page.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Failed to fetch the user. |
| 5 | Report file reading/writing error. |
| 4 | Wrong input parameters. |

## render_json

The render_json function is used to get a chart’s JSON.

```http
svc=report/render_json&params={"attachmentIndex":<uint>,
                                                       "width":<uint>,
                                                       "useCrop":<uint
>,

                                                       "cropBegin":<ui
```

nt>,

```json
"cropEnd":<uint
```

>}

### Parameters

| Name | Description |
| --- | --- |
| ndex | attachmentI Attachment index. |
| width | According to this parameter, the optimum number of pixels for the chart is returned. |
| Сrop the time interval: |  |
| useCrop               1 — yes; | 0 — no. |
| cropBegin | The beginning of the interval, Unix time. |
| cropEnd | The end of the interval, Unix time. |

## Returned result

The following fields are only available in Wialon Hosting
and Wialon Local 2204: units, mmi, interruptions,
possitions.

{

```json
"datasets":{                        /* data */
     "<text>":{                     /* chart index */
           "name":"<text>",         /* chart name */
           "color":<uint>,          /* line colour */
           "y_axis":<uint>,         /* use the second Y-axis (for the
```

charts with two curves and different measurements): 0 — no, 1 — ye
s */

```json
"units": "<text>",         /* chart units of
```

measurement by the Y-axis; null if the chart values have no units
of measurement */

```json
           "data": {
                "x": [
                      <uint>,       /* chart trace (time) */...
                ],
                "y": [              /* chart trace (value) */
                      <int>,
                      ...
                ]
           },
           "colors": [              /* chart colour intervals */

                [<uint>,            /* interval start time */
                    <uint>],        /* colour */...
           ],
     },
     ...
},
     "mmi":[<uint>], /* the array of values by the X-axis from
```

the raw dataset, the interval between which is longer than the ind
icated time (dt) > "Maximum interval between messages" */

```json
"interruptions":[<uint>], /* the array of values by the X-
```

axis from the filtered dataset, the interval between which is long
er than the indicated time (dt) > "Maximum interval between messag
es" */

```json
    "markers":[                         /* markers */
         {

                "type":<uint>,         /* type */
                "x": [
                    <uint>,            /* time */...
                ]
          },
          ...
     ],
     "background_regions": [         /* background intervals */
          {
                "name":"<text>",       /* name */
                "color":<uint>,        /* colour */
                "priority":<uint>,     /* priority */
                "regions":[
                    [<uint>,           /* the beginning of the interval
*/
                     <uint>            /* the end of the interval */
                     ],
                    ...
                ]
          },
          ...
     ],
          "possitions":{      /* the values of the coordinates of the returned points of all the lines in the chart */
                    "time":[<uint>],
                    "lat":[<double>],
                    "lon":[<double>]
          }
}
```

Marker flags:

HEX flag                   DEC flag               Description

0x4                        4                      Event/Violation.

0x8                   8                      Fuel filling.

0x10                  16                     Image.

0x20                  32                     Parking.

0x40                  64                     Speeding.

0x80                  128                    Stop.

0x100                 256                    Fuel drain.

0x800                 2048                   Video.

0x1000                4096                   Violation.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Failed to fetch user. |
| 5 | Report file reading/writing error. |
| 4 | Wrong input parameters. |

## select_result_rows

The select_result_rows function is used to get rows in multilevel reports.

svc = report/select_result_rows&params={

```json
      "tableIndex": <int>,
      "config": {
          "type": "<text>",
          "data": {}
      }
}
```

### Parameters

| Name | Description |
| --- | --- |
| tableIndex | Table index. |
| config | Configuration. |
| The request type: |  |
| type                      range — ordered sequence of rows; | row — row. |
| data | The data for the configuration. |
| If the type parameter is range, the data parameter has the following | format: |

```json
"data":{
          "from":<uint>,
          "to":<uint>,
          "level":<uint>,
          "flat":<uint>,
          "rawValues":<uint>,

          "unitInfo":<uint>
}
```

Option         Description

from           The index of the first row.

to             The index of the last row.

level          Nesting level.

Show the nesting level on the same level with the parent
row:

flat              0 — no;
1 — yes.

The parameter is optional. The default value is 0.

Show the parameters v, vt:

rawValue          0 — no;
s                 1 — yes.

The parameter is optional. The default value is 0.

Show uid:

0 — no;
unitInfo
1 — yes.

The parameter is optional. The default value is 0.

If the type parameter is row, the data parameter has the following format:

"data": {

```json
"rows": [<int>],
"level": <uint>,
"flat": <int>,
"rawValues": <uint>,
"unitInfo": <uint>,
"from": <int>,
"to": <int>
```

}

Option         Description

The index of the row. You can indicate the index of a
rows
nested row to up to next-to-last nesting level.

level          Nesting level.

Show the nesting level on the same level with the parent
row:

flat              0 — no;

1 — yes.

The parameter is optional. The default value is 0.

from           The index of the first nested row (optional).

to             The index of the last nested row (optional).

Show the raw values data:

rawValu           0 — no;
es                1 — yes.

The parameter is optional. The default value is 0.

Show uid:

0 — no;
unitInfo
1 — yes.

The parameter is optional. The default value is 0.

## Returned result

[

```json
{
      "n": <uint>,               /* row index (from 0) */
      "i1": <uint>,              /* the number of the first message i
```

n the specified interval */

```json
"i2": <uint>,              /* the number of the last message in
```

the specified interval */

```json
"t1": <uint>,              /* the time of the first message in
```

the specified interval */

```json
"t2": <uint>,              /* the time of the last message in t
```

he specified interval */

```json
"d": <int>,                /* the quantity of the rows with the
```

next nesting level */

```json
"uid": <long>,             /* unit ID; only if unitInfo is set
```

to 1 */

```json
"c": [                     /* the array of cells */
    {                     /* common cell type */
          "t": "<text>",          /* formatted cell value */
          "v": <double>,        /* original cell value */
          "vt": <double>,       /* value type */
          "pi": {               /* property items */
               "t": "<text>",      /* property items type */
               "ids": [           /* the array of property item I
```

Ds */

```json
                        ]
                   },
                   "y": <double>,        /* latitude */
                   "x": <double>,        /* longitude */

                   "c": "<text>"         /* cell colour (only if cell hasa colour) in "RRGGBB" format */
             },
             {                     /* cell type: video or image */
                   "t": "<text>",       /* cell value text */
                   "j": <JSON>,         /* cell value in JSON format */
                   "v": <double>,       /* cell value */
                   "vt": <int>          /* cell value type */
             }
        ],
        "r": [                      /* holds the subrows which correspond to the requested nesting level */
             {                     /* the set of fields of the row willbe the same as that of the parent row */
                   "n": <uint>,
                   "i1": <uint>,
                   "i2": <uint>,
                   ...
             }
        ]
    }
]
```

The value types are described here.

Possible error codes:

| Code | Description |
| --- | --- |
| 7 | Failed to fetch the report library. |
| 6 | Failed to fetch the user. |
| 5 | Report file reading/writing error. |
| 4 | Wrong input parameters. |

## update_report

The update_report function is used to create, edit, and delete report
templates.

```http
svc=report/update_report&params={
    "itemId":<long>,
    "id":<long>,
    "callMode":"<text>",
    "n":"<text>",
    "ct":"<text>",
    "p":"<text>",
    "tbl":[
        {
            "n":"<text>",
            "l":"<text>",
            "c":"<text>",
            "cl":"<text>",
            "cp":"<text>",
            "s":"<text>",
            "sl":"<text>",
            "filter_order":"<text>",
            "p":"<text>",
            "sch":{"f1":<uint>,"f2":<uint>,"t1":<uint>,"t2":<uint>,"m":<uint>,"y":<uint>,"w":<uint>,"fl":<uint>},
            "f":<uint>
        }
    ]
}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| Name | Description |
| id | Template ID. |
| callMode | Action: create, update, delete. |
| Other parameters are only required to create and edit templates. They are | described on the get_report_data page. |
| The p parameter specifies the grouping of the table and other settings. | Example: |

```json
"p":"{
       \"grouping\":\"
          {\"type\":\"total\",\"nested\":     /* enable grouping \"Total\" */
              {\"type\":\"year\"}}\"          /* enable nested grouping \"Year\" */
}"
```

Basic grouping types:

Type                      Description

total                     Total.

year                      Year.

month                     Month.

week                      Week.

wday                      Day of the week.

Type                         Description

mday                         Day of the month.

day                          Date.

shift                        Shift.

To see the advanced grouping types, get the table information using the
get_report_tables request (the gt parameter).

For the account_tree table, the following parameters can be used:

```json
"p": "{
       \"account_tree\": {
           \"group\": <bool>,
           \"types\": \"<text>\"
       }
}"
```

| Name | Description |
| --- | --- |
| Grouping the elements: |  |
| group | 0 — no; 1 — yes. |
| The default value is 0. |  |
| types | Element types included in the table results: |
| avl_account; | avl_resource; |
| user; |  |
| avl_unit; | avl_unit_group; |
| avl_retranslator; | avl_route. |
| By default, all element types are included. |  |
| Example (all double quotes within the value must be escaped): |  |

```json
     "p":"{\"account_tree\":{\"group\":1,\"types\":\"avl_account,avl_resource,user,avl_unit,avl_unit_group,avl_retranslator,avl_route
\"}}"
```

For the driver_ddd table, the drv_activity (Driver activity source)
parameter can be used:

```json
"p": "{
          \"drv_activity\":"<text>"
          }"
```

Value                  Description

ddd                    Use data from the .ddd files (by default).

online                 Use the data from online activities.

binds_and_trips        Use the data from assignment and trip activities.

For the driver_orders table (Orders), order_filter (Filtration) parameter
can be used:

"p":"{
\"order_filter\":<uint>
}"

Value          Description

0x1            Visited orders. Deprecated.

0x2            Not visited orders. Deprecated.

0x4            Orders visited in time. Deprecated.

0x8            Orders visited late. Deprecated.

0x10           Confirmed and rejected orders.

0x20           Not confirmed and not rejected orders.

0x40           Confirmed orders.

0x80           Rejected orders.

0x100          Visited orders.

0x200          Not visited orders.

0x400          Orders visited in time.

0x800          Orders visited late.

For the unit_counter_sensors (Counter sensors), the
following parameters can be used:

sensor_val:min (minimum sensor value);
sensor_val:max (maximum sensor value).

```json
"p": "{
           \"sensor_val\":{\"min\":\"10\",\"max\":\"14\"}
}"
```

For charts:

```json
"p":"{
           \"sensor_mask\":"<text>",                 /* sensor mask */
           \"instant_speed_base\":{
                  \"mask\":"<text>"}}         /* sensor mask to colour the chart line by sensor */
```

To split shifts in the tables with shifts, use the following parameters:

```json
"p":{\"split_shifts\":1},
"s":{\"split_shifts\"}
```

## Charts

A chart is a table in a template.

To add markers to the chart, add marker table to the template and marker
flags to the chart table. Marker table code sample:

```json
{"n":"unit_events",
 "l":"",
 "f":0,

    "c":"",
    "cl":"",
    "p":"",
    "sch":{
     "y":0,
     "m":0,
     "w":0,
     "f1":0,
     "f2":0,
     "t1":0,
     "t2":0},
    "sl":"",
    "s":"[\"chart_unit_events\"]"},
```

Сode sample for marker flags:

```json
"p":"{
    \"chart_markers\":{
         \"f\":2556}
    }"
}
```

Available markers/states:

Marker                          Flag          Description

unit_events                     0x4           Events.

unit_fillings                   0x8           Fuel fillings.

unit_photos                     0x10          Images.

unit_stays                      0x20          Parkings.

unit_speedings                  0x40            Speedings.

unit_stops                      0x80            Stops.

unit_thefts                     0x100           Fuel drains.

unit_videos                     0x800           Video.

To change charts’ background according to the state of the units, add
marker/state to the template and chart_regions parameter to the chart
table.

ID                                             Description

chart_stops_regions                            Stops.

chart_engine_hours_regions                     Engine hours.

chart_conn_quality_regions                     Connection loss.

chart_stays_regions                            Parkings.

chart_trips_regions                            Trips.

chart_speedings_regions                        Speedings.

chart_digital_sensors_regions                  Digital sensors.

## Advanced settings

Every template setting is a table column. To activate an option, add the
corresponding column to the template.

The following settings are available:

Table          Column                Description

unit_stats     multi_drivers         Multiple drivers/trailers.

Mileage/Fuel/Counters with a
precise_calculat
unit_stats                           precision of up to two decimal
ions
places.

Exclude fuel drains from fuel
unit_stats     exclude_thefts
consumption.

unit_stats     trips_mileage         Mileage from trips only.

Consider track-geofence
unit_stats     intersect_zone
intersections.

unit_stats     address_format        Address format.

unit_stats     time_format           Time format.

unit_stats     us_units              Measurement system.

unit_stats     shifts                Shifts.

unit_trips     render_msgs           All messages on map.

unit_trips     render_trips          Trip routes.

render_geozone
geozones                             Render geofences.
s

unit_video     render_unit_vid
Video markers.
s              eos

unit_filling   render_filling_m
Filling markers.
s              arkers

unit_phot     render_unit_pho
Image markers.
os            tos

render_stops_m
unit_stops                         Stop markers.
arkers

unit_spee     render_speedin
Speeding markers.
dings         gs_markers

unit_theft    render_theft_ma
Fuel drain markers.
s             rkers

unit_event    render_events_
Event markers.
s             markers

render_stays_m
unit_stays                         Parking markers.
arkers

unit_locati   render_location
Unit last location.
on            _markers

unit_stats
all_resources        Geofences from all resources.
_zones

unit_stats                         Add geofence description to
desc_address
_zones                             address.

unit_stats
address_zones        Use geofences for addresses.
_zones

Address format, time format, shift, and measurement
system are specified in the **“p”**parameter.

## Returned result

For creation and modification requests:

```json
[
        <long>,             /* template ID */
        {
                  "id":<long>,       /* template ID */
                  "n":"<text>",      /* name */
                  "ct":"<text>",     /* template type */
                  "c":<uint>         /* check sum (crc16) */
        }
]
```

Template types are described on the get_report_data page.

For deletion requests:

```json
[
        <long>,             /* template ID */null
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the item with the desired ACL | 7 (ADF_ACL_AVL_RES_EDIT_REPORTS). |
| 6 | Undefined error. |
| 4 | Wrong input parameters. |

## value_types

If rawValues in the select_result_rows request is activated, each cell
contains the parameters v (the original cell value) and vt (type).

Available types:

Type       Value

0          Unspecified text value.

1          Address value.

2          Unspecified custom <int> value.

3          Unspecified custom <double> value.

4          Counter value.

5          Custom type: text+value.

10         Distance, kilometers.

20         Speed, km/h.

30         Time value (YYYY/MM/DD HH:MM:SS).

31         Time value (HH:MM:SS).

32         Time value (YYYY/MM/DD).

40   Time interval value, seconds.

41   Time interval value, hours.

42   Time interval value, ratio hours.

50   Volume, litres.

51   Consumption, l/100 km.

52   Consumption, l/h.

53   Consumption, l/ha.

54   Fuel level, litres.

55   Consumption, km per 1 litre.

60   Percentage value.

61   Percentage value with daily reset.

70   Area in hectares.

72   Area in square meters.

73   Zones area in ha or square ft.

74   Zones perimeter in m or ft.

80   Information measurement, bytes, kbytes, mbytes.

90   Weight, tones.

91   Weight, kg.

100        Temperature, in Celsius.

110        Eco driving penalties.

111        Eco driving rank.

112        Eco driving rating.

113        User column.

120        Empty column.

130        Video column value, count; text — JSON.

140        Image column value, count; text — JSON.

## reqformat

All actions are executed using POST requests. Additional parameters
(params) should be given in the form of JSON. The response is also returned
as JSON. All text parameters, either sent or returned ones, are supposed to
use UTF-8 encoding.

```http
http://json.org doesn’t support HEX values, use DEC.
```

Request template:

```http
http://<host>/wialon/ajax.html?sid=<text>&svc=<svc>&params=<params
>

      You must specify Content-Type:application/x-www-form-urlencoded in the request header.
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| sid* | Session ID. |
| svc* | Command. |
| params* | Parameters for the command execution. |
| The following sections describe the values of only two | parameters. These parameters are svc and params. The session ID (sid) is a required parameter for executing all requests (except for …/core/login and some requests described here). |

### Limitations

See the list of limitations here.
