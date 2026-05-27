# exchange

This section describes the methods related to data import and export.

## convert_file

To convert XLSX and CSV files into JSON, use the exchange/convert_file
method:

```http
svc=exchange/convert_file&params={"format":"csv", "separator":","}
```

The maximum file size is 64 MB.

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| format* | File format. The supported formats are XLSX and CSV. |
| separator* | Separator. Only for CSV files. |
| eventHash | Name of the event which will be generated after reading the data. |
| To convert a file, use a POST request with multiple parameters | (multipart/form-data). In form-data, make a separate parameter of the file type and specify the file name. In Postman, for example, you can do this in query params. |
| Request example: |  |
| hAXcAjtvh1D61XpC | Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=excha nge/convert_file&sid=8157df114c0e601f0f31091c3c2ac53d Request Method: POST Connection: keep-alive Content-Length: 1901 Cache-Control: no-cache Content-Type: multipart/form-data; boundary=----WebKitFormBoundary Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*; q=0.8 Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3 Accept-Encoding: gzip,deflate,sdch Accept-Language: ru,en-US;q=0.8,en;q=0.6 ------WebKitFormBoundaryhAXcAjtvh1D61XpC Content-Disposition: form-data; name="params" jUploadForm1372772377019 ------WebKitFormBoundaryhAXcAjtvh1D61XpC Content-Disposition: form-data; name="import_file"; filename="fil e.zip" Content-Type: application/zip ------WebKitFormBoundaryhAXcAjtvh1D61XpC-- |

### Response

In case the file is converted successfully, a JSON text is returned. If the
request didn’t contain the eventHash parameter, the response is returned
immediately. If it did, you should run the avl_evts method to see the result.

Response example:

```json
{

         "filename": "test.xlsx",

         "sheets": [

             {

    "rows": [

            [

                 "№",

                 "Time",

                 "User",

                 "Object type",

                 "Action",

                 "Host",

                 "Notes"

         ],

        [

                "1",

                "2023-09-13 10:45:15",

                "maqsat",

                 "Resource",

                 "Resource 'Radares Maqsat' create
```

d.",

"167.61.60.214",

#### " "

```json
       ],

                        [

                              "2",

                              "2023-09-13 10:45:16",

                              "maqsat",

                              "Resource",

                              "Account 'Radares Maqsat' created.",

                              "167.61.60.214",

                              " "

                        ]

                ]

      }

]

}
```

If conversion failed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| Excessive file size, invalid input parameters, or unknown file | 4 format. |
| 5 | Failed to open or convert the file. |
| 6 | Unknown error. |
| 7 | No access. |

## export_json

To export data to a WLP file, use the exchange/export_json method.

```http
svc=exchange/export_json&params={"fileName":<text>,
                   "json":{}}
```

This request can’t be executed simultaneously with any request from this
chapter and the following requests:

…/report/exec_report,
…/report/export_result,
…/report/get_result_chart,
…/report/get_result_map,

…/messages/load_interval,
…/render/create_messages_layer,

…/unit/get_trips,
…/resource/get_driver_bindings,

…/resource/get_trailer_bindings,
…/account/get_account_history.

### Parameters

| Parameter | Description |
| --- | --- |
| fileName | File name |
| json | JSON to be exported |

### Response

If the request is completed successfully, a WLP file is returned. Otherwise,
an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 3 | Parameters validation error or other types of errors. |
| 1 | Invalid or obsolete request SID. |

## export_messages

To export messages (loaded to a layer or directly) to a file, use the
exchange/export_messages method.

```http
svc=exchange/export_messages&params={"layerName":<text>,
                       "format":<text>,
                       "itemId":<long>,
                       "timeFrom":<uint>,
                       "timeTo":<uint>,
                       "compress":<bool>}
```

This request can’t be executed simultaneously with any request from this
chapter and the following requests:

…/report/exec_report,
…/report/export_result,
…/report/get_result_chart,
…/report/get_result_map,
…/messages/load_interval,
…/render/create_messages_layer,
…/unit/get_trips,
…/resource/get_driver_bindings,
…/resource/get_trailer_bindings,
…/account/get_account_history.

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| layerNa      Message layer name. Specify it to export messages from | me           a layer. |
| itemId | Unit identifier in the system. Specify it to export messages directly. |
| format* | File format: txt, kml, plt, wln, wlb. |
| timeFrom | Start of the interval. Specify it to export messages directly. |
| timeTo | End of the interval. Specify it to export messages directly. |
| compress     Specify 1 to compress the file, or 0 to get the | *            uncompressed file. |

