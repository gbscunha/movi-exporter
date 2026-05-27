# messages

This section describes the methods for working with the message loader.
You can load messages into the loader
using the load_last or load_interval methods and work with them. To load
another set of messages, just add it to the loader. You can clear the loader
by running the unload method.

The loader allows working with only one set of messages,
which is saved into the session on the server side. Later,
you can call methods such as …/unit/calc_sensors for this
set of messages. Adding the next set of messages to the
loader leads to the automatic flush of the current one.

## delete_message

To delete a message, use the method messages/delete_message:

```http
svc=messages/delete_message&params={"msgIndex":<uint>}
```

You can find an example of this request in the sample messages.

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| msgIndex* | Message index. |

### Response

```json
{} /* an empty object if the execution is successful; if not, an error code */
```

### Error codes

Error
Description
code

There is no such message or this message is the last one
4
and can't be deleted, or failed to fetch the unit.

6           Error deleting message.

7           User not found, or no rights on message deletion.

## get_messages

To get messages from the message loader, use the method
messages/get_messages:

```http
svc=messages/get_messages&params={"indexFrom":<uint>,
                                          "indexTo":<uint>,
                                          "timeFrom:"<uint>,
                                          "timeTo":<uint>,
                                          "filter":"<text>",
                                          "flags":<uint>,
                                          "flagsMask":<uint>,
                                          "loadCount":<uint>}

        You can find an example of this request in the samplemessages.
```

### Parameters

The parameters are optional.

| Name | Description |
| --- | --- |
| m | indexFro Index of the first requested message. |
| indexTo | Index of the last requested message. |
| timeFrom | Interval beginning. |
| timeTo | Interval end. |
| filter | Filter, search in the pos and p parameters. |
| flags | Flags for loading messages. See below. |
| k | flagsMas Mask. See below. |
| loadCoun       Number of messages to return (0xffffffff means all the | t              found ones). |
| The method logic is extended: you can use both the old | indexFrom/indexTo logic and the new ones: |
| Logic | Description |
| meTo | timeFrom/ti Determine the start and end time of the messages. |
| timeFrom/lo         Determine the start time of the messages. It will | adCount             display the loadCount number of the last messages. |
| timeTo/load         Determine the end time of the messages. It will | Count               display the loadCount number of the last messages. |
| The filter option can be used for any logic. The search is available in the | pos and p parameters. Even if there are no such parameters in the messages, all the messages contain basic information: t, f, tp. i. o. |

#### Important

To use this method, the request should contain at least one
of the parameter pairs from above.

Response example (no filtering):

```json
[
    {
        "t": 1426233861,
        "f": 7,
        "tp": "ud",
        "pos": {
                  "y": 53.84541,
                  "x": 27.4470783333,
                  "z": 0,
                  "s": 25,
                  "c": 285,
                  "sc": 255
                  },
        "i": 0,
        "o": 0,
        "p": {
                  "adc1": 0,
                  "pre2": 123,
                  "param": 24,
                  "param5": 43
        }
    }
]
```

Filter example:

```json
"filter":"pos.x,p.pre*,p.param?"
```

Filtered response:

```json
[
        {
                  "t": 1426233861,
                  "f": 7,

                  "tp": "ud",
                  "pos": {
                            "x": 27.4470783333
                            },
                  "i": 0,
                  "o": 0,
                  "p": {
                            "pre2": 123,
                            "param5": 43
                  }
        }
]
```

After filtering we see the pos.x value, the values of the parameters in the
pos object which begin with pre, the values of the parameters in the pos
object which begin with param and have one more symbol at the end (for
example, param1 is valid, but param is invalid for search).
The number of defined parameters separated by a comma is unlimited. The
asterisk (*) is used as a wildcard for 0 or more symbols, and the question
mark (?) as a wildcard for one symbol.

### Response

```json
[       /* message array */
        { ... },            /* message */
        { ... }             /* message */
]
```

You can find message formats here.

### Error codes

Error code      Description

4                Invalid input parameters or failed to fetch messages.

## get_task_messages

The messages/get_task_messages request allows you to load registered
event messages for all units to which you have the View object and its
basic properties access rights.

```http
svc=messages/get_task_messages&params={
        "itemIds": [<long>],
        "timeFrom":<uint>,
    "timeTo":<uint>,
    "loadCount":<uint>
}
```

Request example:

```http
https://hst-api.wialon.com/wialon/ajax.html?sid=b8c179f636baedfd43e1890bd48a8ee9&svc=messages/get_task_messages&params={
        "itemIds":[1546, 1545],
        "timeFrom": 1724347800,
        "timeTo": 1724693399,
        "loadCount": 10000
}
```

### Parameters

The following parameters are required:

| Name | Description |
| --- | --- |
| itemIds | The IDs of the units. |
| m | timeFro The beginning of the interval. |
| timeTo | The end of the interval. |
| loadCou       Number of messages to return. The maximum number is | nt            20000. |

