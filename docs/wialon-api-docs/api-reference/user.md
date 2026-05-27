# user

This section describes the methods for working with users. The creation of
users is described here.

## bind_auth_service

To connect or disconnect an authentication service, use the following
request:

```http
svc=user/bind_auth_service&params={

"service":"<text>",

"token":"<text>",

"mode":<bool>,

"serviceId":"<text>",

"userId":<long>

}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| service* | Authentication service URL. |
| token* | Authentication service access token. |
| mode* | 1 to connect, 0 to disconnect. |
| serviceId* | ID from the authentication service. |
| userId | User for whom the authentication service connection/disconnection will be made. |

### Response

If the request is completed successfully, the following result is returned:

```json
{
          <auth_service>:<auth_param> /* "gmail":"john.doe@gmail.com" for google example */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

Failed to fetch the user with
7
ACL(ADF_ACL_USER_OPERATE_AS).

The request is not supported on the server, or failed to
6
connect/disconnect the authentication service.

The current user is not found, or the authentication service
4            is not supported on the server, or a wrong user was
specified.

1002         The user already exists.

## check_activation_code

To check if a specific activation code is available (unassigned), use the
user/check_activation_code method.

### Endpoint

```http
svc=user/check_activation_code&params={
      "code": <text>
}
```

### Parameters

The request must contain the code parameter, specifying the GUID of the
code you want to check.

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
     "guid": "<string>",    // GUID of the activation code.
     "tme": <number>,       // Numerical value associated with the code.
     "tma": <number>,       // Another numerical value associated withthe code.
     "tmc": <number>,       // Another numerical value associated withthe code.
     "use": <0 / 1>         // Indicates whether the code is in use (1)or not (0).
}
```

If you are the top user, all activation codes are returned. If you are not the
top user, only the codes that have been shared with you are returned.

In case the request fails, the response contains an error code.

### Error codes

Error code               Description

4                        Invalid input parameters.

6                        Internal server error.

7                        Unauthorized user or access denied.

## get_dst_time

This page is not yet available in the Wialon Help Center. Please refer to the
previous version of the API documentation to get information about the

user/get_dst_time method.

## get_items_access

To learn what access rights a user currently has to objects, use the
following request:

```http
svc=user/get_items_access&params={"userId":<long>,
                                        "directAccess":<bool>,
                                        "itemSuperclass":"<text>",
                                        "flags":<uint>}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| userId* | User ID. |
| directAccess       Return only the objects to which the user has direct | *                  access rights. |
| itemSupercla | Object type. See the list of all types here. ss* |
| flags | Flags. Return: 0x1 for combined access level, 0x2 for direct access level. |

### Response

```json
{
"<text>": /* item ID */
        {
                 "cacl":<long>,     /* combined access level */
                 "dacl":<long>      /* direct access level */
        }
}
```

Access rights are described here.

### Error codes

Error code                     Description

7                              Failed to fetch user.

## get_items_by_access

This request returns all the objects of the specified type to which the
indicated user has at least the specified access level. The request returns a
list of matching item IDs. It can be useful if you use a lot of
user/get_items_access requests.

### Request

```http
svc=user/get_items_by_access&params={

"userId":<long>,

"itemSuperclass":"<text>",
```

"reqAccess":<long>

}

### Parameters

| Parameter | Description |
| --- | --- |
| userId | User ID. |
| itemSuperclass | Object type. |
| reqAccess | Required access rights. |

### Response

{

```json
"ids":[
                 <long>,
                 <long>,
                 ...
          ]
```

}

### Error codes

Error
Description
code

Failed to fetch the current user or the specified user with
7
ACL (ADF_ACL_USER_SET_ITEMS_ACCESS).

## get_keys

To receive information about the keys used to access external cartographic
services, use the user/get_keys command.

```http
svc=user/get_keys&params={}
```

### Response

If the request has been completed successfully, the following response is
returned:

```json
{
        "<key_name>": {
                "ct":<long>,                      /* creation time
*/
                "name":<text>,                    /* key name */
                "key":<text>,                     /* key value (maybe concealed depending on the user, provider and key type) */
                "provider":<text>,                /* map provider name ("google", "here", "trimble", etc.) */
                "type":<uint>,                    /* bit-wise combination of values from the "Key types" table (see below) */
                "sites":[<text>,<text>,<text>]    /* identifiers ofsites for which the key is available */
        }
        ...
}
```

## Key types

Value          Name

1              GIS_EXT_MAP_KEY_PROTECTED

2              GIS_EXT_MAP_KEY_ROUTING

4              GIS_EXT_MAP_KEY_GEOCODING

8              GIS_EXT_MAP_KEY_DISTANCE_MATRIX

16             GIS_EXT_MAP_KEY_PUBLIC

32             GIS_EXT_MAP_KEY_SPEEDINGS