### Response

Returns a file of the specified format.

If the request parameters have
the itemId, timeFrom, timeTo, format and compress fields, the unit is
obtained by the value of the itemId field and then the unit messages
from timeFrom to timeTo are returned. The layerName field is ignored in
this case, even if it is specified in the request. Otherwise (if at least one of
the temId, timeFrom, timeTo, format and compress fields is missing),
the layer is obtained by the value of the layerName field; after that, the
unit is obtained from the layer and all the unit messages are returned (in
this case the timeFrom and timeTo fields are ignored). In other words, the
method operates in two modes. The first one
requires the itemId, timeFrom, timeTo, format and compress fields; the
second one requires the layerName, format and compress fields.

If the request wasn’t completed successfully, an error code is returned.

### Error codes

Co
Description
de

1      Invalid or obsolete request SID.

One of the following errors:

error validating parameters,
4
layer not found,
failed to save messages to the temporary file.

One of the following errors:

failed to fetch the user,
6
failed to fetch the renderer,
compression-related problems.

One of the following errors:

unit not found,
7         failed to fetch the unit with the required access rights (for the
first mode, it is ADF_ACL_ITEM_EXECUTE_REPORTS, for the
second mode, it is ADF_ACL_AVL_UNIT_EXPORT_MSGS).

10     The unit has no messages within the specified time interval, or
01     any messages at all.

## export_zones

To export geofences to a KML or KMZ file, use the
exchange/export_zones method .

```http
svc=exchange/export_zones&params={"fileName":<text>,
                                      "zones":[
                                             {
                                                    "itemId":<long>,
                                                    "id":<long>
                                             }
                                     ],
                                     "compress":<bool>}
```

This request can’t be executed simultaneously with any request from this
chapter and the following requests:

…/report/exec_report,
…/report/export_result,
…/report/get_result_chart,
…/report/get_result_map,
…/messages/load_interval,
…/render/create_messages_layer,
…/unit/get_trips,
…/resource/get_driver_bindings,
…/resource/get_trailer_bindings,
…/account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| fileName | File name. |
| zones | Array of geofences. |
| itemId | Resource ID. |
| id | Geofence ID. |
| compres      Specify 1 to compress the file, or 0 to get the | s            uncompressed file. |

### Response

If the request is completed successfully, a KML or KMZ file is returned.

Currently, if the resource or geofence with the specified ID is not found on
the server, a XML response with the file name is generated:

### Request

```json
{"fileName":"export_zones_result","zones":[{"itemId":<nonexisting-resource-id>,"id":<nonexisting-geofence-id>}],"compress":0}
```

### Response

#### <?xml version="1.0" encoding="utf-8"?>

<kml>
<Document>
<name>
export_zones_result
</name>
</Document>
</kml>

If the request is not completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| One of the following errors: |  |
| parameter validation error, | 4 empty array of geofences in the request, failed to create a directory for temporary results. |
| One of the following errors: |  |
| failed to fetch the current user, | 6 error processing XML, error compressing the file. |

## import_json

To read data from a WLP file, use the exchange/import_json method.

```http
svc=exchange/import_json&params={"eventHash":<text>}
```

This request can’t be executed simultaneously with any request from this
chapter and the following requests:

…/report/exec_report,
…/report/export_result,

…/report/get_result_chart,
…/report/get_result_map,
…/messages/load_interval,
…/render/create_messages_layer,

…/unit/get_trips,
…/resource/get_driver_bindings,

…/resource/get_trailer_bindings,
…/account/get_account_history.

### Parameters

You can include the optional parameter eventHash in the request. It allows
specifying the event name which will be generated after reading the data.

## Loading a file

To load a WLP file, use a POST request with multiple contents
(multipart/form-data). For example:

Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=excha
nge/import_json&sid=8157df114c0e601f0f31091c3c2ac53d
Request Method: POST
Connection: keep-alive
Content-Length: 1901
Cache-Control: no-cache
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
hAXcAjtvh1D61XpC
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;
q=0.8
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3
Accept-Encoding: gzip,deflate,sdch
Accept-Language: ru,en-US;q=0.8,en;q=0.6