### Response

Example of a response when the request is completed successfully:

{

```json
"count": 5,
"messages": [
     {
         "item_id": 1546,
         "t": 1724420460,
         "f": 1536,
         "tp": "task",
         "et": "adf",
         "x": 0,
         "y": 0,
         "rt": 1724420493,
         "p": {
              "task_sub_type": 21,
              "task_reg_type": 1,
              "task_evt_name": "Custom event",
              "task_id": "b1978b93a308c5c3be0697223bf0c5002ee87d
```

e02ce7937b23a34830516c330466c8916c",

```json
                  "task_update_time": 1724420460,
                  "task_status": 6,
                  "task_priority": 2,
                  "task_assignee": 0,

                     "task_description": "VHS Glitch violated speed limitations."
                     "task_tags": "{\"SPEED\":\"25 km/h\",\"POS_TIME
\":\"10.07.2025 15:52:28\",\"UNIT\":\"VHS Glitch\"}",
                     "task_comments": "[]",
                     "task_account": 1063
                     "task_address_x": 56.65078,
                     "task_address_y": 53,
                     "task_done_rejected": 1752152438,
                     "task_params": {}
                }
          },
      ]
}
```

If the request is not completed, an error code is returned.

### Error codes

Error
Description
code

4               Invalid input parameters.

5               Request execution error.

Access denied. The View object and its basic
7
properties access rights to the units is required.

The maximum number of messages (loadCount) is
1004
exceeded.

## unload

To clear the message loader, use the method messages/unload:

```http
svc=messages/unload&params={}
```

You can find an example of this request in the sample messages.

### Response

```json
{}       /* an empty object if the execution is successful; if not,
an error code */
```

## get_message_file

To get a photo from a driver message, use the method
messages/get_message_file:

```http
svc=messages/get_message_file&params={"itemId":<uint>,
                                            "fileId":"<text>"}
/*Alternative request form:*/svc=messages/get_message_file&params={"msgIndex":<uint>,
                                               "fileName":"<text>"}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| itemId* | Driver ID. |
| fileId* | Image file ID. |

## Alternative request parameters

| Name | Description |
| --- | --- |
| msgIndex* | Message index. |
| fileName* | File name. |
| You can get the fileID parameter here. |  |

### Response

Returns an image.

### Error codes

Error
Description
code

Failed to fetch the message manager with ACL
7
(ADF_ACL_ITEM_EXECUTE_REPORTS).

Incorrect parameters, or file not found, or failed to fetch
4
messages.

## load_interval

To load messages for a certain interval, use the method
messages/load_interval:

```http
svc=messages/load_interval&params={
    "itemId": <long>,
    "timeFrom": <uint>,
    "timeTo": <uint>,
    "flags": <uint>,
    "flagsMask": <uint>,
    "loadCount": <uint>
}
```

This request can’t be executed simultaneously with the following requests:

…/report/exec_report,
…/report/export_result,

…/report/get_result_chart,
…/report/get_result_map,
…/render/create_messages_layer,
…/unit/get_trips,
…/resource/get_driver_bindings,
…/resource/get_trailer_bindings,
all requests from the section exchange,

…/account/get_account_history.

You can find an example of the load_interval request in the
sample messages.

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| Unit or resource ID (depends on the type of message | itemId* you want to get). |
| timeFrom* | Interval beginning. |
| timeTo* | Interval end. |
| flags* | Flags for loading messages. See the description below. |
| flagsMask* | Mask. See the description below. |
| Number of messages to return (0xffffffff means all the | loadCount* found ones). |

## Examples of using masks and flags

Mask         Flag       Result

0xFF00       0x0000     All data messages.

Data messages which contain the alarm bit
0xFF10       0x0010
(0x10).

Data messages which contain the alarm bit
0xFFF0       0x0010     (0x10), but don’t contain information about the
driver code (0x20).

0xFFF2       0x0022     Data messages which contain information about
the driver code (0x20) and input data

Mask               Flag        Result

information (0x02), but don’t contain the alarm
bit (0x10).

0xFF01             0x0601      Events regarded as violations.

Data messages which contain information about
0x4000             0x4000
triggered notifications.

### Response

If the request is completed successfully, the response is as follows:

```json
{
    "count": <uint>,                       /* number of messages */
    "messages": [                          /* array of messages */
        {
            ...
        }
    ]
}
```

You can find message formats, masks and flags here.

If the request is not completed successfully, an error code is returned.

### Error codes

Error code                  Description

7                           Failed to fetch the message manager.

Error code         Description

6                  Failed to fetch messages for the interval.

4                  Failed to get the current user.

1003               Accept-encoding is not gzip.

## load_last

To load a few latest messages for a specified point in time, use the method
messages/load_last:

```http
svc=messages/load_last&params={"itemId":<long>,
                                "lastTime":<uint>,
                                "lastCount":<uint>,
                                "flags":<uint>,
                                "flagsMask":<uint>,
                                "loadCount":<uint>}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| Unit or resource ID (depends on the type of message you | itemId* want to get). |
| lastTime | Time for which messages are requested. * |
| lastCoun | Number of messages which should be loaded. t* |
| Message flags. Used for loading messages with the | flags* specified flags only. See more. |
| flagsMas | Mask. See load_interval. k* |
| loadCoun | Number of messages to return. t* |

### Response

If the request is executed successfully, the following result is returned:

```json
{
          "count":<uint>,                            /* number of messages */
          "messages":[                               /* array of messages */
                  {
                            ...
                  }
          ]
}
```

You can find message formats here.

If the request is not executed successfully, an error code is returned.

### Error codes

Error
Description
code

Failed to fetch the message manager with the required
7
ACL (ADF_ACL_ITEM_EXECUTE_REPORTS).

6            Failed to fetch unit messages.

No messages found for the specified interval, or the
4
number of messages exceeds the limit (10000).

## Message request examples

You can manage messages with the help of the message loader. First, you
should load messages into the message loader using either of the two
methods: messages/load_last or messages/load_interval. Then you can
work with the messages. However, if you want to load other messages, you
should clear the loader first, using the method messages/unload.

## Loading messages

Let’s load data messages with location for the interval from 01.04.2013 to
20.04.2013 using the request messages/load_interval and get the first
three of them. To request only data messages with location, use the mask
0xFF01 (65281). The mask 0xFF00 (65280) determines the message type,
0x0001 (1) detects the availability of location information in messages.
Also, it is necessary to use the flag 0x0001 (1), which comes from the sum
of the flag 0x0000 (0) for data messages and the flag 0x0001 (1) for
messages with location.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=messages/load_interval&params={

                                    "itemId":34868,
                                    "timeFrom":1364760000,
                                    "timeTo":1366487999,
                                    "flags":1,
                                    "flagsMask":65281,
                                    "loadCount":3
                }&sid=<your_sid>
```

Response:

{

```json
        "count": 9172,
        "messages": [{
               "t": 1364760081,
               "f": 3,
               "tp": "ud",
               "pos": {
                         "y": 53.8396544,
                         "x": 27.5608672,
                         "z": 213,
                         "s": 0,
                         "c": 51,
                         "sc": 9
               },
               "i": 0,
               "p": {
                         "param22": 3,
                         "adc1": 12.606,
                         "pwr_ext": 12.598,
                         "param199": 0,
                         "param241": 25701,
                         "battery_charge": 0
               }
        }, {
               "t": 1364760381,
               "f": 3,
               "tp": "ud",
               "pos": {

                 "y": 53.8396544,
                 "x": 27.5609312,
                 "z": 213,
                 "s": 0,
                 "c": 73,
                 "sc": 9
       },
       "i": 0,
       "p": {
                 "param22": 3,
                 "adc1": 12.545,
                 "pwr_ext": 12.547,
                 "param199": 0,
                 "param241": 25701,
                 "battery_charge": 0
       }
}, {
       "t": 1364760682,
       "f": 3,
       "tp": "ud",
       "pos": {
                 "y": 53.8396736,
                 "x": 27.5609664,
                 "z": 215,
                 "s": 0,
                 "c": 64,
                 "sc": 9
       },
       "i": 0,
       "p": {
                 "param22": 3,
                 "adc1": 12.6,
                 "pwr_ext": 12.569,
                 "param199": 0,
                 "param241": 25701,
                 "battery_charge": 0
       }
}]
```

}

After loading the messages, you can choose any number of them for
further processing. For example, let’s choose the ninth message from the
loader. To do this, use the request messages/get_messages:

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=messages/get_messages&params={
                   "indexFrom":8,
                   "indexTo":9
         }&sid=<your_sid>
```

Response:

```json
[{
         "t": 1364762485,
         "f": 3,
         "tp": "ud",
         "pos": {
                   "y": 53.8396992,
                   "x": 27.5609216,
                   "z": 223,
                   "s": 0,
                   "c": 45,
                   "sc": 7
         },
         "i": 0,
         "p": {
                   "param22": 3,
                   "adc1": 12.584,
                   "pwr_ext": 12.569,
                   "param199": 0,
                   "param241": 25701,
                   "battery_charge": 0
         }
}]
```

## Deleting messages

Now let’s delete the first message using the
request messages/delete_message:

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=messages/delete_message&params={
                 "msgIndex":0
         }&sid=<your_sid>
```

Response:

```json
{ }
```

## Clearing message loader

If you want to load messages for another interval or unit, clear the
message loader first:

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=messages/unload&params={}&sid=<your_sid>
```

Response:

```json
{ }
```