If the request hasn’t beed completed, an error code is returned.

### Error codes

Error code             Description

1                      Invalid or obsolete request SID.

4                      Invalid request parameters.

6                      Internal server error.

7                      Unauthorized user.

## get_locale

You can get the date and time format and the first week day options using
the user/get_locale method.

```http
svc=user/get_locale&params={"userId":<long>}
```

### Parameters

The required parameters are marked with an asterisk (*).

Param                            Description

userId*                          User ID.

### Response

If the settings have never been changed using
the user/update_locale request, then a blank object is returned:

```json
{}
```

If the settings have been changed, then the response will be the following:

```json
{
     "fd":"<text>",     /* date and fime format */
     "wd":<uint>      /* the 1st week day: 1 - Monday, 7 - Sunday */
}

     For more information about the date and time format,
     see /render/set_locale.
```

### Error codes

Error
Description
code

Failed to fetch the user with ACL
7
(ADF_ACL_ITEM_VIEW_PROPERTIES).

## get_unit_codes

To fetch the activation codes available to you, use the
user/get_unit_codes method.

### Endpoint

```http
svc=user/get_unit_codes&params={}
```

### Parameters

This method doesn’t require any parameters.

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "guid": "<string>",       // GUID of the activation code.
    "uid": "<unit_id>",       // ID of the unit.
    "tmc": "<created_at>",    // Creation timestamp.

    "ttl": "<time_to_live>",   // Activation code lifetime.
    "tma": "<matched_at>",     // Match timestamp.
    "tme": "<expires_at>",     // Code expiration time.
    "shd": []                  // Array containing IDs of the users the code is shared with.
}
```

If you are the top user, all activation codes are returned. If you are not the
top user, only the codes that have been shared with you are returned.

In case the request fails, the request contains an error code.

### Error codes

Error code             Description

6                      Internal server error.

7                      Unauthorized user or access denied.

## get_video_units

This request is used only for Wialon Local. It returns a list of units with
available live stream.

### Request

```http
svc=user/get_video_units&params={}
```

### Response

[

```json
{
      "id":<long>,
      "name":"<text>",
      "unique_id":"<text>",
      "hw_type":"<text>",
      "video_uri":"<text>",
      "cameras":"<text>",
      "connected":<int> //1 - connected, 0 - disconnecte
```

d

```json
"icon_uri":"<text>",
"cmds":[
                 {
                           "id":<long>,
                           "n":"<text>", //command na
```

me

```json
"c":"<text>", //real comma
```

nd name

```json
"l":"<text>", //real comma
```

nd link type

```json
"p":"<text>", //real comma
```

nd parameter

```json
"a":<long>, //command ACL
"f":<uint>, //command flag
```

s

```json
"ct":<long>, //create time
"mt":<long> //modification
```

time

```
                       },
                       ...
                 ]
},
...
```

]

### Error codes

Error code       Description

7                The host is not running Wialon Local, or access denied.

14               Video service unavailable.

## send_sms

To send an SMS, use the following method:

```http
svc=user/send_sms&params={"phoneNumber":"<text>",
                            "smsText":"<text>"}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| phoneNumber* | Phone number. |
| smsText* | Message text. |

### Response

```json
{
          "hash":"<text>" /* returns an SMS GUID if sending is succe

ssful */
}
```

### Error codes

Error code       Value

6                Error sending SMS, or the user can't send SMS.

4                Incorrect parameter.

## share_billing_code

You can share activation codes with users who are lower in the hierarchy. To
do this, use the user/share_billing_code method.

Prerequisites
-
To share an activation code, the following prerequisites must be met:

The user with whom you want to share the code must have dealer
rights.

The code must not be already shared with a user from another
branch of the hierarchy.
The code must not be already assigned to any unit.

When sharing activation codes, consider the following details:

A code shared with a lower-level user is automatically shared with users
higher in the same branch of the hierarchy.

You can’t share the same activation code with users from different
branches of the hierarchy.

If dealer rights are revoked from an account, any shared activation
codes are automatically unshared.

### Endpoint