------WebKitFormBoundaryhAXcAjtvh1D61XpC
Content-Disposition: form-data; name="params"

```json
{"eventHash":"jUploadForm1372772377019"}
------WebKitFormBoundaryhAXcAjtvh1D61XpC
Content-Disposition: form-data; name="eventHash"

jUploadForm1372772377019
------WebKitFormBoundaryhAXcAjtvh1D61XpC
Content-Disposition: form-data; name="import_file"; filename="file.zip"
Content-Type: application/zip

------WebKitFormBoundaryhAXcAjtvh1D61XpC--
```

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

To be sure that data has been read, you can execute the events method:

```json
{
        "tm":<uint>,                                  /* current servertime (UTC) */
        "events":[
                 {
                          "i":-1,
                          "d":{                       /* data */
                                    "hash":<text>,            /* uploadcomplete */files: {                  /* files uploaded */
                                               <text>:<Object>,               /*file name: file data */...
                                    }
                          }
                 }
        ]
}
```

If the request is not completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 4 | No files attached. |
| 7 | Failed to obtain the current user. |

## import_messages

To import messages from a file, use the exchange/import_messages method.

svc = exchange/import_messages&params={

```json
    "itemId": <long>,
    "eventHash": <text>
}
```

This request can’t be executed simultaneously with any request from this
chapter and the following requests:

…/report/exec_report
…/report/export_result

…/report/get_result_chart
…/report/get_result_map

…/messages/load_interval
…/render/create_messages_layer

…/unit/get_trips
…/resource/get_driver_bindings

…/resource/get_trailer_bindings
…/account/get_account_history

### Parameters

The required parameter is marked with an asterisk (*).

| Name | Description |
| --- | --- |
| itemId* | Item ID. |
| eventHash | Event name, which will be generated after messages are imported. |
| dontMarkImported | If this parameter is set to 1, imported messages will not be marked as imported but as blackbox; the registration time may differ from the message time. If this parameter is missing or set to a value other than 1, messages will be marked as imported. |

## Loading a file

To load a file, use a POST request with multiple contents (multipart/form-
data). For example:

Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=excha
nge/import_messages&sid=8157df114c0e601f0f31091c3c2ac53d
Request Method: POST
Connection: keep-alive
Content-Length: 2744
Cache-Control: no-cache
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
lvunQiir9AesO8qB
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;
q=0.8
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3

Accept-Encoding: gzip,deflate,sdch
Accept-Language: ru,en-US;q=0.8,en;q=0.6

------WebKitFormBoundarylvunQiir9AesO8qB
Content-Disposition: form-data; name="params"

```json
{"itemId":898446,"eventHash":"jUploadForm1372773585167"}
------WebKitFormBoundarylvunQiir9AesO8qB
Content-Disposition: form-data; name="eventHash"

jUploadForm1372773585167
------WebKitFormBoundarylvunQiir9AesO8qB
Content-Disposition: form-data; name="messages_filter_import_file"; filename="4100.zip"
Content-Type: application/zip

------WebKitFormBoundarylvunQiir9AesO8qB--
```

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

To make sure that the messages have been imported, you can execute the
avl_evts method.

```json
{
    "tm": <uint>,            /* current server time (UTC) */
    "events": [
      {
          "i": -1,
          "d": {             /* data */
           "hash": <text>,   /* upload complete */
           "msgCount": <text>/* number of imported messages */

            }
        }
    ]
}
```

If the request is not completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 4 | No file attached. |
| 6 | Internal error. |
| One of the following errors: |  |
| failed to fetch the user, |  |
| 7                   unit not found, | failed to fetch the unit with the required access right (ADF_ACL_AVL_UNIT_IMPORT_MSGS). |

## import_pois_read

This method is deprecated and shouldn’t be used. Currently, it returns an
error code.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 7 | Returned in all other cases. |

## import_pois_save

This method is deprecated and shouldn’t be used. Currently, it returns an
error code.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 7 | Returned in all other cases. |

## import_zones_read

To read geofences from a file, use the
exchange/import_zones_read method:

```http
svc=exchange/import_zones_read&params={"eventHash":<text>}
```

This request can’t be executed simultaneously with any request from this
chapter and the following requests:

…/report/exec_report,
…/report/export_result,
…/report/get_result_chart,
…/report/get_result_map,
…/messages/load_interval,
…/render/create_messages_layer,
…/unit/get_trips,
…/resource/get_driver_bindings,
…/resource/get_trailer_bindings,
…/account/get_account_history.

### Parameters

You can include the optional parameter eventHash in the request. It allows
specifying the event name which will be generated after reading the data.

## Uploading a file

To upload a file with geofences, use a POST request with multiple contents
(multipart/form-data). For example:

Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=excha
nge/import_zones_read&sid=8157df114c0e601f0f31091c3c2ac53d
Request Method: POST
Connection: keep-alive
Content-Length: 1281
Cache-Control: no-cache
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
zmBiAUFQVzA8mRkx
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;
q=0.8
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3
Accept-Encoding: gzip,deflate,sdch

#### Accept-Language: ru,en-US;q=0.8,en;q=0.6

------WebKitFormBoundaryzmBiAUFQVzA8mRkx
Content-Disposition: form-data; name="params"

```json
{"eventHash":"jUploadForm1372771850650"}
------WebKitFormBoundaryzmBiAUFQVzA8mRkx
Content-Disposition: form-data; name="eventHash"

jUploadForm1372771850650
------WebKitFormBoundaryzmBiAUFQVzA8mRkx
Content-Disposition: form-data; name="import_file"; filename="geofence.kml"
Content-Type: application/vnd.google-earth.kml+xml

------WebKitFormBoundaryzmBiAUFQVzA8mRkx--
```

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

To make sure that the geofences have been read, you can execute the
…/requests/avl_evts method:

```json
{
      "tm": <uint>,                   /* current server time (UTC) */
      "events": [
          {
              "i": -1,
              "d": {                  /* data */
                    "hash": <text>,           /* upload complete */

                  "zones": [<Object>]         /* array of geofences read */
             }
        }
    ]
}
```

If the request is not completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | Invalid or obsolete request SID. |
| 4 | No files attached. |
| 7 | Failed to fetch the user. |

## import_zones_save

To import geofences, use the exchange/import_zones_save method:

```http
svc=exchange/import_zones_save&params={"itemId":<long>,
                                               "zones":[{
                                                        "n":<text>,
                                                        "d":<text>,
                                                        "id":<long>,
                                                        "t":<byte>,
                                                        "w":<uint>,
                                                        "f":<uint>,
                                                        "c":<uint>,

                                                 "b":{
                                                          "min_x":<double>,
                                                          "min_y":<double>,
                                                          "max_x":<double>,
                                                          "max_y":<double>,
                                                          "cen_x":<double>,
                                                          "cen_y":<double>
                                                 },
                                                 "p":[{
                                                          "x":<double>,
                                                          "y":<double>,
                                                          "r":<uint>
                                                 }]
                                           }]}
```

This request can’t be executed simultaneously with any request from this
chapter and the following requests:

…/report/exec_report,

…/report/export_result,
…/report/get_result_chart,

…/report/get_result_map,
…/messages/load_interval,

…/render/create_messages_layer,
…/unit/get_trips,

…/resource/get_driver_bindings,
…/resource/get_trailer_bindings,

…/account/get_account_history.

### Parameters

| Name | Description |
| --- | --- |
| itemId | Resource ID in the system. |
| id | Geofence ID in the system. |
| zones | Array of geofence IDs. |
| You can find the description of other parameters on | the get_zone_data page. |
| In geofence description the following parameters are required: n (geofence | name), t (geofence type), w (line thickness or circle radius), f (flags), c (color), p (geofence points). The other geofence parameters are useful, but optional. The itemId parameter (resource ID) is required. |

### Response

If the request is completed successfully, the number of imported geofences
is returned:

#### <int>

If the request is not completed, an error code is returned.

### Error codes

Co
Description
de

1       Invalid or obsolete request SID.

4       Parameter validation error.

6       No geofence IDs specified.

One of the following errors:

resource with the specified ID doesn't exist,

7           failed to fetch the resource with the specified access right
(ADF_ACL_AVL_RES_EDIT_ZONES),
failed to fetch user.
