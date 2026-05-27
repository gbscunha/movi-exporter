# Item search

One of the most common requests in Wialon is a search request. Two types
of search are available in Wialon:

searching items by ID,
searching items by property.

See the description of both search tpes below.

## Searching items by ID

If you know the ID of an item, you can get any available information about
this item by using the core/search_item method.

### Example

Let’s find out the last location of a unit with ID 34868. To get information
about the unit location, we must include flag 0x00000400 (1024) in the
request. Besides, let’s include flag 0x00000001 (1) to get the unit name.
For information about flags and data formats see the Data format section.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_item&params={
    "id": 34868,
    "flags": 1025
}
&sid=<your_sid>
```

Response example:

```json
{
    "item": {
        "nm": "Bavarian Tractor",
        "cls": 2,
        "id": 34868,

         "pos": {
              "t": 1358761631,
              "y": 53.9205504,
              "x": 27.4921152,
              "z": 238,
              "s": 0,
              "c": 102,
              "sc": 10
         },
         "lmsg": {
              "t": 1358761631,
              "f": 3,
              "tp": "ud",
              "pos": {
                   "y": 53.9205504,
                   "x": 27.4921152,
                   "z": 238,
                   "s": 0,
                   "c": 102,
                   "sc": 10
              },
              "i": 0,
              "p": {
                   "param22": 3,
                   "adc1": 12.352,
                   "pwr_ext": 12.356,
                   "param199": 0,
                   "param241": 25701,
                   "battery_charge": 0
              }
         },
         "uacl": 638138188323
    },
    "flags": 1025
}
```

From this response, we can find out that the unit with the specified ID is
called Bavarian Tractor and its last known location is 53.9205504° N and
27.4921152° E.

## Searching items by property

To find multiple items which have a certain property, use the
core/search_items method.

## Example 1

Let’s find all users by executing the following request:

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&params={
      "spec": {
           "itemsType": "user",
           "propName": "sys_name",
           "propValueMask": "*",
           "sortType": "sys_name"
      },
      "force": 1,
      "flags": 1,
      "from": 0,
      "to": 0
}&sid=<your_sid>
```

An asterisk in the propValueMask parameter means that the result array
will contain users with any values in the sys_name field (that is, users with
any names). It means all available users will be included in the result. Value
1 of the flags parameter means that basic information about the item must
be included in the result. For information about user flags, see the Users
page. Zero values of the from and to parameters indicate that all the
found users must be returned.

Response example:

```json
{
    "searchSpec": {
      "itemsType": "user",
      "propName": "sys_name",

         "propValueMask": "*",
         "sortType": "sys_name"
    },
    "dataFlags": 1,
    "totalItemsCount": 1,
    "indexFrom": 0,
    "indexTo": 0,
    "items": [
         {
             "nm": "test_6512789",
             "cls": 1,
             "id": 648548,
             "uacl": -1
         }
    ]
}
```

The example above can be used to search only items such as resources,
retranslators, units, unit groups, users and routes. But some of these items,
such as resources or routes, normally contain subitems. For instance,
geofences are resource subitems. You can see how to search subitems in
the examples below.

## Example 2

To search subitems, add the propType parameter to the search
specification, set its value to propitemname, and indicate the subitem
name in the propName parameter. You can find the list of all subitems on
the core/search_items page.