```http
svc=user/share_billing_code&params={
      "userId": <long>,
      "code": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| userId | ID of the user with whom the activation code should be shared. |
| code | Activation code to be shared. |

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "result": "success"
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
Code

1              Invalid input parameters.

2              The Activation codes module is not enabled.

3              Invalid source user.

The target user doesn’t have dealer rights or the
4
Manage access codes access right.

5              Invalid target user.

6              The code is not shared with the source user.

7              The code has already been shared.

8              The code is assigned to a unit.

9              Internal error.

## unshare_billing_code

To revoke sharing of an activation code with a specific user and their
subordinate, use the user/unshare_billing_code method.

### Endpoint

```http
svc=user/unshare_billing_code&params={
      "userId": <long>,
      "code": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| userId | ID of the user with whom the activation code should no longer be shared. |
| code | The activation code to be unshared. |

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
{
    "result": "success"
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
Code

1            Invalid input parameters.

2            The Activation codes module is not enabled.

3            Invalid source user.

The target user doesn’t have dealer rights or the
4
Manage access codes access right.

5            Invalid target user.

6            The code is not shared with the source user.

7            The code has already been shared.

9            Internal error.

## update_auth_params

To change two-factor authentication settings, use the following method:

```http
svc=user/update_auth_params&params={"userId":<long>,
                                           "type":<int>,
                                           "phone":"<text>"}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| userId* | User ID. |
| type* | Type (0 for none, 1 for email, 2 for SMS ). |
| phone | Phone number (if type:2). |

### Response

```json
{
    "type":<uint>,
    "phone":"<text>"
}
```

### Error codes

Error
Description
code

Failed to fetch user with ACL
7           (ADF_ACL_ITEM_EDIT_PROPERTIES), or user not found, or
incorrect parameters provided.

6           Failed to set new authentication parameters.

## update_hosts_mask

To set or update the user host mask, use the following method:

```http
svc=user/update_hosts_mask&params={"userId":<long>,
                                      "hostsMask":"<text>"}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| userId* | User ID. |
| hostsMask* | Host mask. |

### Response

```json
{
         "hm":"<text>"   /* host mask */
}
```

### Error codes

Error
Description
code

Failed to fetch the user with ACL
7
(ADF_ACL_USER_EDIT_FLAGS).

6              Failed to update the host mask.

## update_item_access

To give a user access rights to an item, use the method
user/update_item_access:

```http
svc=user/update_item_access&params={"userId":<long>,
                                        "itemId":<long>,
                                        "accessMask":<long>}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| userId* | User ID. |
| itemId* | Item ID. |
| accessMask* | Access mask. See here. |

### Response

```json
{}      /* an empty object if the execution is successful, if not,
an error code */
```

### Error codes

Error
Description
code

Failed to fetch the user with ACL
7          (ADF_ACL_USER_SET_ITEMS_ACCESS), or the user doesn’t
have rights to edit this object.

6          Failed to update access to the object.

## update_locale

To set the date and time format and the first week day options, use the
following method:

```http
svc=user/update_locale&params={"userId":<long>,
                                "locale":
                                            {
                                                "fd":"<text>",
                                                "wd":<ubyte>
                                            }
}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| userId* | User ID. |
| Date and time format. | fd* See here. |
| First week day: | wd*                             1 for Monday; 7 for Sunday. |

### Response

{

```json
"locale":
            {
                "fd":"<text>",       /* date and time format */
                "wd":<uint>      /* first week day: 1 for Monday, 7
```

for Sunday */

```
}
```

}

### Error codes

Error
Description
codes

Failed to fetch user with ACL
7                 (ADF_ACL_ITEM_VIEW_PROPERTIES), or incorrect
parameters provided.

6              Failed to update locale.

## update_password

To update a user’s password, use the following method:

```http
svc=user/update_password&params={"userId":<long>,
                                     "oldPassword":<text>,
                                     "newPassword":<text>}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| userId* | User ID. |
| oldPassword* | Old password. |
| newPassword* | New password. |

### Response

```json
{}       /* an empty object if the execution is successful; if not,
an error code */
```

### Error codes

Error
Description
code

The user wasn't found, or the current user doesn't have
7           rights to change the specified user, or the user's password
is immutable.

The password doesn't match security requirements, or
6           failed to update the password, or the current user wasn't
found.

## update_user_flags

To set user flags (additional properties), use the method
user/update_user_flags:

```http
svc=user/update_user_flags&params={"userId":<long>,
                                       "flags":<uint>,
                                       "flagsMask":<uint>}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| userId* | User ID. |
| flags* | Setting flags. See below. |
| flagsMask* | Mask which determines what bits will be changed. |
| The user setting flags are as follows: |  |
| Value | Description |
| 0x01 | User disabled. |
| 0x02 | Can't change password. |
| 0x04 | Can create items. |
| 0x10 | Can't change settings. |
| 0x20 | Can send SMS. |
| 0x40 | Administrator. |

## Example of using the mask and flags

We need to allow a user to change their password (0x02), forbid to change
the settings (0x10), and leave all the other flags without changes. In this
case, the mask will be 0x2+0x10=0x12. The flag 0x02 must be
removed, and the flag 0x10 must be set, therefore, the parameter flag
will be 0x10.

### Response

```json
{
        "fl":<uint>       /* flags */

}
```

### Error codes

Error
Description
code

6           Failed to update flags.

Failed to fetch the user with ACL
7           (ADF_ACL_USER_EDIT_FLAGS), or failed to fetch the user's
creator, or incorrect flags were provided.

## update_user_notification

To send an online notification to a user, use the command
user/update_user_notification.

## Creation

```http
svc=user/update_user_notification&params={

"itemId":<long>, /*required*/

"callMode":"<text>", /*required*/

"h":"<text>", /*required*/

"d":"{ /*required*/

\"body\":\"<text>\",

\"head\":{

\"c\":<uint>,

\"fs\":\"<text>\"

},

\"multiple\":<int>

}",

"s":"<text>", /*required*/

"ttl":<uint> /*required*/

}
```

## Deletion

```http
svc=user/update_user_notification&params={

"itemId":<long>, /*required*/

"id":<long>, /*required*/

"callMode":"<text>", /*required*/

}
```

### Parameters

The required parameters are marked with an asterisk (*).

## Creation parameters

| Name | Description |
| --- | --- |
| itemId* | User ID. |
| callMode | Action type (must be "create" for creation). * |
| h* | Subject. |
| d* | Message text settings. |
| body* | Text. |
| с* | Colour, RGB. |
| fs* | Font size. |
| multiple | Multiple activation: 1 - yes, 0 - no. * |
| s* | Sender. |
| Lifetime (UTC). When the lifetime expires, the notification | ttl* will be deleted. |

## Deletion parameters

| Name | Description |
| --- | --- |
| itemId* | User ID. |
| id* | Notification ID. |
| callMode* | Action type (must be "delete" for deletion). |

#### Important

If the ttl parameter indicates a date in the past, the
notifications trigger only online (not stored on the server).
The ttl parameter is a date in milliseconds from January 1,
1970.

### Response

Response to creation:

```json
[
        <long>,            /* notification ID */
        {
                  "id":<long>,         /* notification ID */
                  "t":<uint>,          /* lifetime (UTC) */
                  "d":"<text>",        /* message text settings*/
                  "h":"<text>",        /* subject */
                  "s":"<text>"         /* sender */
        }
]
```

Response to deletion:

```json
[
        <long>,            /* notification ID */null

]
```

### Error codes

Error
Description
code

Failed to fetch user with ACL
7
(ADF_ACL_ITEM_EDIT_OTHER).

6               Failed to create/delete the notification.

4               Incorrect mode (must be "create" or "delete").

## verify_auth

The user/verify_auth command is used to receive a verification code to
the specified address. If the address is valid, the code is sent to it and an
empty string is returned in the response. To complete two-factor
authentication and verify the code, use the verify_code request.

```http
svc=user/verify_auth&params={"userId":<long>,
                                "type":<int>,
                                "destination":"<text>"}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| userId* | User ID. |
| type* | Address type (0 for sms, 1 for email). |
| destination* | Email or phone number. |

### Response

```json
{ }
```

## Error code

Error
Description
code

Failed to fetch user with ACL
7              (ADF_ACL_ITEM_EDIT_PROPERTIES), or incorrect
parameters provided

6              Failed to send the authentication code.

## verify_code

The user/verify_code request is used for two-factor authentication. The
request should contain the code received by email or SMS after sending
the user/verify_auth command.

```http
svc=user/verify_code&params={
         "userId":<long>,
         "code":<long>
}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| userId* | The ID of the user. |
| The code received by email or SMS after sending the | code* user/verify_auth command. |

### Response

If the request is completed successfully, an empty response is returned.

```json
{ }
```

Otherwise, an error code is returned.

### Error codes

| Code | Description |
| --- | --- |
| Invalid parameters specified, user not found, or code TTL | 4 expired. The code is valid for 2 hours. |
| The maximum number of code entry attempts has been | 1006 exceeded. |

## Other methods

This section describes the dynamic requests that you can send to the
server.

## avl_evts

The avl_evts request returns information about the events that have
occurred since the last execution of this request.

```http
http://<host>/avl_evts?sid="<text>"
```

### Parameters

| Name | Description |
| --- | --- |
| sid | Session ID. |

### Response

```json
{
        "tm":<uint>,    // server time

        "events":[           // events
                   {
                             "i":<long>,          // item ID
                             "t":"<text>",        // event type: m - message, u - update, d - delete
                             "d":{                // event description, depends on the event type...
                             }
                   }
        ]
        "sensors": [
        {
               "i": <uint>,          // Unit ID
               "d": {                // Sensor data object
                   "<sensor_id>": {
                        "value": <double|text>,          // Raw sensor value
(numeric or text)
                        "format": {
                             "value": <text>,            // Formatted sensorvalue
                             "custom_value": <text> // Custom label from the "Intervals and colors" setting (for text sensors)
                        },
                        "text_value": <text>             // Present only fortext sensors
                   }
               }
        }
    ]
}
```

The sensors field contains calculated sensor values for units that have
received new messages since the last avl_evts request. This field provides
real-time sensor value updates without requiring separate sensor
calculation requests.

If no units have new sensor values, the sensors field returns an empty
array.

Each object in the array represents one unit (identified by i - unit ID).
The d object contains sensor data, where keys are sensor IDs.

## Sensor value formats

Sensor value formats in the response depend on whether it is a text sensor
or a numeric one. Text sensors include custom sensors with the Text
parameters option enabled, and sensors of the Driver assignment,
Trailer assignment, and Passenger sensor types.

Numeric analog
Parameter                                       Text sensor
sensor

Contains the raw
numeric value (for
Contains the text value
value            example, 16.749812) or
(for example, "Active").
-348201.3876 if no data
has been received.

Contains the formatted
value with units (for          Duplicates the
format.value     example, "0 km", "62.15        text_value (for example,
°F") or "---" if no data       "Active").
has been received.

Contains the custom
text defined in the
format.custo     Not included in the
Intervals and colors
m_value          response.
setting (for example,
"Device is active").

Contains the text value
Not included in the
text_value                                      or "---" if no data has
response.
been received.

## avl_render

To get a tile which contains information about all the enabled graphic
layers, use the following request:

```http
http://<host>/avl_render/<x>_<y>_<z>/<sid>.png
```

You can find an example of this request in the sample messages.

### Parameters

| Name | Description |
| --- | --- |
| x | X-coordinate of the tile. |
| y | Y-coordinate of the tile. |
| z | Zoom. |
| sid | Session ID. |

```json
"adfurl":<uint> /* a specific variable used to avoid browser caching by changing the <uint> value in the session. */
```

The tile coordinates are calculated according to the concept described
here. Zoom tiles for Webgis are from 17 to z.

## Tile size

The default tile size is 256*256. In order to change the tile size, you may
use the render/set_locale request with the density parameter.

### Error codes

Error code                   Description

304                          Not modified.

503                          Service unavailable.

### Response

Returns a PNG image.

## avl_zone_image

To get the image of a geofence, use the following request:

```http
http://<host>/avl_poi_image/<rid>/<id>/<max_border>/<any.png>
```

### Parameters

| Name | Description |
| --- | --- |
| rid | Resource ID. |
| id | Geofence ID. |
| max_bor      Maximum image size (from 16 to 256 pixels, | der          recommended: 32). |
| v | Allow SVG format. |
| any | Any value (optional). Specified if it is necessary to download the image instead of using the cached value. |

### Response

Returns the image in the PNG or SVG format.

## address (gis_geocode)

Wialon allows determining coordinates by address as well as determining
the address by coordinates. To get the address knowing the coordinates,
use the following request:

```http
https://geocode-maps.wialon.com/<host>/gis_geocode?coords=[{"lon":
<double>,"lat":<double>}]&city_radius=<uint>&dist_from_unit=<uint>&txt_dist="<text>"&flags=<uint>&uid=<long>&gis_sid="<text>"&search_provider="<text>"
```

The is usually hst-api.wialon.com.

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| coords* | Array of coordinates [{"lon":<double>,"lat":<double>}]. |
| city_rad    Minimum city radius, km. | ius         If no city is found within the maximum distance from the unit (the following option), the address will be associated with another city. In this parameter, you can specify the |
| minimum size of a city that should be used to form the | address. This helps to exclude small cities from addresses. |
| m_unit | Maximum distance from the unit, km. If the unit is located near the road and there is a city, town, dist_fro or village within the indicated distance, then the road name and the distance to this city will be shown in the address line. |
| txt_dist | Units of measurement for the maximum distance from the unit. |
| flags* | Flags of the output format (see below). |
| uid | ID of the current user. Deprecated, always use gis_sid. |
| gis_sid* | Unique ID of the user session. |
| search_ | Provider name. Possible values of search_provider are provide google, sygic, yandex, here, trimble. r* |
| lang | Language. |
| house_ | If the nearest address is a street, a house is searched for at a distance of house_detect_radius (25 meters by default) in order to specify the location on this street if possible. If the detect_ house is found and the street of the house coincides with radius the street where the object was found, the house is taken as the address. Otherwise, only the street is taken. |
| The default address format is: 45321 (street, house, city, region, country). | You can change it using the digits from 1 to 5: |
| Digit | Description |
| 1 | Country |
| 2 | Region |
| 3 | City |
| 4 | Street |
| 5 | House |
| For formatting use any of these digits five or fewer times. This output | format is placed into flags according to the following algorithm: any digit is specified by 3 bits, beginning from bit 31. It means that the maximum quantity of the involved bits equals to 15 (from 31 to 17). |
| Format | Decimal        Binary                       Result |
| 0 100 101 011 010 | 12552110                                    Street, house, city, 45321                     001 08                                          region, country. 0000000000000000 |
| 0 100 101 000 000 | 12415139 45                        000                          Street, house. 84 0000000000000000 |
| 0 011 011 011 011 | 92032204                                    City, city, city, 33333                     011 8                                           city, city. 0000000000000000 |

## Additional flags

Value                  Description

512                    Return MGRS data.

### Error codes

Error code             Description

1                      Invalid session.

4                      Wrong input parameters.

6                      Unknown error.

7                      Access denied, unknown provider.

### Response

```json
["<text>"]       /* array of addresses */
```

## apps (apps/list)

To get the list of available apps, use the following request:

```http
svc=apps/list&params={"manageMode":1,"filterLang":""}
```

### Parameters

You can use the following optional parameters in the request:

| Name | Description |
| --- | --- |
| manageMode | 1 - flag for billing data. |
| filterLang | Filter by language. |

### Response

If the request is completed successfully, the following response is returned:

```json
{"name":"<text>", /* app name */
"description":"<text>", /* app description */
"url":"<text>", /* app url */
"flags":<uint>, /*flags */
"sortOrder":<uint>, /*sort type */
"serviceName":"<text>", /* service name*/
"id":<uint>, /* app ID */
"langs":"<text>", /* app languages*/
"requiredServicesList":"<text>", /* required services */
"billingPlans":"<text>", /* required billing plans*/}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

Access denied (unknown WDC_ROOT, unknown cluster for
7
the user, billing check failed for the user).

## avl_driver_image

To get the image of a driver or trailer, use the following request:

```http
http://<host>/avl_driver_image/<rid>/<did>/<max_border>/<any.png>
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| rid* | Resource ID. |
| did* | Driver ID or trailer ID. |
| max_borde       Maximum image size (from 16 to 256 pixels, | r*              recommended: 32). |
| flags | Flags. Must contain 0x02 to get the trailer image. |

### Response

If the request is completed successfully, an image in the PNG format is
returned. Otherwise, the response is an error code.

### Error codes

Error code                  Description

404                         Not found.

304                         Not modified.

503                         Service unavailable.

416                         Invalid range requested.

## avl_hittest_pos

To get information about any item on a graphic layer by its coordinates, use
the following request:

```http
http://<host>/avl_hittest_pos?sid="<text>"&lat=<double>&lon=<double>&scale=<uint>&radius=<double>&layerName="<text>"
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| sid* | Session ID. |
| lat* | Latitude. |
| lon* | Longitude. |
| scale | Zoom: 0-17. |
| radius* | Search radius in degrees (like coordinates). |
| e | layerNam Layer name. |
| flags | Layer flags (see below). By default, all possible bits are set. |

### Flags

| Flag | Description |
| --- | --- |
| 0x10 | Use information from the marker layer. |
| 0x20 | Use information from the message layer. |
| 0x40 | Use information from the shape layer. |
| To get marker (POI) information, specify the POI icon | coordinates and any radius. In the case of a geofence or a circle-shaped marker, specify the coordinates within its shape and any radius. |

### Response

For messages:

{

```json
         "type":"msg",              // Result type.
         "currMsg":{                // Current message....
         },
         "prevMsg":{                // Previous message....
         },
         "sensors": {           // Sensor values.

             "<sensor_id>": {
                 "value": <double|text>,        // Sensor value.
                 "format": {
                     "value": <text>            // Formatted sensor value with units of measurement.
                 }
             }
        },
        "msgIndex":<uint>,        // Current message index.
        "unitId":<long>,          // Unit ID.
        "mileage":<double>,       // Mileage.
        "layerName":"<text>"      // Layer name.
}
```

The formats of the current and previous messages are described here.

For markers:

```json
{
        "type":"marker",          // Result type.
        "lat":<double>,           // Latitude.
        "lon":<double>,           // Longitude.
        "info":[{}],              // Information about the marker: depends on the marker type.
        "layerName":"<text>",     // Layer name.
        "marker":"<text>"         // Additional information about the marker if available.
}
```

For geofences:

```json
{
        "type":"shape",           // Result type.
        "lat":<double>,           // Latitude.
        "lon":<double>,           // Longitude.

         "layerName":"<text>",     // Layer name.
         "shape":"<text>"          // Information about the geofence,
for example, its name.
}
```

## avl_hittest_time

When the track layer is rendered, you can get the message closest to the
specified time (used in the Track player, Track analysis tools, etc.). The
time value should be within the time interval for which the track layer is
rendered. To get such a message, use the request:

```http
http://<host>/avl_hittest_time?sid="<text>"&unitId=<uint>&layerName="<text>"&time=<uint>&revert=<bool>
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| sid* | Session ID. |
| unitId* | Unit ID. |
| layerNa | Layer name. me* |
| time* | Time. |
| revert | Search order. The value false stands for the direct order, the value true for the reverse one. |
| anyMsg | Process all messages to find the result. True - all messages, false - the messages marked with the flag 0x1. |

### Response

```json
{
        "currMsg":{               /* current message */...
        },
        "prevMsg":{               /* previous message */...
        },
        "index":<uint>,           /* current message index */
        "layerName":"<text>"      /* layer name */
}
```

The formats of the current and previous messages are described here.

## avl_item_image

To get the image of a unit, use the following request:

```http
http://<host>/avl_item_image/<item_id>/<max_border>/<any.png>
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| item_id* | Unit ID. |
| max_bor      Maximum image size (from 16 to 256 pixels, | der          recommended: 32). |
| any | Any value. Specified if it is necessary to download the image instead of using the cached value. |

### Response

Returns an image in the PNG format.

## avl_msg_photo

To get a photo from a message, use the following request:

```http
http://<host>/avl_msg_photo?sid=<sid>&layerName="<text>"&msgIndex=
<uint>&time=<uint>&unitIndex=<uint>&saveMode=<uint>
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| sid* | Session ID. |
| layerName | Layer name. * |
| msgIndex* | Message index. |
| time* | Time. |
| unitIndex* | Unit index. |
| saveMode | Used for saving an image to a file on the user's device, 1 - active. |

### Response

Returns a photo.

## coordinates_intelli (gis_searchintelli)

This search is convenient because you don’t need to specify whether you
are searching for a street, country, house, etc. One phrase with an arbitrary
word order is enough for this search. This request returns results in the
default format: the formatted address path, coordinates, and the map
name. To get coordinates by specifying the address in any custom format,
use the following request:

```http
https://search-maps.wialon.com/<host>/gis_searchintelli?phrase="<text>"&count=<uin t>&indexFrom=<uint>&uid=<long>...
```

The is usually hst-api.wialon.com.

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| phrase* | Search phrase. |
| count* | Number of output results. |
| indexFrom | Sequence number of the first result. |
| uid | Current user ID. Deprecated, always use gis_sid. |
| gis_sid* | Unique ID of the user session. |
| search_pro         Provider name. Possible values of search_provider | vider*             are google, sygic, yandex, here, trimble. |
| flags | Search and format flags (see below). |
| searchFlags | Additional search flags (see below). * |
| lang | Language. |
| vant | allow_irrele 1 - active, allow irrelevant result. |

## Search flags

| Flag | Description |
| --- | --- |
| 0x100 | Dump the path in the result. |
| 0x200 | Dump the map name in the result. |
| 0x400 | Dump the map coordinates in the result. |
| 0x800 | Do not create JSON. Return results as a list of objects. |

### Flags

| Flag | Description |
| --- | --- |
| 0x0 | Search country. |
| 0x1 | Search region. |
| 0x2 | Search city. |
| 0x3 | Search street. |
| 0x4 | Search house. |
| 0x100 | Add fields with a formatted address path to the result. |
| 0x200 | Add the map name to the result. |
| 0x400 | Add coordinates to the result. |

### Response

[

```json
{
          "items":[
                     {
                            "name":"<text>",                       /*
```

name of the search item */

```json
"map":"<text>",           /* map nam
```

e */

```json
                                     "x":<double>,             /* longitude */
                                     "y":<double>,             /* latitude */
                                     "path":"<text>",                      /*part of the address path, excluding the part placed in "name" */
                                     "formatted_path":"<text>"             /*address string formatted according to the flags */
                         }
                 ],
                 "country":"<text>",           /* country */
                 "region":"<text>",            /* region */
                 "city":"<text>",                     /* city */
                 "street":"<text>",            /* street */
                 "house":"<text>",                    /* house */
                 "flags":<uint>,               /* flags */
                 "more":<uint>                 /* additional results: 0 -no, 1 - yes */
        }
]
```

The flags that show how detailed the result is:

| Flag | Description |
| --- | --- |
| 0x0 | Country |
| 0x1 | Region |
| 0x2 | City |
| 0x3 | Street |
| 0x4 | House |

### Error codes

Error code         Description

1                  Invalid session.

4                  Wrong input parameters.

6                  Unknown error.

7                  Access denied, unknown search provider.

## coordinates_simple (gis_search)

To get the coordinates by specifying the address, use the following request:

```http
https://search-maps.wialon.com/<host>/gis_search?country="<text>"&region="<text>"&city="<text>"&street="<text>"&flags=<uint>&count=<uint>&indexFrom=<uint>&uid=<long>
```

The is usually hst-api.wialon.com.

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| country | Name of a country or its part. |
| region | Name of a region or its part. |
| city | Name of a city or its part. |
| street | Name of a street or its part. |
| flags* | Search and format flags. See the description below. |
| count* | Output result count. |
| indexFrom | Sequence number of the first result. |
| searchFlags* | Additional search flags. See the description below. |
| gis_sid* | Unique ID of the user session. |
| uid | Current user ID. Deprecated, always use gis_sid. |

## Search flags

| Flag | Description |
| --- | --- |
| 0x100 | Dump the path in the result. |
| 0x200 | Dump the map name in the result. |
| 0x400 | Dump the map coordinates in the result. |
| 0x800 | Do not create JSON. Return results as a list of objects. |

### Flags

| Flag | Description |
| --- | --- |
| 0x0 | Search country. |
| 0x1 | Search region. |
| 0x2 | Search city. |
| 0x3 | Search street. |
| 0x4 | Search house. |
| 0x100 | Add fields with a formatted address path to the result. |
| 0x200 | Add the map name to the result. |
| 0x400 | Add coordinates to the result. |
| Format flags are described here. |  |

### Error codes

Error code         Description

1                  Invalid session.

4                  Wrong input parameters.

6                  Unknown error.

7                  Access denied, unknown search provider.

### Response

```json
{
        "items":[          /* array of results */
                 {
                           "name":"<text>",                 /* name ofthe search item*/
                           "map":"<text>",          /* map name */
                           "x":<double>,            /* longitude */
                           "y":<double>,            /* latitude */
                           "path":"<text>",                 /* part ofthe address path, excluding the part placed in "name" */
                           "formatted_path":"<text>"        /* addressstring formatted according to the flags */
                 }
        ],
        "more":<uint>      /* additional results: 0 - no, 1 - yes */
}
```

## gis_render

To get a tile of a WebGIS map, use the following request:

```http
https://<host>/gis_render/<x>_<y>_<z>/<uid>/<tile_name>.png?density=...
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| x* | X-coordinate of the tile. |
| y* | Y-coordinate of the tile. |
| z* | Zoom. |
| uid* | Current user ID. Deprecated, always use gis_sid. |
| density | Tile size. |
| gis_sid* | Unique ID of the user session. |
| f* | Flags: 0x200 - zoom Google Maps. |
| Tile coordinates are calculated according to the concept described here. | Zoom tiles for Webgis from 17 to z. |

## Density

The parameter is optional. The default tile size is 256*256.

Value                 Tile size                         Ratio

1                     256*256                           1

2                     384*384                           1.5

3                     512*512                           2

4                     768*768                           3

5                     1024*1024                         4

### Error codes

Error code                     Description

500                            Internal server error.

401                            Access denied.

304                            Not modified.

### Response

Returns an image in the PNG format.

## Code examples

In this section, you can find examples of how to use API methods. In the
examples, https://hst-api.wialon.com is used as the Wialon Hosting request
server, and wialon_test is used as a demo login. To test an example, copy
it to the address bar of your browser. Note that the session ID is a required
parameter which you can obtain from a successful login operation.

## Login and logout

To execute any request in Wialon, you must sign in and get a session ID.

## Login

To sign in, use the token/login method. In the example below, this method
is used to sign in to https://hst-api.wialon.com.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=token/login&params={
                 "token":"2fe8024e0ab91aa6c8ed82717b71bddcECDC36235
```

8DF7D90986F5173D405CD0D42DE7B38"

```
}
```

Response example:

{

```json
"host": "212.98.173.107",
"eid": "d1cb60897768780f846df7ab2400eb5f",
"tm": 1358415984,
"user": {
     "nm": "wialon_test",
     "cls": 1,
     "id": 50935,
     "prp": {
          "addr_provider": "map_visicom",
          "cfmt": "0",
          "city": "Mexico",
          "dst": "-1",
          "fpnl": "monitoring",
          "language": "ru",
          "show_log": "0",
          "tz": "134232128",
          "user_settings_hotkeys": "1",
          ...
     },
     "token": "{"app":"Wialon Hosting","ct":1443682655,"at":144
```

3682655,"dur":2592000,"fl":-1,"p":"{}","items":[]}",

```json
"th": "2fe8024e0ab91aa6c8ed82717b71bddcECDC362358DF7D90986
```

F5173D405CD0D42DE7B38",

```json
        "crt": 0,
        "bact": 50936,
        "fl": 6,
        "hm": "",
        "uacl": 2097795
   },
   "classes": {
        "avl_hw": 4,
        "avl_resource": 3,

         "avl_retranslator": 7,
         "avl_route": 6,
         "avl_unit": 2,
         "avl_unit_group": 5,
         "user": 1
    },
    "features": {
         "unlim": 1,
         "svcs": {
             ...
         }
    }
}
```

For further operations, the session ID from the eid field is required. In the
provided example, it is d1cb60897768780f846df7ab2400eb5f.

## Logout

To stop working with Wialon and log out of the system, deactivate the
session using the core/logout method. For example:

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/logout&params
={}&sid=d1cb60897768780f846df7ab2400eb5f
```

Response example:

```json
{
         "error":0
}
```

Such a result indicates that you have signed out successfully.

The parameters of this request and the returned value are described on the
core/logout page.
