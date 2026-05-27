# order

In this section, you can find all the methods used for working with orders.

## optimize

In order to use optimization when planning the route and distributing
orders, use order/optimize:

```http
svc=order/optimize&params={"itemId":<long>,
                            "orders":[<uint>,{JSOn},...],
                            "warehouses":[<uint>],
                            "units":[<uint>],
                            "flags":<uint>,
                            "gis":{
                                 "provider":<uint>,
                                 "addPoints":<uint>,
                                 "speed":<uint>,
                                 "mode":"<text>",
                                 "avoid":"<text>",
                                 "departure_time":<uint>,
                                 "traffic_model":"<text>",
                                 "transit_mode":"<text>",
                                 "transit_routing_preference":"<text
>"
                            },
                            "busyRoutes":{
                                 "<uint>":[
                                        {
                                              "tf":<uint>,
                                              "tt":<uint>,
                                              "pf":{<uint> || {JSON}},
                                              "pt":{<uint> || {JSON}
                                        },
                                        ...
                                 ]
                            },
                            "addPoints":<bool>,
                            "priority":{<uint>:{<uint>:<uint
>},...},
                            "criterions":{"<text>":<uint>,...},
                            "preference":{<uint>:<uint>,...}

}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Resource ID. |
| Optimized order array (order indexes/order | orders* JSON delimited with a comma). |
| warehouses | Warehouse array. |
| flags* | Optimization flags. |
| gis | GIS settings. |
| busyRoutes | Busy period. |
| tf | Busy period start time. |
| tt | Busy period end time. |
| pf | Busy period start location: order ID or JSON. |
| pt | Busy period end location: order ID or JSON. |
| provider | Map source: 0 - none, 1 - Gurtam Maps (default), 2 - Google. |
| mode | Mode of transportation: driving, walking, bicycling, or transit (only for Google). |
| avoid | Route restrictions: tolls, highways, ferries and/or indoor (only for Google). |
| departure_time | Planned time of departure (only for Google). |
| traffic_model | Assumptions: best guess, pessimistic, or optimistic (only for Google). |
| transit_mode | Preferred modes: bus, subway, train, tram and/or rail (only for Google). |
| transit_routing_pre   Preferences for transit requests (only for | ference               Google). |
| addPoints | Return a track in the response: 1 - yes, 0 - no. |
| speed | Speed which should be used for optimization, km/h (60 by default). |
| units | Unit array. |
| priority | Sequence of orders: {unit index:{order index:expected index of order in a route}} The index equal to -1 makes the order be the last in the route. |
| Route completion criteria: |  |
| max_mileage. The maximum mileage, m. | max_duration. The maximum duration, s. criterions               max_order_count. The maximum number of orders. |
| max_idling. The maximum idle time between | orders, s. |
| preference | Order priority in the route. |
| The JSON format is the same as in the update request. |  |
| You can find further information about the Google | settings here. |

### Flags

| Flag | Description |
| --- | --- |
| Optimize by order schedule. The order tf and tt parameters | 0x1 are used. |
| 0x2 | Optimize by completion duration of all orders. |
| 0x2 | Optimize by carrying capacity (weight). 0 |
| 0x4 | Optimize by effective capacity (volume). 0 |
| 0x8       Optimize only orders with tt > current time. If tf < current | 0         time, then tf = current time. |
| If the criteria are exceeded: |  |
| 0x100 | The route is terminated. |
| 0x200 | An intermediate warehouse is visited. |
| 0x300 | The route is divided into several routes. |

### Response

{

```json
"1":{                                                   /* optim
```

ization for the first unit */

```json
"orders":[
                  {
                            "ml":<uint>,    /* mileage
```

*/

```json
"tm":<uint>,    /* time to
```

visit the order area */

```json
"id":<uint>     /* order i
```

ndex in the array sent in the request (starts from 0)      */

```json
},
{
          "ml":<uint>,    /* mileage
```

*/

```json
"tm":<uint>,    /* time to
```

visit the order area */

```json
"id":<uint>     /* order i
```

ndex in the array sent in the request (starts from 0)      */

```json
                          }
        ]
},
"2":{                                                   /* optim
```

ization for the second unit (if the number of units is greater tha
n one) */

```json
"orders":[
                  {
                            "ml":<uint>,    /* mileage
```

*/

```json
"tm":<uint>,    /* time to
```

visit order area */

```json
"id":<uint>      /* order i
```

ndex in the array sent in the request (starts from 0)        */

```json
},
{
         "ml":<uint>,     /* mileage
```

*/

```json
"tm":<uint>,     /* time to
```

visit the order area */

```json
"id":<uint>      /* order i
```

ndex in the array sent in the request (starts from 0)        */

```
                            }
         ]
},
...,                                                      /* optim
```

ization for other units (if the number of units is greater than tw
o) */

```json
"success":<bool>                                      /* optimiz
```

ation status:
1 - success (there is a
solution which meets all the requirements),
0 - failed */
}