Let’s find resources which contain geofences with names including the
word office. We want the response to contain only the first two found
resources. In order for the response to include geofences, we must set flag
0x00001000 (4096) in addition to the basic flag.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&params={
    "spec": {

        "itemsType": "avl_resource",
        "propName": "zones_library",
        "propValueMask": "*office*",
        "sortType": "zones_library",
        "propType": "propitemname"
   },
   "force": 1,
   "flags": 4097,
   "from": 0,
   "to": 1
```

}&sid=<your_sid>

Response example:

{

```json
 "searchSpec": {
      "itemsType": "avl_resource",
      "propName": "zones_library",
      "propValueMask": "*office*",
      "sortType": "zones_library",
      "propType": "propitemname"
 },
 "dataFlags": 4097,
 "totalItemsCount": 1,
 "indexFrom": 0,
 "indexTo": 0,
 "items": [
      {
          "nm": "template_en",
          "cls": 3,
          "id": 163266,
          "zl": {
            "1": {
              "n": "Head office",
              "d": "",
              "id": 1,
              "f": 1,
              "t": 2,

"e": 60774,
"b": {
    "min_x": 43.5271002776,
    "min_y": 49.7636455785,
    "max_x": 43.5622908598,
    "max_y": 49.7794993012,
    "cen_x": 43.5446955687,
    "cen_y": 49.7715724398
}
```

},
"2": {

```json
"n": "Route1_final_destination",
"d": "",
"id": 2,
"f": 1,
"t": 2,
"e": 62438,
"b": {
    "min_x": 44.3872954375,
    "min_y": 48.6329175554,
    "max_x": 44.6300246245,
    "max_y": 48.856592389,
    "cen_x": 44.508660031,
    "cen_y": 48.7447549722
}
```

},
"3": {

```json
 "n": "Route1_starting_point",
 "d": "",
 "id": 3,
 "f": 1,
 "t": 2,
 "e": 4566,
 "b": {
     "min_x": 43.107388,
     "min_y": 50.009182,
     "max_x": 43.294156,
     "max_y": 50.119376,
     "cen_x": 43.200772,
     "cen_y": 50.064279

                  }
             },
             "4": {
                  "n": "Shopping mall",
                  "d": "",
                  "id": 4,
                  "f": 1,
                  "t": 1,
                  "e": 39844,
                  "b": {
                      "min_x": 37.5347102757,
                      "min_y": 55.7544919087,
                      "max_x": 37.5596537243,
                      "max_y": 55.7598140913,
                      "cen_x": 37.546216,
                      "cen_y": 55.757443
                  }
             },
             "5": {
                  "n": "Warehouse",
                  "d": "",
                  "id": 5,
                  "f": 1,
                  "t": 3,
                  "e": 44015,
                  "b": {
                      "min_x": 37.5537148786,
                      "min_y": 55.7585093867,
                      "max_x": 37.5576971214,
                      "max_y": 55.7607546133,
                      "cen_x": 37.555706,
                      "cen_y": 55.759632
                  }
             }
        },
        "uacl": 2200454562339
    }
]
```

}

As a result, one resource with 5 geofences was found. One of them contains
the word office in its name.

## Example 3

Let’s find units with the name mask *Volvo*:

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&params={
     "spec": {
          "itemsType": "avl_unit",
          "propName": "sys_name",
          "propValueMask": "*Volvo*",
          "sortType": "sys_name"
     },
     "force": 1,
     "flags": 1439,
     "from": 0,
     "to": 0
}&sid=021df621073f5b102b83740b0ea0eaf5
```

Specification:

Parameter                      Value              Description

itemsType                      avl_unit           Unit

propName                       sys_name           Search by name

propValueMask                  *Volvo*            Name mask

Response example:

{

```json
"searchSpec": {
     "itemsType": "avl_unit",
     "propName": "sys_name",
     "propValueMask": "*Volvo awe*",
     "sortType": "sys_name",
     "propType": "",
     "or_logic": "0"
},
"dataFlags": 1439,
"totalItemsCount": 1,
"indexFrom": 0,
"indexTo": 0,
"items": [
     {
         "nm": "Volvo awesome",
         "cls": 2,
         "id": 21728414,
         "prp": {
              "label_color": "39219",
              "solid_colors": "39219",
              "track_solid": "39219",
              "use_sensor_color": "0"
         },
         "crt": 930848,
         "bact": 930849,
         "mu": 0,
         "ct": 1599638776,
         "ftp": {
              "ch": 0,
              "tp": 0,
              "fl": 1
         },
         "uid": "Volvo XC90",
         "uid2": "",
         "hw": 96266,
         "ph": "+37069678441",
         "ph2": "",
         "psw": "",
```

"pos": {

```json
"t": 1614336759,
"f": 1073741831,
"lc": 0,
"y": 43.2444668333,
"x": -118.146447667,
"c": 0,
"z": 300,
"s": 12,
"sc": 8
```

},
"lmsg": {

```json
"t": 1614336759,
"f": 1073741831,
"tp": "ud",
"pos": {
     "y": 43.2444668333,
     "x": -118.146447667,
     "c": 0,
     "z": 300,
     "s": 12,
     "sc": 8
},
"i": 0,
"o": 0,
"lc": 0,
"rt": 1614336760,
"p": {
     "hdop": 0.5,
     "pass": "E2000020340F02371900D866",
     "mil": 1001,
     "ves": "900025517477741444444",
     "io_1_76": 459,
     "tco_activity_tm": 400,
     "fuel": 220.79,
     "tco_driver1_id": "rettt"
}
```

},
"act": 1,
"dactt": 0,

```json
            "flds": {
                 "1": {
                      "id": 1,
                      "n": "Type",
                      "v": "Navtelecom"
                 },
                 "2": {
                      "id": 2,
                      "n": "Device type",
                      "v": "Teltonika"
                 }
            },
            "fldsmax": -1,
            "aflds": {},
            "afldsmax": -1,
            "uri": "/avl_library_image/19725/0/library/unit/supertux.png",
            "ugi": 1,
            "uacl": -1
        }
    ]
}
```

## Example 4

Let’s get the list of subusers.

If the hierarchy is simple, that is, there is only one parent account and the
others are subordinate to it, you can get the list of subusers by specifiying
the creator’s name. To do this, pass rel_user_creator_name in the
propName parameter, and specify the creator’s name in the
propValueMask parameter.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&sid=0281169f3adf2593e00f2fc1&params={
    "spec": {

         "itemsType": "user",
         "propName": "rel_user_creator_name",
         "propValueMask": "chdi_test",
         "sortType": "sys_name"
    },
    "force": 1,
    "flags": 3,
    "from": 0,
    "to": 0
}
```

If the hierarchy is complicated, that is, there are several parent accounts,
you can get the list of subusers by specifiying the chain of creators. To do
this, pass creatortree in the propType parameter, and specify the name
of the top user’s ID (or any parent user’s ID, if you want to see only their
subusers) in the propValueMask parameter.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&sid=0281169f3adf2593e00f2fc1&params={
    "spec": {
         "itemsType": "user",
         "propName": "sys_user_creator",
         "propValueMask": 930848,
         "sortType": "sys_name",
         "propType": "creatortree"
    },
    "force": 1,
    "flags": 3,
    "from": 0,
    "to": 0
}
```
