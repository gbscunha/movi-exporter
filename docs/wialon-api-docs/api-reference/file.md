# file

In this section, you can find all the methods related to file storage.

## get

In order to get a file from the file storage, use the file/get method.

```http
svc=file/get&params={"itemId":<long>,
                                   "storageType":<uint>,
                                   "path":<text>,
                                   "format":<uint>}
```

### Parameters

| Parameter | Description |
| --- | --- |
| itemId | Item ID. |
| e | Storage type: 1 - public (all users can see and download storageTyp files), 2 - protected (only users with access rights can see and download files). |
| path | Relative path from the root folder to the file. |
| format | Specify "format":1 to get a DDD file in VDO format. |

### Response

Returns the file.

If there is no file according to the specified path, an error code is returned:

#### Invalid input{"error":3}

## library

If you want to get PNG, SVG, GIF, and JPG files from default or custom
libraries, use the file/library method.

```http
svc=file/library&params={"type":<text>,
                            "flags":<uint>}
```

### Parameters

| Parameter | Description |
| --- | --- |
| type | Library name. The default values are unit, group, poi. |
| Specify one of the values: | 0 - list files only from the default library (only default flags           type values are valid); 1 - list files from all available hierarchy libraries recur- sively (your account, parent, parent's parent, etc.) |

## Creating and finding a custom library

To create a custom library, follow these steps:

1. Create the directory library in the public file storage of the account:
<account_id>/1/library
2. Place a custom library in the library folder. For example, if your custom
library is called cust_lib, the path will be
<account_id>/1/library/cust_lib

To find the custom library and list its content, specify the library name as
a type value. For example, type:‘cust_lib’

### Response

If the request is completed successfully, a list of files is returned.

```json
{
      "<account_id>": [          /* account ID, 0 - default library */
                          {
                              "n":<text>,        /* file name */
                              "s":<uint>,        /* file size (bytes) */
                              "ct":<uint>,       /* file creation time,
UNIX-time */

                               "mt":<uint>       /* file last modification time, UNIX-time */
                         },
                         ...
    ],
    ...                          /* other account IDs (if any) */
}
```

If the request is not completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | User not authorized. |
| 4 | Invalid input parameters. |
| Failed to retrieve the list of files from the library and | 5 accounts. |
| Failed to retrieve the current account or item with the | 7 standard library. |

## list

To see the storage folder structure, use the file/list method:

```http
svc=file/list&params={"itemId":<long>,
                         "storageType":<uint>,
                         "path":<text>,

                         "mask":<text>,
                         "recursive":<bool>,
                         "fullPath":<bool>}
```

### Parameters

| Parameter | Description |
| --- | --- |
| itemId | Item ID. |
| Storage type: | storageTy       1 - public (all users can see and download files), pe              2 - protected (only users with access rights can see and download files). |
| path | Relative path from the root folder to the file. |
| mask | File name mask. It can contain the asterisk (*) which replaces 0 or more characters, and the question mark (?) which replaces 1 character. If you specify several masks, separate them by commas. |
| recursive | Use this flag to specify whether you want the content to be displayed recursively with subdirectories. |
| fullPath | Use this flag to specify whether you want to see the full path of the items. |
| Only the item creator can place and delete files. |  |

### Response

If the request is completed successfully, the storage structure is
returned. The signature n/c means that the hierarchy item is a folder, the
signature n/s means this is a file.

```json
[
          {
                  "n": <text>,               /* path to the selected folder, starts with "public" or "protected" */
                  "c": [                     /* root folder content, itcan include files and/or folders */
                                   {
                                             "n": <text>     /* foldername */
                                             "c": [...]      /* foldercontent, it can include files and/or folders */
                                   },

                                   {
                                             "n": <text>,    /* file name */
                                             "s": <text>     /* file size (bytes) */
                                   },
                                   ...
                  ]
          }
]
```

If the request hasn’t been completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | User not authorized. |
| 4 | Invalid input parameters. |
| 5 | Failed to get the list of files at the specified path. |
| Insufficient rights to the item specified in the itemId | 7 parameter. |

## mkdir

To create a new folder in the file storage, use the file/mkdir method:

```http
svc=file/mkdir&params={"itemId":<long>,
                                  "storageType":<uint>,
                                  "path":<text>}
```

### Parameters

| Parameter | Description |
| --- | --- |
| itemId | Item ID |
| Storage type: | storageTyp       1 — public (all users can see and download files), e                2 — protected (only users with access rights can see and download files). |
| path | Relative path from the root folder to the folder you want to create. |

### Response

If the request is completed successfully, an empty response is returned:

```json
{ }
```

If the request hasn’t been completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | User not authorized. |
| 4 | Invalid input parameters. |
| 5 | Failed to create a folder at the specified path. |
| Insufficient rights to the item specified in the itemId | 7 parameter. |

## put

To upload files to the file storage, use the file/put method.

```http
svc=file/put&params={
"itemId": <long>,
"storageType": <uint>,
"path": <text>,
"writeType": <uint>,

"eventHash": <text>
}&sid=<text>
```

### Parameters

Paramete
Description
r

itemId          Item ID.

Storage type:
1 — public (all users can see and download
storageTy       files);
pe              2 — protected (only users with access rights can see
and download
files)

path            Relative path from the root folder to the file.

Write type:
0 — overwrite the file,
writeType
1 — append to the file content,
2 — don't overwrite if the file exists.

eventHas        Name of the event which will be generated after
h               processing the data.

A file mustn’t have the same name as a folder.

To upload multiple files, send them using a POST request with parameters
(multipart/form-data). For example:

Request URL: https://hst-api.wialon.com/wialon/ajax.html?svc=file/
put
Request Method: POST
Connection: keep-alive
Content-Length:333998
Cache-Control:max-age=0
Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryM
pLUirMexsfCGaJP
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;
q=0.8
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3
Accept-Encoding: gzip,deflate,sdch
Accept-Language: ru,en-US;q=0.8,en;q=0.6

------WebKitFormBoundaryhJ0ZukEcpN7MgFnC
Content-Disposition: form-data; name="params"

```json
{"itemId":439,"storageType":"1","path":"1","writeType":0,"eventHash":"jUploadForm1414572405484"}
------WebKitFormBoundaryhJ0ZukEcpN7MgFnC
Content-Disposition: form-data; name="eventHash"

jUploadForm1414572405484
------WebKitFormBoundaryhJ0ZukEcpN7MgFnC
Content-Disposition: form-data; name="f"; filename="one-file"
Content-Type: application/octet-stream

------WebKitFormBoundaryhJ0ZukEcpN7MgFnC--
```

### Response

If the request is completed successfully, the following response is returned:

```json
{
    "error":0
}
```

If the request is not completed, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| 1 | User not authorized. |
| 4 | Invalid input parameters. |
| Insufficient rights to the item specified in the itemId | 7 parameter. |

## read

To read a text file, use the file/read method.

```http
svc=file/read&params={
     "itemId": <long>,
     "storageType": <uint>,
     "path": <text>,
     "contentType": <uint>
}
```

### Parameters

Paramete
Description
r

itemId          Item ID.

Storage type:
storageTy       1 — public (all users can see and download files),
pe              2 — protected (only users with access rights can see
and download files).

path            Relative path from the root folder to the file.

Content type. The content can be returned as:
contentTy       0 — text,
pe              1 — hex string,
2 — base64 string.

### Response

If the request has been completed successfully, the file content is returned.

```json
{
      "content": <content>
}
```

If the request hasn’t been completed, an error code is returned.

### Error codes

Cod
Description
e

1        User not authorized.

3        File not found.

4        Invalid input parameters.

Insufficient rights to the item specified in the itemId
7
parameter.

## rm

To delete a file, use the file/rm method.

```http
svc=file/rm&params={
    "itemId": <long>,
    "storageType": <uint>,
    "path": <text>
}
```

### Parameters

Paramete
Description
r

itemId         Item ID.

Storage type:
storageTy      1 — public (all users can see and download files),
pe             2 — protected (only users with access rights can see
and download files).

path            Relative path from the root folder to the file.

To clear public or protected storage totally, use “path”:“/”
in your request.

### Response

If the request is completed successfully, you will receive an empty
response.

```json
{}    /* empty json */
```

If the request hasn’t been completed, an error code is returned.

### Error codes

Erro
r         Description
code

1         User not authorized.

4         Invalid input parameters.

5         File not found.

Insufficient rights to the item specified in
7
the itemId parameter.

## write

To write text content into a file, use the file/write method:

```http
svc=file/write&params={
    "itemId":<long>,
    "storageType":<uint>,
    "path":<text>,
    "content":<text>,
    "writeType":<uint>,
    "contentType":<uint>
}
```

### Parameters

Paramete
Description
r

itemId         Item ID.

Storage type:
storageTy      1 — public (all users can see and download files),
pe             2 — protected (only users with access rights can see
and download files).

path           Relative path from the root folder to the file.

content        File content.

Write type:
0 — overwrite the file,
writeType
1 — append to the file content,
2 — don't overwrite if the file exists.

Content type. The content can be returned as:
contentTy      0 — text,
pe             1 — hex string,
2 — base64 string.

### Response

If the request is completed successfully, an empty response is returned.

```json
{} /* empty json */
```

Otherwise, an error code is returned.

### Error codes

Co
Description
de

1       User not authorized.

4       Invalid input parameters.

Failed to overwrite the file because a file with the same name
5
already exists and "writeType":2 is specified.

Insufficient rights to the item specified in
7
the itemId parameter.