If only warehouse orders have been assigned to the unit
(the 0x4 flag), it will not appear in the response.

If the route is divided into several routes, there will be a
route array in the response.

### Error codes

Error
Description
code

7              Invalid itemId.

6              Internal error.

Logic error. See the reason in the response for more
4
information.

## attach

To attach a file to an order, use order/attach:

```http
svc=order/attach&params={"itemId":<long>,
                           "id":<long>,
                           "eventHash":"<text>"}
           &sid="<text>"
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Order ID within the resource. |
| eventHash | Event name. It will be generated after processing the data. |
| To attach a file to an order, send a POST request. See the example below. |  |
| attach | Request URL:https://hst-api.wialon.com/wialon/ajax.html?svc=order/ Request Method:POST Content-Type:multipart/form-data; boundary=----WebKitFormBoundarya 38SwBwyXw5BFPQ1 |
| ------WebKitFormBoundarya38SwBwyXw5BFPQ1 | Content-Disposition: form-data; name="params" |

```json
{"itemId":39801,"id":3,"eventHash":"jUploadForm1435580226231"}
------WebKitFormBoundarya38SwBwyXw5BFPQ1
Content-Disposition: form-data; name="eventHash"

jUploadForm1435580226231
------WebKitFormBoundarya38SwBwyXw5BFPQ1
Content-Disposition: form-data; name="file_upload"; filename="attachment.txt"
Content-Type: application/octet-stream

------WebKitFormBoundarya38SwBwyXw5BFPQ1--
```

### Response

```json
{
         "error":0
}
```

### Error codes

Error code       Description

7                Couldn't get the item with the provided itemId.

5                An error occurred while writing the file.

4                No file was provided or one of the files was empty.

## complete_from_history

If the orders were not completed online, you may use
the order/complete_from_history method to complete the orders using
history messages:

order/complete_from_history&params={"itemId":<long>,

```json
"orders":[long]}
```

### Parameters

| Parameter | Description |
| --- | --- |
| itemId | Resource ID. |
| orders | Array of order IDs. |
| Make sure the unit is assigned to the order. |  |
| Use: |  |
| ./update with callMode=‘‘create’’ to create an order with the unit | assigned; ./update with callMode=‘‘assign’’ to assign a unit to the order that has already been created. |

### Response

{

```json
"completed":<bool>         /* checked the aggregated status of
```

the orders:
1 - completed (if at least one orde
r is completed during the request processing, the status of this o
rder will be changed to "s":2),
0 - not completed (no order has bee
n completed during request processing) */
}

### Error codes

Error
Description
code

7              Couldn't get the item with the provided itemId.

6              Failed to create the order collection.

No order was provided or one of the orders was
4
erroneous.

## detach

To detach a file from an order, send the order/detach method:

