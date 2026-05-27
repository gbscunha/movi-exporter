# core

This section describes the basic Wialon methods, such
as search_items, reset_password_perform, logout, etc.

## batch

The batch function is used to execute several methods in one request.

```http
svc=core/batch&params=[
                            {
                                    "svc":"<text>",
                                    "params":{}
                            }
                        ]
```

The request can also be as follows:

```http
svc=core/batch&params={
                            "params": [{
                                    "svc":"<text>",
                                    "params":{}
                            }],
                            "flags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| svc | Command name. |
| s | param Parameters. |
| One of the following: |  |
| flags | 0 — execute all commands (by default); 1 — stop batch if an error is returned by some command. |

## Returned result

```json
[
         {       /* object with data if there are no errors */...
         },
         {       /* error code if an error has occurred */
                 "error":<int>
         },
         ...
]

      If the flags parameter is set to 1 and an error has occurredwhile executing one of the commands, all the methods thatfollow this one return the error code 10.
```

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | The returned result is too large. |
| 4 | Wrong input parameters. |

## check_accessors

The check_accessors function is used to get the list of access rights to the
units of subordinate users.

svc=core/check_accessors&params={"items":[<long>],

```json
"flags":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| items | The array of unit IDs. |
| The flag used for adding the dact parameter in the returned | result: |
| flags               1 — add; | 0 — don't add. |

## Returned result