```http
svc=order/detach&params={"itemId":<long>,
                            "id":<long>,
                            "path":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Order ID within the resource. |
| path | File name. |
| To get the list of files attached to the order, use | order/list_attachments. |

### Response

```json
{ }
```

### Error codes

Error code         Description

7                  Couldn't get the item with the provided itemId.

5                  An error occurred while deleting the file.

## get_attachment

To get an attached file, use order/get_attachment:

```http
svc=order/get_attachment&params={"itemId":<long>,
                                     "id":<long>,
                                     "path":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Order ID within the resource. |
| path | File name. |

### Response

In case of success, the server will return the requested file.

If failed,

#### Invalid input{"error":3}

## get_orders_history

To get the history of orders, use the order/get_orders_history method.

```http
svc=order/get_orders_history&params={
                                                   "itemId":<long>,
                                                   "ivalType":<int>,
                                                   "ivalFrom":<uint>,
                                                   "ivalTo":<uint>,
                                                   "name":"<text>",
                                                   "unitId":<long>,
                                                   "orderId":<long>,
                                                   "orderUid":<long>,
                                                   "routeId":<long>
                                      }
```

### Parameters

The required parameters are marked with an asterisk (*).

Default

| Parameter | Description |
| --- | --- |
| value |  |
| itemId* | Resource ID. |
| ivalType       1 | Requested interval type, the same as in messages. Possible values are 1,2,3,4. |
| ivalFrom | 0             Interval start time. |
| ivalTo | UINT_MAX    Interval end time. |
| Order name masks. For example, | name                         "name": "Vil*,Berl*" will search for orders which start with 'Vil' and 'Berl'. |
| unitId | Unit ID. |
| orderId | Order ID (can be repeated in history). |
| orderUid | Unique order ID. |
| routeId | Route ID. |

### Response

{

```json
"orders":[
       {...}.
       {...},
       ...
],
"count":<uint>,       /* number of the filtered orders
```

(size of "orders") */

```json
"total":<uint>        /* total number of orders for the
```

requested period */
}

### Error codes

Error code                   Description

7                              Invalid resource ID.

6                              Internal error.

## get_route_from_history

To get a route from history, use order/get_route_from_history.

### Request

```http
svc=order/get_route_from_history&params={
                                                     "itemId":<long>,
                                                     "routeId":<long>,
                                                     "timeFrom":<uint>,
                                                     "timeTo":<uint>,
                                                     "addPoints":<uint>
                                       }
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Resource ID. |
| routeId* | Route ID. |
| timeFrom* | Start time. |
| timeTo* | End time. |
| addPoints | Add route points to the response. The default is 1. |

### Response

```json
{
        "routes":[
                {...},
                {...},
                ...
        ],
        "count":<uint>,
        "total":<uint>
}
```

### Error codes

Error code                  Description

7                           Incorrect resource ID.

6                           Internal error.

## get_routes_history

To get the history of routes, use order/get_routes_history.

### Request

```http
svc=order/get_routes_history&params={
                                                   "itemId":<long>,
                                                   "ivalType":<int>,
                                                   "ivalFrom":<uint>,
                                                   "ivalTo":<uint>,
                                                   "name":"<text>",
                                                   "unitId":<long>,
                                                   "routeId":<long>
                                      }
```

### Parameters

The required parameters are marked with an asterisk (*).

Default

| Parameter | Description |
| --- | --- |
| value |  |
| itemId* | Resource ID. |
| ivalType       1 | Requested interval type, the same as in messages. Possible values are 1,2,3,4. |
| ivalFrom | 0             Interval start time. |
| ivalTo | UINT_MAX      Interval end time. |
| Route name masks. For example: | name                         "name": "Vil*,Berl*" will search for routes which start with 'Vil' and 'Berl'. |
| unitId | Unit ID. |
| routeId | Route ID. |

### Response

```json
{
         "routes":[
                  {...}.
                  {...},
                  ...
         ],
         "count":<uint>,            /* number of the filtered routes
(size of "routes") */
         "total":<uint>             /* total number of routes for therequested period */
}
```

### Error codes

Error code                      Description

7                               Invalid resource ID.

6                               Internal error.

## list_attachments

To see all the files attached to the order, use:

```http
svc=order/list_attachments&params={"itemId":<long>,
                                         "id":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID. |
| id | Order ID within the resource. |

### Response

[

```json
{
      "n":"<text>",        /* file name */
      "s":<uint>, /* size, bytes */
      "ct":<uint>,         /* creation time */
      "mt":<uint> /* last modification time */
},
...
```

]

### Error codes

Error code                     Description

7                              Invalid resource ID.

5                              No orders found.

## list_virtual_order_routes

To get the list of virtual routes, use order/list_virtual_order_routes.

### Request

```http
svc=order/list_virtual_order_routes&params={
                                                   "itemId":<long>
                                       }
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Resource ID |

### Response

```json
{
         {...},
         {...},
         ...
}
```

### Error codes

Error code                   Description

7                              Incorrect resource ID.

## route_update

To create, edit or delete a route, use the order/route_update method.

```http
svc=order/route_update&params={ "itemId":<long>,
                                   "orders":\[\],
                                   "routeId":<long>,
                                   "callMode":"<text>"}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Resource ID. |
| orders* | Array of JSON orders and a "callmode" for each order. |
| routeId* | Route ID. |
| callMode* | Action: create, edit, delete. |
| The result is similar to the batch of order/update. |  |

### Response

{

```json
"orders":[{
        "id":<uint>,                /* order ID */
        "f":<uint>,                 /* order flags */
        "u":<uint>,                 /* unit ID */
        "uid":<uint>,               /* order UID */
        "callMode":"<text>"
},
...
]
```

}

### Error codes

Error code        Description

7                 Invalid resource ID.

4                 Logic error. See the reason in the response.

## update

The basic method to work with orders is order/update.

## How to start

Create an order with callMode:“create” (if no unit is assigned to the
order, the response with the order details will return s:0);

Assign a unit to the order using callMode:"assign" (the response with
the order details will return s:1);
Manually move an order to history using callMode:“register”.

## Creating or updating an order

{

```json
"svc": "order/update",
"params": {
  "itemId": <long>,      /* resource ID */
  "id": <long>,          /* order ID (0 in the case of creation)
```

*/

```json
"n": "<text>",         /* order name */
"oldOrderId": <long>, /* old order ID */
"oldOrderFiles": ["<text>"], /* array of old order files */
"p": {                 /* order parameters */
  "n": "<text>",       /* client name */
  "p": "<text>",       /* phone */
  "p2": "<text>",      /* second phone */
  "e": "<text>",       /* email */
  "a": "<text>",       /* address */
  "v": "<text>",       /* volume */
  "w": "<text>",       /* weight, kg */
  "c": <uint>,         /* cost */
  "ut": <uint>,        /* service time, s */
  "t": "<text>",       /* vehicle type */
  "d": "<text>",       /* description */
  "uic": "<text>",     /* number of the shipping document */
  "cid": "<text>",     /* custom ID */
  "cm": "<text>",      /* comment upon confirming/rejecting orde
```

r */

```json
"aff": "<text>",     /* [warehouse] list of warehouse unit IDs
```

("123,456") */

```json
"z": "<text>",       /* [warehouse] list of warehouse geofence
```

s ("resId_geofenceId,...") */

```json
"ntf": <uint>,       /* notification flags: 1 - SMS to first p
```

hone; 0x2 - SMS to second phone; 0x10 - email */

```json
"pr": <uint>,        /* order priority */
"tags": [<uint>],    /* order tags */

     "r": {                /* route information */
         "id": "<uint>",   /* route ID */
         "i": "<uint>",    /* number [0..] */
         "m": "<uint>",    /* mileage from previous point as planne
```

d, m */

```json
"t": "<uint>",    /* time from previous point as planned, s
```

*/

```json
"ndt": <uint>,    /* time before estimated delivery to noti
```

fy customer, s */

```json
         "vt": "<uint>"    /* visit time as planned, UNIX_TIME */
     }
},
"rp": "<text>",            /* order route */
"f": <uint>,               /* order flags */
"tf": <uint>,              /* lower bound of order completion time,
```

UNIX-time */

```json
"tt": <uint>,              /* upper bound of order completion time,
```

UNIX-time */

```json
"trt": <uint>,             /* acceptable schedule advancement time,
```

s */

```json
"r": <uint>,               /* order point radius, m */
"y": <double>,             /* order point latitude */
"x": <double>,             /* order point longitude */
"u": <long>,               /* unit ID */
"ej": {},                  /* extended JSON (optional) */
"tz": <int>,               /* user time stamp */
"callMode": "<text>", /* "create" or "delete" to create or del
```

ete, respectively */

```json
    "dp": ["<uint>", ..] /* array of dependent order IDs */
}
```

}

## Deleting an order

{

```json
"svc": "order/update",
"params": {

    "itemId": <long>,      /* resource ID */
    "id": <long>,          /* order ID (0 in the case of creation) */
    "force": <uint>,       /* enable force deletion of problem routes
```

(optional) */

```json
    "callMode": "delete"
}
```

}

## Moving an order to the history manually

svc=order/update&params={"itemId":<long>,               /* resource ID */

```json
"id":<long>,                                 /*
```

order ID (0 in the case of creation) */

```json
"callMode":"register"}
```

## Assigning a unit to the order

svc=order/update&params={"itemId":<long>,               /* resource ID */

```json
"id":<long>,                                 /*
```

order ID (0 in the case of creation) */

```json
"u":<long>,                                  /*
```

unit ID */

```json
"callMode":"assign"}
```

## Rejecting an order

svc=order/update&params={"itemId":<long>,               /* resource ID */

```json
"id":<long>,                                 /*
```

order ID (0 in the case of creation) */

```json
"callMode":"reject"}
```

## Confirming an order

```http
svc=order/update&params={"itemId":<long>,           /* resource ID */
                            "id":<long>,                                 /*order ID (0 in the case of creation) */
                            "callMode":"confirm"}
```

### Flags

The flags should be passed in the f field in JSON. They are as follows:

Value     Description

The order will be marked as completed if there is at least one
0x1
message within the order area with zero speed in it.

The order will be completed after the unit leaves the order
0x2
area.

0x4       First warehouse.

0x8       Last warehouse.

0x10      Intermediate (reload) warehouse.

0x20      Permanent order.

0x40      The orders can’t be confirmed outside the specified radius.

Value      Description

Do not change the order status after the route is completed
0x80
automatically.

If the route has been completed automatically, but the order
0x100      has not been executed, a new one is created on the basis of
the order copy.

The flags 0x8, 0x10 are taken into account during
optimization only if the orders are in the array of
warehouses.

### Response

callMode=‘‘create’’:

```json
[<​uint>,​
         {
         "​id":​
              <u​int>​
                     ,                              /* order ID */
         "​n":"<text>",                                /* order name */
         "​p":​
             {                                                  /​
                                                                 * order parameters */
               "n":"<text>",                        /* client name */
               "p":"<text>",                        /* phone */
               "p2":"<text>",                       /* second phone */
               "e":"<text>",                        /* email */
               "a":"<text>",                        /* address */
               "v":<uint>,                   /* volume */
               "w":<uint>,                   /* weight, kg */
               "c":<uint>,                   /* cost */
               "ut":<uint>,                         /* service time,​s
*/

           "t":"<text>",                             /* vehicle type */
           "d":"<text>",                             /* description */
           "uic":"<text>",                           /* number of the s
```

hipping document */

```json
"cid":"<text>",                           /* custom ID */
"cm":"<text>",                            /* comment which i
```

s left upon confirming or rejecting the order */

```json
"aff":"<text>",                           /* [ warehouse ] l
```

ist of the warehouse unit IDs ("123,456") */

```json
"z":"<text>",                             /* [ warehouse ] l
```

ist of the warehouse geofences ("resId_geofenceId,...") */

```json
"ntf":<uint>,                             /* notification fl
```

ags */

```json
"pr":<uint>,                              /* order priority
```

*/

```json
"r": {                                      /* route informa
```

tion */

```json
"id":"<text>",                       /* route ID */
"i":"<text>",                        /* number [0..] */
"m":"<text>",                        /* mileage from th
```

e previous point according to the plan, m */

```json
"t":"<text>",                        /* time from the p
```

revious point according to the plan, s */

```json
"ndt":<uint>,               /* time within which the c
```

ustomer should be notified before the estimated delivery time, s
*/

```json
"vt":"<text>"                        /* visit time acco
```

rding to the plan, UNIX_TIME */

```json
    },
"​rp":"<text>",                                 /​
                                                * order route, g
```

oogle polyline encoding format */
"​
f":<​
uint>,​                              /​
* order flags */

```json
"tf":<​uint>,                                   /​
                                                * lower bound of
```

order completion time, UNIX-time */
"​
tt":<​
uint>,​                             /​
* upper bound of order
completion time, UNIX-time */
"​
trt":<​
uint>,​                            /​
* acceptable time of a
dvancing the schedule, s */
"​
uid":<​
uint>,​                            /​
* ​
unique I
​D (is used a
s the unique key in the order history)         */

"​
r":<​
uint>,​                          /​
* order point radius,
m */
"​
y":<​
double>,​                        /​
* order point latitude
*/
"​
x":<​
double>,​                        /​
* order point longitud
e */
"​
u":<​
long>,​                          /​
* unit ID */
"​
s":<​
uint>,​                          /​
* order status:​0 - in
active (no unit assigned),​1 - active,​2 - completed on time, 3 -
completed late, 4      rejected, 5 - the unit is in the order area */
"​
sf":<​
uint>,​                         /​
* order status flag (0
x100 - rejected,​0x200 - confirmed, 0x400 - received a notificatio
n about the order) */
"​
st":<​
uint>,                         /​
* last status modificat
ion time */

```json
"tz":<uint>,                           /* user time stamp         */
"eta":<uint>,                              /* ETA calculated
```

every 180 seconds by routing (or considering the route as a straig
ht line) if there is the next order and an activated notification
about ETA/mileage(RD) */

```json
"rd":<​double>,                       /* mileage */
"cnm":<​uint>,                        /* mileage counter from t
```

he unit properties */

```json
"nt":<uint>,                               /* next_time, stan
```

ds for the time when the orders received the status 'next' */

```json
"ds":<uint>,                               /* completion stat
```

us, an integer is passed in the 'confirm' parameter, for example,
% */

```json
"dp":<uint>,                               /* list of order U
```

IDs on which the current order depends: the current order can't be
completed until the listed orders are completed first */

```json
"stt":<uint>,                              /* start_transfer_
```

time, stands for the arrival time */

```json
"dtt":<uint>,                              /* done_transfer_t
```

ime,   stands for the exit time */

```json
"if":<uint>                                /* internal_flags,
```

see the description below */

```
}
```

]

callMode=‘‘update’’:

```json
[
       <uint>             /* updated order ID */
]
```

callMode=‘‘delete’’:

```json
[
       <uint>,            /* deleted order ID */null
]
```

callMode=‘‘assign’’,‘‘register’’,‘‘reject’’:

```json
{ }    /* success */
```

## or

```json
{
       "error":4          /* if failed to assign */
}
```

## Internal flags

The internal flags should be passed in the if field in JSON. They are as
follows:

Value   Description

0x1     The order is being delivered.

The driver has been notified about a deviation from the
0x2
route.

The driver has been notified that the order hasn’t been
0x4
confirmed.

The client has been notified about the estimated time of
0x10
arrival.

The client has been notified what distance is left to the
0x20
delivery point.

### Error codes

Error
Description
code

Couldn’t fetch the resource or unit issue. See the reason
7
in the response.

Couldn’t update the specified route. Make sure the
6
provided route ID is correct.

4          Invalid call mode or incorrect provided data.