{
"<unit_id>": {                       /* unit ID */
"<acc_id>": {                /* user ID */

```json
"acl": <long>,               /* inherited unit access r
```

ights that are superimposed by a mask over direct access rights; i
f something is prohibited according to the inherited access right
s, it is prohibited according to the resulting access rights as we
ll */

```json
"dacl": <long>               /* if the flags:1 is set,
```

the access rights to the unit are direct (from the unit owner) */

```
      },
      ...                          /* other user IDs (if any) */
},
...                                /* other unit IDs (if requested)
```

*/

```
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 7 | Failed to fetch the user. |
| 4 | Wrong input parameters. |

## check_items_billing

The check_items_billing function is used to check the current user’s access
rights to items.

```http
svc=core/check_items_billing&params={"items":[<long>],
                                               "accessFlags":<long>,
                                               "serviceName":"<text>"}
```

During the request processing, both available services and access rights to
items are checked. If, for example, a user has access right to create reports
in some resource, but has already reached the limit of allowed report
templates according to the cost table, the resource is not shown in the
result array.

### Parameters

| Name | Description |
| --- | --- |
| items | The array of item IDs. |
| accessFlags | Access flags (described below). |
| serviceName | The name of the service (see the get_account_data page). |

## Returned result

```json
[
        <long>             /* array of items that the user can access
*/
]
```

Possible error codes:

| Code | Description |
| --- | --- |
| 4 | Wrong input parameters. |

## Access flags

## General

| Flag | Description |
| --- | --- |
| 0x0001 | View object and its basic properties. |
| 0x0002 | View detailed object properties. |
| 0x0004 | Manage access to this object. |
| 0x0008 | Delete object. |
| 0x0010 | Rename object. |
| 0x0020 | View custom fields. |
| 0x0040 | Manage custom fields. |
| 0x0080 | Edit not mentioned properties. |
| 0x0100 | Change icon. |
| 0x0200 | Request reports and messages. |
| 0x0400 | Edit ACL-propagated objects. |
| 0x0800 | Manage object log. |
| 0x1000 | View admin fields. |
| 0x2000 | Manage admin fields. |
| 0x4000 | View and download files. |
| 0x8000 | Upload and delete files. |

## Units and unit groups

| Flag | Description |
| --- | --- |
| Edit connectivity settings (device type, unique ID, | 0x0000100000   phone, access password, message validity filtration). |
| 0x0000200000 | Create, edit, and delete sensors. |
| 0x0000400000 | Edit counters. |
| 0x0000800000 | Delete messages. |
| 0x0001000000 | Send commands. |
| 0x0002000000 | Manage events. |
| View connectivity settings (device type, unique ID, | 0x0004000000   phone, access password, message validity filtration). |
| 0x0010000000 | View service intervals. |
| 0x0020000000 | Create, edit, and delete service intervals. |
| 0x0040000000 | Import messages. |
| 0x0080000000 | Export messages. |
| 0x0400000000 | View commands. |
| 0x0800000000 | Create, edit, and delete commands. |
| 0x4000000000 | Edit trip detector. |
| Flag | Description |
| 0x8000000000 | Use unit in jobs, notifications, routes, retranslators. |

## Users

| Flag | Description |
| --- | --- |
| 0x100000 | Manage user’s access rights. |
| 0x200000 | Act on behalf of this user (create objects, log in, etc.). |
| Change flags for given user (allows changing the | 0x400000   additional properties of the user; see the update_user_flags function). |

## Retranslators

| Flag | Description |
| --- | --- |
| 0x100000 | Edit retranslator properties including start/stop. |
| 0x200000 | Add or remove units from retranslator, change their UIDs. |

## Resources (Accounts)

| Flag | Description |
| --- | --- |
| 0x0000000100000 | View notifications. |
| 0x0000000200000 | Create, edit, and delete notifications. |
| 0x0000001000000 | View geofences. |
| 0x0000002000000 | Create, edit, and delete geofences. |
| 0x0000004000000 | View jobs. |
| 0x0000008000000 | Create, edit, and delete jobs. |
| 0x0000010000000 | View report templates. |
| 0x0000020000000 | Create, edit, and delete report templates. |
| 0x0000040000000 | View drivers. |
| 0x0000080000000 | Create, edit, and delete drivers. |
| 0x0000100000000 | Manage account. |
| 0x0000200000000 | View orders. |
| 0x0000400000000 | Create, edit, and delete orders. |
| 0x0000800000000 | View passengers. |
| 0x0001000000000 | Create, edit, and delete passengers. |
| 0x0100000000000 | View trailers. |
| 0x0200000000000 | Create, edit, and delete trailers. |

## Routes

| Flag | Description |
| --- | --- |
| 0x0000000100000 | Edit route properties. |

## Other

| Flag | Description |
| --- | --- |
| 0xfffffffffffffff | Gives full access rights to an object. |

## check_unique

The check_unique function is used to check the uniqueness of an item.

```http
svc=core/check_unique&params={"type":"<text>",
                                 "value":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| type | Item type (user, avl_resource). |
| value | Item name. |

## Returned result

If the item is unique, the returned result is:

```json
{"result":0}
```

If the item exists, the returned result is:

```json
{"result":1}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Locker error or the limit on the number of API requests | 1003 according to a certain rule exceeded. |
| 4 | Wrong input parameters. |

## create_auth_hash

The create_auth_hash function is used to create an authorization hash.

The combination of the create_auth_hash and use_auth_hash functions
can be used instead of the duplicate function.

```http
svc=core/create_auth_hash&params={}

      The generated hash is valid within 2 minutes from themoment of its creation.
```

## Returned result

```json
{
         "authHash":"<text>"       /* authorization hash value */
}
```

Error codes:

| Code | Description |
| --- | --- |
| 9 | Failed to generate auth hash. |
| Failed to check the top level access to the token or failed to | 7 access the SDK package. |
| 1 | Failed to fetch the current user. |

## create_resource

The create_resource function is used to create new resources.

svc=core/create_resource&params={"creatorId":<long>,

```json
"name":"<text>",
"dataFlags":<uint>,
"skipCreatorCheck":<bool>}
```

### Parameters

| Name | Description |
| --- | --- |
| creatorId | The ID of the user that should be indicated as the creator of the new resource. |
| name | Resource name (4–50 characters). |
| dataFlags | The flags with the resource properties for the returned result. See the resources page. |
| A special flag. 1 — enable. The default value is 0. |  |
| You can’t create an account for a | user that has created items while he had no account. To create a skipCreatorCheck           resource for such user, use skipCreatorCheck=1. The flag is used for that purpose only. The purpose of this limitation is to protect the hierarchy. |

## Returned result

```json
{
        "item":{           /* resource created */...
        },
        "flags":<uint>     /* applied flags with properties */
}
```

The format of the item parameter is described on the resources page.

Possible error codes:

| Code | Description |
| --- | --- |
| 2014 | The selected user is the creator of some system objects. |
| 1002 | Failed to fetch the creator with the desired ID. |
| 7 | Failed to check the create_resources billing. |
| One of the following errors: |  |
| failed to fetch the creator with the desired ID; |  |
| 6             current user doesn't have the | ADF_STORAGE_USER_FLAG_ITEM_CREATOR flag; failed to create the resource because of the billing rules. |
| Wrong input parameters or the length of | 4 the name parameter is out of bounds (4–50 characters). |

## create_retranslator

The create_retranslator function is used to create a new retranslator.

```http
svc=core/create_retranslator&params={"creatorId":<long>,
                                           "name":"<text>",
                                           "config":{
                                                        "protocol":"<text
>",
                                                        "server":"<text>",
                                                        "port":<ushort>,
                                                        "auth":"<text>",
                                                        "ssl":<int>,
                                                        "debug":<int>,
                                                        "v6type":<int>
                                           },
                                           "dataFlags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| creatorI    The ID of the user that should be the creator of the | d           retranslator. |
| name | The name of the retranslator (4–50 characters). |
| config | Retranslator configuration. |
| protocol | Protocol ID (see the update_config page). |
| server | Retranslation server. |
| port | Port (for all protocols, except NIS). |
| auth | Authorization (only for NIS and Wialon IPS protocols). |
| Using SSL (for NIS): |  |
| ssl | 0 — no; |
| 1 — yes. |  |
| Using the debug mode: |  |
| debug             0 — no; | 1 — yes. |
| Using the protocol ver. 6 (only for Granit Navigator): |  |
| v6type            0 — no; | 1 — yes. |
| dataFla        Flags with the retranslator properties for the returned | gs             result (see the retranslator page). |

## Returned result

{

```json
"item":{           /* retranslator created */...
},
"flags":<uint>     /* applied flags with properties */
```

}

The format of the item parameter is described on the retranslator page.

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Failed to fetch the creator or failed to create retranslator. |
| One of the following errors: |  |
| wrong input parameters; |  |
| 4              failed to validate the configuration; | failed to create retranslator with the specified protocol (see the reason field for details). |

## create_route

The create_route function is used to create new routes.

```http
svc=core/create_route&params={"creatorId":<long>,
                                   "name":"<text>",
                                   "dataFlags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| creatorId | The ID of the user that should be the creator of the new route. |
| Name | Description |
| name | Route name (4–50 characters). |
| dataFlags | Flags with the route properties for the returned result (see the routes page). |

## Returned result

```json
{
        "item":{            /* route created */...
        },
        "flags":<uint>      /* applied flags with properties */
}
```

The format of the item parameter is described on the route page.

Possible error codes:

| Code | Description |
| --- | --- |
| 7 | Route library not loaded. |
| One of the following errors: |  |
| failed to fetch the route creator; |  |
| 6 | failed to create the route; |
| failed to check the access rights of the current user to the | route. |
| 4 | Wrong input parameters. |

## create_unit

The create_unit function is used to create new units.

```http
svc=core/create_unit&params={"creatorId":<long>,
                                "name":"<text>",
                                "hwTypeId":<long>,
                                "dataFlags":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| d | creatorI The ID of the user that should be the unit creator. |
| name | Unit name (4–50 characters). |
| d | hwTypeI Device (hardware) ID. |
| dataFlag      Flags with the unit properties for the returned result (see | s             the unit page). |

## Returned result

```json
{
        "item":{          /* unit created */...
        },
        "flags":<uint>    /* applied flags with properties */
}
```

The format of the item parameter is described on the unit page.

Possible error codes:

| Code | Description |
| --- | --- |
| The creator is a top account or the create_units billing | 7 transaction failed. |
| 6 | Failed to fetch user creator or failed to create unit. |
| 4 | Wrong input parameters. |

## create_unit_group

The create_unit_group function is used to create unit groups.

```http
svc=core/create_unit_group&params={"creatorId":<long>,
                                        "name":"<text>",
                                        "dataFlags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| creatorId | The ID of the user that should be the creator of the unit group. |
| name | The name of the unit group (4–50 characters). |
| dataFlags | Flags with the unit group properties for the returned result (see the group page). |

## Returned result

```json
{
           "item":{         /* unit group created */...
           },
           "flags":<uint>   /* applied flags with properties */
}
```

The format of the item parameter is described on the group page.

Possible error codes:

| Code | Description |
| --- | --- |
| The creator is a top account user or failed to check | 7 the create_unit_groups billing transaction. |
| 6 | Failed to fetch the creator or failed to create unit group. |
| 4 | Wrong input parameters. |

## create_user

The create_user function is used to create users.

```http
svc=core/create_user&params={"creatorId":<long>,
                                "name":"<text>",
                                "password":"<text>",
                                "dataFlags":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| d | creatorI The ID of the user that should be the new user's creator. |
| name | The name of the new user (4–50 characters). |
| d | passwor The password of the new user. |
| dataFlag      Flags with the user properties for the returned result (see | s             the user page). |

## Returned result

```json
{
        "item":{          /* user created */...
        },
        "flags":<uint>    /* applied flags with properties */
}
```

The format of the item parameter is described on the user page.

Possible error codes:

| Code | Description |
| --- | --- |
| 1002 | The user with this name already exists. |
| The creator is a top account user or failed to check the | 7 create_users billing transaction. |
| 6 | Failed to fetch the creator or failed to create user. |
| 4 | Wrong input parameters. |

## duplicate

The duplicate function is used to log in as another user. It duplicates the
active session.

```http
svc=core/duplicate&params={"operateAs":"<text>",
                             "continueCurrentSession":<bool>,
                                 "appName":"<text>",
                                 "checkService":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| The name of the user on whose behalf you want to log | operateAs      in to the system. The parameter should be empty if you want to log in as the main user. |
| n | The parameter defines whether the previous session should be continued. Possible values: continueCu rrentSessio       false (by default); true — both SIDs remain valid. |
| appName | An optional possibility to rename the app in the duplicated session. |
| checkServic    An optional possibility to validate the billing service of | e              the current user. |
| To get information about the current session without generating a new | session, use the duplicate function with the following parameter: |

```http
svc=core/duplicate&params={"restore": 1}
```

## Returned result

The format of the returned result is the same as for the login function.

Possible error codes:

| Code | Description |
| --- | --- |
| 1003 | No session. |
| Failed to fetch the subordinate user | 8         (the operateAs parameter) or failed to set the token ACLs for the new session. |
| Access denied due to the billing rules (only for | 7 the checkService parameter). |
| 1 | Invalid session. |

## export_file

The export_file function is used to export the results of searching items as
a XLSX file.

```http
svc=core/export_file&params={"spec":{
                                               "itemsType":"<text>",
                                               "propName":"<text>",
                                               "propValueMask":"<text>",
                                               "sortType":"<text>"
                              },
                              "force":<uint>,
                              "flags":<long> /* columns flags */

}

      Other parameters are described on the search_items page.
```

Flags:

Value          Description

### For the "user" itemsType

0x0001         Name.

0x0002         Creator.

0x0004         Account.

0x0008         Billing plan.

0x0010         Last visit.

0x0020         Email.

0x0040         Host.

0x0080         Authentication type.

0x0100         Phone number for two-factor authentication.

0x0200         Status.

0x0400         Permission to change the password.

0x0800        Permission to create items.

0x1000        Permission to change settings.

0x2000        Permission to send SMS.

0x4000        Time zone.

For the "avl_unit" itemsType

0x0001        Name.

0x0002        Creator.

0x0004        Account.

0x0008        Device type.

0x0010        Unique ID.

0x0020        Phone.

0x0040        Last message.

0x0080        Created.

0x0100        Custom fields.

0x0200        Groups.

0x0400        Deactivation.

For the "avl_unit_group" itemsType

0x0001        Name.

0x0002        Creator.

0x0004        Account.

0x0008        Units.

For the "avl_resource" itemsType

0x0001        Name.

0x0002        Creator.

0x0004        Parent account.

0x0008        Billing plan.

0x0010        Dealer rights.

0x0020        Units.

0x0040        Balance.

0x0080        Days.

0x0100        Status.

0x0200        Blocked.

0x0400        Activated units.

For the "avl_retranslator" itemsType

0x0001        Name.

0x0002        Creator.

0x0004         Account.

0x0008         Protocol.

0x0010         Server.

0x0020         State.

0x0040         Units for retranslation.

0x0080         Unit unique ID.

## Returned result

As a result, an XLSX file is returned.

Possible error codes:

| Code | Description |
| --- | --- |
| 5 | Failed to fetch the current user. |
| 4 | Wrong input parameters. |

## export_to_file

The export_to_file function is used to export the search results of the
Trash section to an XLSX table.

```http
svc=core/export_to_file&params={
    "sheets":[

                 {
                           "title":"<text>",
                           "rows":[
                                      ["<text>"]
                           ]
                 }
         ],
         "format":<uint>
}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| sheets* | Array of tables. |
| title* | Table title. |
| rows* | Table columns and rows. |
| format* | Table format. Specify 8 for XLSX. |

### Response

If completed successfully, returns an XLSX file.

### Error codes

| Code | Description |
| --- | --- |
| Invalid parameters provided or inappropriate format | 4         specified. The only suitable format is XLSX, that is, the request should contain "format": 8. |
| Request execution error (failed to create temporary | 5 directories and/or execute file creation method). |

## get_account_data

To get information about the settings of the account you are currently
signed in and its billing plan (billing plan name, balance, days left, available
services), use the core/get_account_data method:

```http
svc=core/get_account_data&params={
    "type": <int>,
}
```

### Parameters

The request must contain the type parameter with one of the following
values:

1, to get basic information required to estimate the state of the user
who is currently signed in.

2, to get detailed information with combined, personal and billing plan
settings.

### Response

If the request is completed successfully, the response contains either basic
or detailed information, depending on the value of the type parameter.

Basic information:

```json
{
     "parentAccountName": <text>, /* Parent account name. */
     "parentAccountId": <long>, /* Parent account GUID. */
     "parentEnabled": <int>,            /* Shows whether the parent accountis enabled. */
     "plan": <text>,                    /* Billing plan name. */
     "enabled": <int>,           /* Account state: 0 — blocked, 1 — active. */
     "switchTime": <int>,               /*   Last time of changing the "​enabled" parameter.​ */
     "created": <uint>,            /*    Creation time (UNIX time).​ */
     "flags": <uint>,                   /* Billing plan flags. */
     "balance": <text>,          /* Balance (with currency). */
     "daysCounter": <int>,              /* Day counter. */
     "services": {                 /* List of services.*/
          <text>: {              /* Service name. */
                "type": <int>,          /* Type: 1 — on demand; 2 — periodic. */
                "usage": <uint>,             /* Quantity of active resourcesin which the service is used. */
                "maxUsage": <int>, /* Maximum quantity of resources.
*/
                "cost": <text>, /* Cost table. */
                "interval": <int>, /* Reset interval: 0 — none, 1 — hourly, 2 — daily, 3 — weekly, 4 — monthly. */
                "descr": <text> /* Description. */
          },
          ...
     },
     "dealerRights": <int>,             /* Allow using dealer rights for this billing plan: 0 — no, 1 — yes */
     "subPlans":[<text>]            /* Array of subplans. */
}
```

Detailed information:

{

```json
"parentAccountName": <text>, /* Parent account name. */
"parentAccountId": <long>, /* Parent account GUID. */
"parentEnabled": <int>,        /* Shows whether the parent account
```

is enabled. */

```json
"plan": <text>,                /* Billing plan name. */
"enabled": <int>,          /* Account state: 0 — blocked, 1 — acti
```

ve. */

```json
"switchTime": <int>            /* Last time of changing the "​enabl
```

ed" parameter​*/

```json
"flags": <uint>,               /* Duplicates the same flags from t
```

he billing plan settings (see the "plan" field below). */

```json
"balance": <text>,         /* Balance (with currency). */
"daysCounter": <int>,          /* Day counter. */
"settings": {
     "balance": <double>,            /* Balance. */
     "plan":{               /* Billing plan settings. */
           "flags": <uint>,          /* Billing plan flags. */
           "blockBalance": <int>, /* Block balance. */
           "denyBalance": <int>,     /* Minimum balance required for
```

the paid services to be available. */

```json
"minDaysCounter": <int>,       /* Minimum number of days r
```

equired for the account to be enabled. */

```json
"historyPeriod": <int>,        /* History period during wh
```

ich unit messages are stored, in days (if 0 is specified here, the
storage period is unlimited). */

```json
"currencyFormat": <text>,      /* Currency format. */
"services": {          /* List of services. */
    <text>: {      /* Name. */
        "type": <int>,         /* Type: 1 — on demand; 2 —
```

periodic. */

```json
"usage": <uint>,           /* Number of used items
```

of this type. */

```json
"maxUsage": <int>      /* Maximum allowed number o
```

f items of this type. */

```json
"cost": <text>,           /* Cost table. */
"interval": <int>, /* Reset interval: 0 — non
```

e, 1 — hourly, 2 — daily, 3 — weekly, 4 — monthly. */

```json
                    "descr": <text>            /* Description. */

                     },
                     ...
               }
         },
         "personal": {                /* Account settings. */...          /* In the same format as the billing plansettings. */
         },
         "combined": {                /* Combined settings (settings related to the billing plan and account). */...          /* In the same format as the billing plansettings */
         }
    },
    "siteAccess": {
               "<service_name>":"<dns_name>",        /* Where the key is a service name and the value is a DNS name. */...
    },
    "dealerRights": <int>, /* Allow using dealer rights for this billing plan: 0 — no, 1 — yes */
    "subPlans": [<text>]       /* Array of subplans. */
}
```

You can find available values of billing plan and account flags, as well as
the list of services on the account/get_account_data page.

For further information about the structure of account and billing plan
settings, see account/update_billing_plan.

If the request fails, error code 4 is returned, indicating one of the following
issues:

the input parameters are wrong,

failed to fetch the user.

## get_hw_cmds

The get_hw_cmds function is used to get the list of commands available
for a unit or a hardware type, or to get the command templates.

```http
svc=core/get_hw_cmds&params={"deviceTypeId":<long>,
                                "unitId":<long>,
                                "template":<bool>
                                "lang":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| peId | deviceTy Hardware type ID. |
| unitId | Unit ID. |
| template | Flag. If set to 1 (on), the returned result is a JSON with the command template data. The parameter is optional. |
| lang | Flag. Translates the values of "title" and "label" values. The parameter is optional. |
| You can set only one parameter or both. The search begins with the | hardware type ID and if it fails, continues with the unit ID. If you want to omit a parameter, set it to 0. |

## Returned result

The returned result contains the list of available commands if template:0
or missing:

```json
{
                  "<text>":[              /* link type: GSM, TCP, UDP, VRT */
                               "<text>",          /* command type */...
                  ],
                  ...
}
```

If the template flag is set to 1, the command template is returned. It can
be a custom set of fields. An example of a JSON is given below:

```json
{
    "<cmd_template_name>": {                  /* name */
         "icon": <text>,                      /* icon */
         "props": [                            /* properties */
             {
                  "label":<text>,              /* property label */
                  "type":<text>,               /* type */
                  "validate":<text>,           /* validation rule */
                  "value": [                   /* key-value array */
                       {
                            "n":<text>,        /* key */
                            "v":<text>         /* value */
                       },
                       ...
                  ],
                  "default":<text>,            /* a default value (for example the I
P address port) */
                  "title":<text>,              /* title */
                  "maxlength":<uint>           /* maximum length */
             },
             ...
         ]
    },
    ...

}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Failed to fetch the current user. |
| One of the following: |  |
| wrong input parameters; | 4 failed to fetch the hardware by ID; failed to fetch the billing plan for the hardware. |

## get_hw_types

The get_hw_types function is used to get the list of available hardware
types.

```http
svc=core/get_hw_types&params={"filterType":"<text>",
                                  "filterValue":["<text>"|<uint>],
                                  "includeType":<bool>,
                                  "ignoreRename":<bool>}
```

### Parameters

All parameters are optional.

| Name | Description |
| --- | --- |
| Filter type: |  |
| name; |  |
| filterType          id; | type; feature. |
| The array of filter values (comma-delimited). The values | for different filterType can be as follows: |
| filterValue | name — full device name(s); id — device ID/IDs; type — values (auto, tracker, mobile, soft). |
| includeTy        The flag, which is responsible for showing the device | pe               type in the returned result. The default value is false. |
| ignoreRen        The flag, which is responsible for ignoring the renaming | ame              of the device type. The default value is false. |

## Returned result

[                  /* hardware types */

```json
           {
               "id":<uint>,                   /* ID */
               "uid2":<uint>,                 /* second ID */
               "name":"<text>",               /* name */
               "hw_category":"<text>",        /* hardware type */
                  "hw_features":"<text>", /* hardware features */
               "tp":"<text>",                 /* TCP port */
               "up":"<text>"                  /* UDP port */

        },
        ...
]
```

## get_statistics

The get_statistics function is used to receive the aggregated statistics
information.

```http
svc=core/get_statistics&params={"resourceId":<long>,
                                                                           "timeFrom":<uint>,
                                                                           "timeTo":<uint>,
                                                                           "type":"<text>",
                                                                           "interval_type":<uint>,
                                                                           "recursive":<uint>}
```

### Parameters

| Name | Description |
| --- | --- |
| resourceId | Resource ID. |
| timeFrom | Time from in the Unix time format. |
| timeTo | Time to in the Unix time format |
| type | One of following: items, logins, hw, sms. |
| The style of grouping the results: |  |
| 1 — by days; |  |
| interval_type | 2 — by weeks; 4 — by months; 8 — by quarters. |
| The default value is 1. |  |
| Depending on the value: |  |
| recursive                0 — use messages only from desired resource; | 1 — use messages also from child resources. |

## Returned result

```json
{
           "<timestamp>":{
                  "<resource_id>":{
                             "<parameter_name>": <int>,        /* statistics parameter Name-Value pairs         */...
                  }
           },
           ...,
           "users": {
                  "<user_id>": "<text>",       /* ID — name pairs */...

           }
}
```

The list of available statistics parameters:

sms_count;
sms_nf_count;

sms_count_<user_id>;
sms_job_count;
sms_order_count;
sms_manual_count;
sms_auth_count;
sms_cmd_<sms_type>_count;
logins_count_<user_id>;

logins_duration_<user_id>;
<unit_type_name>_deleted;
<unit_type_name>_created;
<item_type_name>_created;
<resource_type_name>_created;
<type_name>_created;
hw_<hw_type_id>;

<user_type_name>_created;
avl_driver_created;

avl_driver_deleted;
avl_job_created;

avl_job_deleted;
avl_notification_created;

avl_notification_deleted;
avl_tag_created;

avl_tag_deleted;
avl_trailer_created;

avl_trailer_deleted;
avl_geozone_created;

avl_geozone_deleted;

avl_unit_sensor_created;

avl_unit_sensor_deleted;
avl_unit_activated;

avl_unit_deactivated;
avl_unit_total.

The parameter avl_unit_total is returned in response to the request
with “type”: “items”. It shows the total number of units related to the
specified account and subordinate accounts.

### Error codes

Possible error codes:

| Code | Description |
| --- | --- |
| Failed to fetch the user with the desired ACL | 7 (ADF_ACL_ITEM_VIEW) or unexpected type value. |
| 4 | Wrong input parameters. |

## logout

The logout function is used to log out from Wialon correctly.

```http
svc=core/logout&params={}
```

## Returned result

```json
{
        "error":<int>      /* error code */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 0 | Logged out successfully. |
| 1 | Server connection error. |
| 4 | Non-authorized user. |

## reset_password_perform

The reset_password_perform function is used to finish the procedure of
changing password.

```http
svc=core/reset_password_perform&params={"user":"<text>",
                                               "code":"<text>"}
```

### Parameters

After the execution of the reset_password_request, an email with link is
sent to the user. The link leads to the URL indicated in the request and
contains two more parameters needed to finish the password reset:

| Name | Description |
| --- | --- |
| user | User name. |
| code | The code generated by the reset_password_request and sent to the user by email. |

## Returned result

```json
{
        "newPassword":"<text>"     /* new password */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| Wrong input parameters or failed to finish the password | 4 resetting. |

## reset_password_request

The reset_password_request is used to reset the password.

```http
svc=core/reset_password_request&params={"user":"<text>",
                                             "url":"<text>",
                                             "email":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| user | User name. |
| url | The URL sent in the email after the password reset request: <url>?user=<login>&passcode=<passcode>. See the value of the passcode on the reset_password_perform page. |
| email | User email. |

## Returned result

```json
{
        "error":0        /* successful request */
}
```

Possible error codes:

| Code | Description |
| --- | --- |
| 11 | See the reason field for the details. |

## search_item

The search_item function is used to find an item with a certain ID.

```http
svc=core/search_item&params={"id":<long>,
                              "flags":<long>}
```

### Parameters

| Name | Description |
| --- | --- |
| id | Item ID. |
| flags | Flags with properties for the returned result. The value of this parameter depends on the item type. The data formats of all item types and their flags are described in the format section. |

## Returned result

```json
{
        "item":{         /* found item */...
        },
        "flags":<uint>   /* applied flags with properties */
}
```

The format of the item parameter depends on the item type. All formats
are described in the format section.

Possible error codes:

| Code | Description |
| --- | --- |
| One of the following: |  |
| failed to get the current user; | 7 failed to find the item with the certain ID; the item is not active. |
| 6 | No session. |

## search_items

The search_items function is used to search for items by certain properties.

```http
svc=core/search_items&params={
    "spec":{
         "itemsType":"<text>",
         "propName":"<text>",
         "propValueMask":"<text>",
         "sortType":"<text>",
         "propType":"<text>",
         "or_logic":<bool>
    },
    "force":<uint>,
    "flags":<long>,
    "from":<uint>,
    "to":<uint>
}
```

### Parameters

| Name | Description |
| --- | --- |
| spec | Search specification. |
| itemsType | Item type (see the list below). |
| The name of the property by the value of which you | propName        want to search (see the list of possible properties below). You can use the character \|. |
| propValueMask | The property value mask. You can use the following characters: * \| , > < =. |
| sortType | The name of the property used for sorting. |
| propType | Property type (see the list below). |
| or_logic | The flag of the OR logic for the propName parameter (see Search by multiple properties section). |
| Depending on the value: |  |
| 0 — if such search has been done, return the | force              result; 1 — start a new search. |
| flags | Flags with properties for the returned result. The value of this parameter depends on item type. Data formats of all item types and their flags are described in the Data format section. |
| from | The index of the first returned item. To start a new search, specify 0. |
| to              The index of the last returned item. If 0 is specified, | all elements beginning from the index specified in |
| Name | Description |
| the from parameter are returned. |  |

## Item types

Item types (itemsType parameter):

avl_hw — hardware type;

avl_resource — resource;

avl_retranslator — retranslator;

avl_unit — unit;

avl_unit_group — unit group;

user — user;

avl_route — route.

## Item properties

Item properties (propName and sortType parameters):

sys_name — item name;

sys_id — item ID;

sys_unique_id — unique unit ID (IMEI);

sys_phone_number — unit phone number;

sys_phone_number2 — unit second phone number;

sys_user_creator — creator ID;

rel_user_creator_name — creator name;

sys_billing_account_guid — account ID;

rel_billing_account_name — account name;

rel_billing_parent_account_name — parent account name;

rel_billing_plan_name — billing plan name;

sys_comm_state — hardware state (1 — enabled, 0 — disabled);

rel_hw_type_name — hardware name;

rel_hw_type_id — hardware ID;

sys_account_balance — account balance;

sys_account_days — account days;

sys_account_enable_parent — dealer rights (1 — on, 0 — off);

sys_account_disabled — account blocked (1 — yes, 0 — no);

rel_account_disabled_mod_time — last modification time for the
sys_account_disabled properties, UNIX time;

rel_account_units_usage — number of units in the account;

rel_last_msg_date — last message time, UNIX time;

rel_is_account — whether the resource is an account (1 — yes, 0 — no);

login_date — last login time, UNIX time;

retranslator_enabled — retranslator state (1 — started, 0 — stopped);

rel_creation_time — creation time;

rel_group_unit_count — the number of units in a group;

rel_customfield_name — the name of the custom field of the unit;

rel_customfield_value — the value of the custom field of the unit;

rel_profilefield_name — the name of the profile field of the unit;

rel_profilefield_value — the value of the profile field of the unit;

rel_adminfield_name — the name of the admin field of the unit;

rel_adminfield_value — the value of the admin field of the unit;

rel_customfield_name — the name and value of the custom field of the
unit, separated by :;

rel_profilefield_name — the name and value of the profile field of the
unit, separated by :;
rel_adminfield_name — the name and value of the admin field of the unit,
separated by :.

For more values of this parameter, see the table below.

## Property types

Property types (propType parameter):

property — property;

list — list;

propitemname — subitem name (for example, geofence is a subitem of
resource);
creatortree — chain of creators (search of this type will return the list of
items the chain of creators of which contains the user specified in
the propValueMask parameter);
accounttree — chain of accounts (search of this type will return the list of
items the chain of accounts of which contains the account specified in
the propValueMask parameter);

customfield — custom fields;

profilefield — unit profile;

adminfield — administrative fields;

servicename — services.

## Subitems

If you want to search subitems, set the propitemname value for the
propType parameter. Then, other parameters can have any of the following
values:

Item (itemsType                 Subitem (propName and sortType
parameter)                      parameters)

avl_unit                        unit_sensors

avl_unit                        unit_commands

avl_unit                        service_intervals

avl_resource                    drivers

avl_resource                    driver_groups

Item (itemsType                 Subitem (propName and sortType
parameter)                      parameters)

avl_resource                    jobs

avl_resource                    notifications

avl_resource                    trailers

avl_resource                    trailer_groups

avl_resource                    zones_library

avl_resource                    reporttemplates

avl_resource                    orders

avl_route                       rounds

avl_route                       route_schedules

avl_retranslator                retranslator_units

avl_unit
user                            custom_fields
avl_resource

avl_unit
user                            admin_fields
avl_resource

## Sorting types

By default, direct sorting works as follows:

any name is split into bits for sorting (symbols, digits);
digits are sorted first, and then symbols;

- symbol is considered a hyphen and is sorted before digits (see
the special sorting);
system supports decimal mark numbers (3.12) and floating point
numbers (2e10; 5.1E-2).

The following sorting types are available:

Type           Description

Returns values sorted in ascending order:
Direct

```json
"sortType":"<item_property>"

Returns values by sorted in descending order:
```

Reverse

```json
"sortType":"!<item_property>"

Returns values sorted by the first property, then in case
```

Combined       of values equality by the second property, and so on:

```json
"sortType":"<property1>,!<property2>"

According to this sorting, the - symbol is considered anegative number sign. By default, the - symbol is
```

Special
considered a hyphen, not a minus.

```json
"sortType":"-<item_property>"
```

## Search by multiple properties

You can search for elements by several properties at once. For example:

```json
"itemsType":"avl_resource","propName":"rel_is_account,*","propValueMask":"1,qwe","sortType":"sys_name","propType":"property,customfield"
```

The number of properties in the propName, propType and propValueMask
parameters should be the same because they are calculated by three,
respectively.

The AND logic is worked by default for the propName parameter. It means
that the system will find all accounts (rel_is_account:1) the names of which
start with foo (sys_name:"foo*").

To enable the OR logic for the propName parameter, specify ''or_logic'':1 in
request.

## Using comparison operators in search

In the propValueMask parameter, you can use the following comparison
operators: <, >, =, >=, <=. If search criterion is a string field, the system will
search for numbers only in the beginning of such value. If search criterion
is number field, all value will be analysed.

## Example 1

```json
"itemsType":"avl_unit","propName":"sys_name,sys_name","propValueMask":">=32,<33.5"
```

The search results list all units the names of which start with numbers
between 32 and 33.5.

## Example 2

```json
"itemsType":"avl_resource","propName":"sys_account_balance,sys_account_balance","propValueMask":">2,<=23"
```

The search results list all resources and accounts the balance of which
is greater than 2 and less than or equal to 23.

You can also use the = operator if the field value starts with > or <.

## Example 3

```json
"itemsType":"avl_unit","propName":"sys_name","propValueMask":"=>12
3<,=<123>"
```

The search results list all available units with the names >123< and <123>.

## Returned result

```json
{
     "searchSpec": {                       /* search specification */
          "itemsType": "<text>",           /* items type */
          "propName": "<text>",            /* property name */
          "propValueMask": "<text>",       /* property value mask */
          "sortType": "<text>",            /* property name for sorting
*/
          "propType": "<text>"             /* property type */
     },
     "dataFlags": <uint>,                  /* applied data flags */
     "totalItemsCount": <uint>,            /* quantity of found items */
     "indexFrom": <uint>,                  /* beginning index */
     "indexTo": <uint>,                    /* ending index */
     "items": [{...}]                      /* found items */
}
```

The format of items array depends on the item type. All formats are
described in the Data format section.

Possible error codes:

| Code | Description |
| --- | --- |
| 4 | Wrong input parameters. |

## set_session_property

The set_session_property request is used to configure some parameters
of the current session.

svc=core/set_session_property&params={"prop_name":"<text>", "prop_
value":"<text>"}

### Parameters

The allowed property names (prop_name):

skip_nonactive_items — allows hiding the deactivated objects (by
default, all session objects are shown);
long_values — if set to 1, the server sends long numbers as strings (in
brackets).

For both cases the prop_value should be:

1 — activate;

2 — deactivate.

### Example

svc=core/set_session_property&params={"prop_name": "skip_nonactive
_items","prop_value": "1"}

## Returned result

{ }

Possible error codes:

| Code | Description |
| --- | --- |
| 6 | Session not found or failed to set property. |
| 4 | Wrong input parameters. |

## update_data_flags

The update_data_flags function is used to add and delete items from a
session. Adding items to a session is necessary to receive events from
them.

```http
svc=core/update_data_flags&params={"spec":[
                                            {
                                                   "type":"<text>",
                                                   "data":<long|text|
[long]>,
                                                   "flags":<long>,
                                                   "mode":<uint>,
                                                   "max_items":<uint>
                                            }
                                       ]}
```

### Parameters

| Name | Description |
| --- | --- |
| spec | The array of units with a configuration for requesting the modification of items that are in the session. |
| The method of transferring items to the session: |  |
| type | id: by ID. If this method is selected, you should specify the item ID in the data parameter. type: by type. If this method is selected, you should specify the type of items in the data parameter (see search_items). col: by ID list. If this method is selected, you should specify an array of IDs of the required items in the data parameter. access: subscribing to events about creating/deleting, obtaining/denying the items access rights, in the data parameter: 1, enable; 0, disable. |
| data | Data. This parameter depends on the previous one. |
| The flags that define what information about items should | flags   be added to the session. The item flags of each type are described in the Data format section. |
| The flag application mode: |  |
| 0: redefine flags for the specified items. |  |
| 1: add the specified flags to the existing ones in the | session. 2: delete the specified flags from the session (when mode       deleting the basic flag, the item is deleted from the session). |
| The flags are specified to monitor changes in the specific | properties of the item. The number of specified flags depends on your needs. If you want to receive all events, all flags should be specified. You can receive the events using the avl_evts function. |
| max_it       The maximum number of subscribed items. Available only | ems          when type='type'. |

## Returned result

```json
[                 /* array of items*/
        {
                  "i":<long>,      /* ID */
                  "d":{            /* other fields */...
                  },
                  "f":<long>       /* applied flags with properties
*/
        },
        ...
]
```

The “d” field format depends on the returned item type. If the “2” flag
mode is indicated when sending this request, the null value is returned to
the “d” field. The formats of all item types are described in the Data
format section.

Possible error codes:

| Code | Description |
| --- | --- |
| 4 | Wrong input parameters or error updating flags. |

## use_auth_hash

The use_auth_hash function can be used together with the
create_auth_hash instead of the duplicate function. In the authHash field,
enter the result of the create_auth_hash request.

```http
svc=core/use_auth_hash&params={"authHash":"<text>",
                                "operateAs":"<text>",
                                "checkService":"<text>"}
```

### Parameters

| Name | Description |
| --- | --- |
| authHash | The authorization hash that you can get using the create_auth_hash request. |
| operateAs | The name of the subordinate user on whose behalf you want to log in. |
| checkServi     You can check using the get_account_data (see | ce             the Service list section). |

## Returned result

```json
{
        "eid":"<text>",                    /* session ID */
        "gis_sid":"<text>",                /* session ID for the GISservices */
        "host":"<text>",                          /* host */
        "hw_gw_ip":"<text>",               /* hardware gateway IP */
        "au":"<text>",                     /* username */
        "hl":<int>,                               /* have login ID.
True if the field is present (the value always 1) */
        "tm":<uint>,                       /* current time (UTC) */

 "wsdk_version":"<text>",        /* SDK version */
     "base_url":"<text>",
     "hw_gw_ip":"<text>",             /* hardware gateway IP */
     "hw_gw_dns":"<text>",            /* hardware gateway DNS */
     "gis_search":"<text>",        /* GIS search URL */
     "gis_render":"<text>",           /* GIS render URL */
     "gis_geocode":"<text>",          /* GIS geocode URL */
     "gis_routing":"<text>",          /* GIS routing URL */
     "token":"<text>",                /* session token */
     "th":"<text>",                   /* token hash */
     "web_site":"<text>",             /* URL of the Wialon Monitoring
```

system */

```json
"web_cms_manager_site":"<text>"                 /* URL of the Wial
```

on Management system */

```json
"user":{                                /* the user on whose behal
```

f you want to log in */

```json
"nm":"<text>",                       /* name    */
"cls":<uint>,                        /* the ID of the s
```

uperclass "user" */

```json
"id":<long>,                         /* ID */
"prp":{                              /* custom properti
```

es, for example: */

```json
"dst":"<text>",                       /* dayligh
```

t saving time */

```json
"language":"<text>",                  /* languag
```

e (two-lettered code) */

```json
"msakey":"<text>",                    /* access
```

key to the mobile site */

```json
"pcal":"<text>",                                  /*
```

Iranian calendar */

```json
"tz":"<text>",                        /* time zo
```

ne */

```json
"us_units":"<text>",                  /* US metr
```

ics (miles and gallons) */
...

```json
  },
  "crt":<uint>,                        /* creator ID */
  "bact":<uint>,                       /* account ID */
  "fl":<uint>,                         /* user flags */
  "hm":"<text>",                       /* host mask */

"uacl":<uint>,                      /* user access to
```

himself */

```json
"mu": <uint>,                       /* measurement sys
```

tem */

```json
"ct": <uint>,                       /* the date of use
```

r creation */

```json
"ftp": {"<text>"},                  /* FTP server sett
```

ings */

```json
"ld": <uint>,                       /* the date of the
```

previous login */

```json
"pfl": <uint>,                      /* the flag of the
```

creator */

```json
"ap": {                             /* two-factor auth
```

entication settings */

```json
"type":<uint>,               /* authentication
```

type (0 — none, 1 — email, 2 — SMS) */

```json
       "phone":"<text>"             /* phone number */
},
"mapps": {"<text>"},                /* the list of mob
```

ile apps */

```json
"mappsmax": <int>                   /* the restriction
```

s for the mobile applications specified in the billing plan */

```json
},
"classes":{                         /* the superclasses availa
```

ble to the current user (key — superclass name, value — superclass
ID): */

```json
"avl_hw":<uint>,                    /* hardware type
```

*/

```json
       "avl_resource":<uint>,              /* resource */
       "avl_retranslator":<uint>,          /* retranslator */
       "avl_unit":<uint>,                  /* unit */
       "avl_unit_group":<uint>,            /* unit group */
       "user":<uint>,                      /* user */
       "avl_route":<uint>                  /* route */
}
"features":{
       "unlim":<bool>,                     /* billing plan ty
```

pe: 0 — regular, 1 — special (for development/testing) */

```json
"svcs":{                            /* hash-collection
```

of allowed services; if a service isn't mentioned here, it is forb

idden */
"<service_name>":<bool>,          /* key — s
ervice name; value: 0 — service available, but limit reached, 1 —
service available and can be used */
...

```
                 }
           }
}

      For additional information regarding the <service_name>,
      please see the list of services.
```

The user flags are described on the update_user_flags page.

See more about the FTP settings on the update_ftp_property page.

Possible error codes:

| Code | Description |
| --- | --- |
| 1003 | See the reason field for details. |
| 8 | Login failed. |
| 7 | Access denied. |
| 4 | Wrong input parameters. |
