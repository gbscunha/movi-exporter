# account

This section describes the methods that can be applied to accounts.

## activation_code_report

To retrieve historical data about activation code actions (assignments,
unassignments, and expirations) within a specified time range, use the
account/activation_code_report method.

Prerequisites
-
The activation code feature (billing_by_codes) must be enabled for
the service.
The user must be the creator of a top account or an account with
dealer rights.

### Endpoint

```http
svc=account/activation_code_report&params={
    "timeFrom": <long>,
    "timeTo": <long>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| timeFrom | Start of the time range (Unix timestamp). Must be less than timeTo. |
| timeTo | End of the time range (Unix timestamp). Must be greater than timeFrom. |

### Response

If the request is completed successfully, the response is returned as an
array of objects in the following format:

```json
[
    {
        "guid": <text>,       /* Activation code GUID. */
        "uid": <long>,        /* Unit ID. Returns 0 if the code wasn't assigned at the time of the action. */
        "uname": <text>,      /* Unit name. Empty if the code wasn't assigned. */
        "action": <int>,      /* Action type: 0 — assigned, 1 — unassigned, 2 — expired. */
        "acc_id": <long>,     /* Account ID where the unit is created. Returns 0 if no unit was assigned. */

         "acc_name": <text>,    /* Account name. Empty if no unit wasassigned. */
         "tmc": <long>,         /* Code creation timestamp (Unix time). */
         "ttl": <long>,         /* Validity period in seconds. */
         "tma": <long>,         /* Activation timestamp, that is, when the code was first assigned to a unit (Unix time). */
         "tme": <long>          /* Estimated expiration timestamp (Unix time). */
    }
]
```

The data returned depends on the user’s role:

Top account user: all activation code actions for the specified time
range are returned.
Account with dealer rights: only actions linked to units to which the
user has the Manage activation codes access right
(ADF_ACL_AVL_UNIT_MANAGE_BILLING_CODES) are returned.

If no actions occurred in the specified time range, an empty array is
returned.

If the request fails, an error code is returned.

### Error codes

Error
Description
code

Invalid input parameters (missing parameters or timeFrom
4
>= timeTo).

5            Error performing request (internal server error).

7            Access denied, because the user doesn’t belong to a
service with billing_by_codes enabled, or isn’t an account

Error
Description
code

creator with dealer rights.

## change_account

Prerequisites
-
In order to transfer a unit into a subordinate account, the user who
created the account must have the Manage account access right to
their own account (ACL flag 0x100000000). The following access rights
to the transferred unit are necessary:

View object and its basic properties (ACL flag 0x000001)
Manage access to this object (ACL flag 0x000004)

Delete object (ACL flag 0x000008)
Edit connectivity settings: device type, unique ID, phone, access
password, message validity filtering (ACL flag 0x100000)

#### Delete messages (ACL flag 0x800000)

To transfer a unit into a subordinate account and change the unit creator in
this account, use the account/change_account method:

```http
svc=account/change_account&params={"itemId":<long>,
                                       "resourceId":<long>}
```

### Parameters

The request must contain the following parameters.

| Parameter | Description |
| --- | --- |
| itemId | Unit ID. |
| resourceId | Account ID. |

### Response

If migration ends successfully, an empty object is returned.

If some errors occur, the response has the following format:

```json
{
          "error":\<uint>
}
```

## check_billing_issues

To identify hierarchy rule violations in billing services, use the
account/check_billing_issues method. It checks the entire account
hierarchy (both parent and child accounts).

### Endpoint

```http
svc=account/check_billing_issues&params={
    "itemId": <long>
}
```

### Parameters

The request must contain the itemId parameter specifying the ID of the
account to be checked for billing issues.

### Response

If the request is completed successfully, the response is returned in the
following format:

```json
[
    {
        "svc_name": <text>,          // Service name where the issue was detected.
        "reason": <int>,             // Issue code (see below).
        "account_id": <long>,        // ID of the account causing theissue. Specified if the signed-in user has the "View object and its basic properties" access right to this account.
        "account_name": <text>       // Name of the account causing the issue.pecified if the signed-in user has the "View object and its basic properties" access right to this account.
    }
]
```

### Issue codes

Issue
Description
code

The account has reached the service limit according to the
1           service cost specified in the parent account (applies to
periodic services and services on demand).

The account has reached the balance limit according to the
service cost and the Limit by balance option specified in
2
the parent account or its billing plan (applies only to
services on demand).

Issue
Description
code

-1           Other billing issues.

If the request fails, an error code is returned.

## check_smtp_settings

To validate SMTP server settings before applying them to a billing plan, use
the account/check_smtp_settings method.

Only top-level users can use this method. Subusers will
receive an error.

### Endpoint

```http
svc=account/check_smtp_settings&params={
    "send_from": <text>,
    "send_to": <text>,
    "smtp_host": <text>,
    "smtp_port": <uint>,
    "smtp_login": <text>,
    "smtp_password": <text>,
    "subject": <text>,
    "body": <text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| send_from | Sender email address. |
| send_to | Recipient email address for the test message. |
| smtp_host | SMTP server address including protocol (e.g., smtps://smtp.gmail.com or smtp://smtp.example.com). |
| smtp_port | SMTP server port number (e.g., 465 for SMTPS, 587 for SMTP with STARTTLS). |
| smtp_login | Login username for SMTP authentication. |
| Password for SMTP authentication. Instead of this | smtp_password       parameter, you can use plan specifying the billing plan name. |
| Name of the billing plan from which to retrieve the | plan                saved SMTP password. Instead of this parameter, you can use the smtp_password parameter. |
| subject | Subject line for the test email. |
| body | Body text for the test email. |

### Examples

Below are the examples of the account/check_smtp_settings requests.

## Request with password

svc=account/check_smtp_settings&params={

```json
     "send_from": "notifications@example.com",

    "send_to": "admin@example.com",
    "smtp_host": "smtps://smtp.gmail.com",
    "smtp_port": 465,
    "smtp_login": "notifications@example.com",
    "smtp_password": "your_app_password",
    "subject": "Test SMTP Connection",
    "body": "This is a test email to validate SMTP settings."
}
```

## Request with billing plan

```http
svc=account/check_smtp_settings&params={
    "send_from": "notifications@example.com"
    "send_to": "admin@example.com",
    "smtp_host": "smtps://smtp.gmail.com"
    "smtp_port": 465,
    "smtp_login": "notifications@example.com"
    "plan": "my_billing_plan",
    "subject": "Test SMTP Connection",
    "body": "This is a test email to validate SMTP settings."
    }
```

### Response

If the request is completed successfully and the test email is sent, the
response returns code 250:

```json
{
    "code": 250
}
```

If the request fails, an error code is returned.

### Error codes

Error
Description
code

General validation or configuration error. This code may
indicate one of the following:

Invalid input parameters
Neither password nor billing plan was specified
Failed to fetch billing account plugin
600        Failed to fetch subaccount plans
Specified billing plan not found
Failed to get email config plugin
Failed to get email service
Failed to create email

800     The current user is not a top-level user or is not signed in.

6       Failed to resolve the SMTP server host.

Connection timeout. This may occur when an incorrect port
28
is specified.

Failed to receive data from the server. This may occur
56      when attempting to connect to an SMTPS server using
SMTP protocol.

535     Invalid SMTP credentials (login or password).

Incorrectly formatted email address or unrecognized
555
character in the send_from or send_to fields.

## create_account

To create a new account, use the account/create_account method:

```http
svc=account/create_account&params={"itemId":<long>,
                    "plan":<text>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource ID. |
| plan | Billing plan. |

### Response

If the account is created successfully, an empty object is returned.

Otherwise, an error code is returned.

## delete_account

To delete an account, use the account/delete_account method.

### Endpoint

To delete an account with units in Wialon Hosting, use the folowing
signature:

```http
svc=account/delete_account
&params={
    "itemId": <long>,
    "reasons": [{"reason_key"}]
}
```

To delete an account without units in Wialon Hosting or any account in
Wialon Local, use the folowing signature:

```http
svc=account/delete_account
&params={
    "itemId": <long>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Account ID. |
| reasons | Array of reasons for deleting an account in Wialon Hosting. Reason keys are described below. |

### Account deletion reasons

Reason Key                                               Description

delayed_resolution_of_reported_bugs_partner              Bugs or
technical

Reason Key                                  Description

issues were
not resolved
quickly
enough
(partner
initiative).

Bugs or
technical
issues were
delayed_resolution_of_reported_bugs_user    not resolved
quickly
enough (user
initiative).

Key features
or functions
were missing
or insufficient
missing_functionality_partner               (partner
initiative). A
text field can
be added for
details.

Key features
or functions
were missing
or insufficient
missing_functionality_user                  (user
initiative). A
text field can
be added for
details.

downtime_or_frequent_errors_partner         The system
experienced

Reason Key                                          Description

frequent
outages or
errors
(partner
initiative).

The system
experienced
frequent
downtime_or_frequent_errors_user
outages or
errors (user
initiative).

Disagreement
disagreement_on_pricing
on pricing.

Another
platform
offers better
better_terms_from_another_platform
pricing,
features, or
flexibility.

Account
access was
restricted or
blocked due
strict_debt_management_rules_or_account_blockages   to unpaid
invoices or
strict
financial
policies.

poor_technical_support_quality                      Technical
support was
slow,
unhelpful, or

Reason Key                                      Description

not meeting
expectations.

The preferred
language is
lack_of_support_in_desired_language
not
supported.

The end user
failed to pay
end-                                            or went out of
user_stopped_payments_or_went_out_of_business   business,
causing
termination.

Other
reasons
(partner
other_reasons_partner                           initiative). A
text field can
be added for
details.

Other
reasons (user
initiative). A
other_reasons_user
text field can
be added for
details.

Another
provider
better_terms_from_another_provider              offers more
favorable
conditions.

Reason Key                                                Description

Seasonal
removal of
seasonal_units_deletion                                   units that are
no longer
active.

The formal
contract
contract_expiration                                       ended and
wasn’t
renewed.

Poor service
poor_service
quality.

### Example

Below is an example of a request for deleting an account with units in
Wialon Hosting.

```http
svc=account/delete_account&params={"itemId": 19812, "reasons":
[{"reason_key": "delays_in_resolving_reported_technical_problems_partner"}]}
```

Below is an example of a request for deleting an account because of
missing functionality, which includes the text field.

```http
svc=account/delete_account &params={ "itemId": 19813, "reasons":
[{ "reason_key": "missing_functionality_user", "text": "User needed a specific report that is not available."}]}
```

### Response

If the account is deleted successfully, an empty object is returned.

Otherwise, an error code is returned.

## do_payment

To make a payment, use the account/do_payment method:

```http
svc=account/do_payment&params={"itemId":<long>,
                    "balanceUpdate":<double>,
                    "daysUpdate":<int>,
                    "description":<text>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID |
| balanceUpdate | Sum of payment. The value can be negative. |
| daysUpdate | Quantity of days added. The value can be negative. |
| description | Description. |

### Response

If the payment is successful, an empty object is returned.

Otherwise, an error code is returned.

## enable_account

To enable or disable an account, use the account/enable_account
method:

```http
svc=account/enable_account&params={"itemId":<long>,
                    "enable":<bool>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| enable | Mode: 0 — disable, 1 — enable. |

### Response

If the account is enabled successfully, an empty object is returned.

Otherwise, an error code is returned.

## get_account_data

To get detailed information about an account, use this signature of the
account/get_account_data method:

```http
svc=account/get_account_data&params={"itemId":<long>,
                                            "type":<uint>}
```

For information about several accounts, use the following signature:

```http
svc=account/get_account_data&params={"itemId":[<long>],
                                            "type":<uint>}
```

### Parameters

The request can contain the following parameters. The required parameters
are marked with an asterisk (*).

| Parameter | Description |
| --- | --- |
| itemId* | Resource (account) ID. |
| Response flag. Types of response: |  |
| type | 1 — minimal information, usually required to estimate the state of the logged user; 2 — detailed information with combined, personal and billing plan settings; 4 — excludes subordinate accounts from usage. The information concerns only the current account; |
| 8 — details on personal sites. |  |

### Response

If the request is completed successfully, the response for a single account
is as follows:

{

```json
"parentAccountName":<text>, /* Parent account name. */
"parentAccountId":<long>,       /* Parent account ID. */
"parentEnabled":<bool>,             /* Parent account is: 1 — availa
```

ble, 0 — blocked. */

```json
"plan":<text>,            /* Billing plan name. */
"enabled":<int>,     /* State: 0 — blocked, 1 — active. */
"flags":<uint>,           /* Flags - duplicates flags from billing
```

plan settings. */

```json
"created":<unit>, /* Account creation time, UNIX-time. */
"balance":<text>, /* Balance (with currency). */
"daysCounter":<uint>, /* Counter of days. */
"settings":{
     "balance":<double>,      /* Balance. */
     "plan":{           /* Billing plan settings. */
         "flags":<uint>,            /* Billing plan flags (see belo
```

w). */

```json
"blockBalance":<int>, /* Minimum balance for the accou
```

nt to be active. */               "denyBalance":<int>,       /* deny balan
ce */

```json
"minDaysCounter":<int>,          /* Minimum number of days. I
```

f a lower number of days is left, the account is blocked. */

```json
"historyPeriod":<uint>,          /* Period during which messa
```

ges are stored. If 0 is specified, the storage period is unlimite
d. */

```json
"currencyFormat":"<currency_format>", /* Account curre
```

ncy format. */

```json
"services":{           /* List of services. */
    <text>:{        /* Service name. */
          "type":<int>,          /* Service type: 1 — on dema
```

nd; 2 — periodic */

```json
"usage":<uint>,            /* Number of created res
```

ources in the current service */

```json
"maxUsage":<int>, /* Maximum number of resourc
```

es. */

```json
"cost":<text>,            /* Cost table. */
"interval":<int>       /* Reset frequency: 0 — non
```

e, 1 — hourly, 2 — daily, 3 — weekly, 4 — monthly.*/

```json
"descr":"<text>"      /* Billing service descrip
```

tion. */

```json
           }
     }
},
"personal":{           /* Account (personal) settings. */...           /* Has the same format as billing plan set
```

tings. */

```json
},
"combined":{           /* Combined settings consisting of bil
```

ling plan and account settings. */
...           /* Has the same format as billing plan set
tings. */

```json
       }
},
"siteAccess":{
            "<service_name>":"<dns_name>",          /* Where the key i
```

s a service name and the value is a DNS name */
...

```
/* If you use the "type=8" parameter (see above), the
```

object includes the following additional information.*/
"<service_name>": {

```json
"n":"<dns_name>", /* Where the value is a DNS nam
```

e. */

```json
"tt":"<template_type>", /* Where the value is a si
```

te template type (wialon_web, cms_manager.) */

```json
"b":"<branch>", /* Site branch (v1311, master, dev
```

elop,v1408). */

```json
"sp":<int>, /* SSL port. */
"force_https":"<force_https>", /* Site custom prop
```

erty "force_https". */

```json
"ignore_in_cms_login_as":"<ignore_in_cms_login_as
```

>" /* Site custom property "ignore_in_cms_login_as". */

```json
            }
            ...
},
"serviceKeys":{ /* External map providers. */                      "nam
```

e":"<text>",        /* Map key name.*/

```json
             "type":<int>,            /* Key type. */
             "provider":"<text>" /* Map provider name. */

      },
      "managable":<int>,      /* Allow managing the account specifiedin the request: 1 — yes, 0 — no. */
      "dealerRights":<int>, /* Allow using dealer rights for the billing plan of the specified account: 0 — no, 1 — yes. */
      "subPlans":[<text>]     /* Array of subordinate billing plans.
*/
}
```

The response for several accounts is structured as follows:

```json
{
      "<account_id1>": {    /* Requested account ID. */...                  /* Account information (see above). */
      },
      "<account_id2>": {    /* Requested account ID. */...                  /* Account information (see above). */
      },
      ...
}
```

### Service key types

Type               Description

0x01               Protected key (Gurtam key).

0x02               Routing key.

0x04               Geocoding key.

0x08               Distance matrix key.

Type              Description

0x10              Map tiles key.

### Account flags

| Flag | Description |
| --- | --- |
| Block users, if the balance is lower than the blocking | 0x01 threshold. |
| Forbid login to the system and stop account functioning if the | 0x02 balance is less than the blocking threshold. |
| Decrease the number of days in the day counter, and block | 0x20      the account when the number of remaining days reaches the minimum. |
| 0x40 | Redefine billing plan flags. |
| 0x04 | Allow unknown services. |

### Services list

Service                  Type            Description

Activates the Accounts section in
CMS Manager; defines the quantity
avl_resource             periodic
and cost of resources and
accounts.

Service              Type            Description

Activates the Retranslators
section in CMS Manager and
avl_retranslator     periodic
defines the allowed quantity and
cost of retranslators.

Activates the Routes module.
Enables the Routes tab and
avl_route            periodic
associated reports and
notifications.

Activates the Units section in CMS
Manager and the Units tab in the
avl_unit             periodic
monitoring system. Defines the
cost and quantity of units.

Activates the Unit groups section
in CMS Manager and Units tab in
avl_unit_group       periodic
the monitoring system. Defines the
cost and quantity of unit groups.

on
cms_manager                          Grants access to CMS Manager.
demand

Activates the button to create units
on              in the Units section in CMS
create_units
demand          Manager and the Units tab in the
monitoring system.

Activates the button to create
on              users in the Users section in CMS
create_users
demand          Manager and the Users tab in the
monitoring system.

create_unit_groups   on              Activates the button to create unit
demand          groups in the Unit groups section
in CMS Manager and the Unit

Service            Type            Description

groups tab in the monitoring
system

Activates the button to create
on              resources and accounts in the
create_resources
demand          Resources section in CMS
Manager.

Activates the Custom fields tab in
the properties of units, users or
groups. Defines the cost and
custom_fields      periodic
quantity (summarized, by objects
of different types) of custom fields;
does not affect drivers and trailers.

Activates advanced reports:
reports on unit groups, users,
drivers, trailers as well as groups
on
custom_reports                     of drivers and trailers (except the
demand
Log table for users and unit
groups). Works within the Reports
module.

Activates the Drivers module and
defines the cost and quantity of
drivers. If disabled, the Drivers
drivers            periodic        tab is not shown and mentions of
drivers disappear from
notifications, user settings, and
SMS dialog.

Defines the quantity and cost of
driver_groups      periodic        driver groups. Works within the
Drivers module.

Service              Type            Description

Enables sending notifications by e-
on              mail. The recommended limitation
email_notification
demand          is 10 reports an hour (to avoid
server overloading).

Enables sending a report by e-mail
(within the Jobs module). The
on
email_report                         recommended limitation is 10
demand
reports an hour (to avoid server
overloading).

on
google_service                       Activates Google services.
demand

on              Activates the Import/Export
import_export
demand          features on monitoring sites.

Activates the Jobs tab. Defines the
jobs                 periodic        cost and the allowed number of
jobs.

on              Activates the Locator option in the
locator
demand          user menu.

on              Grants access to the Messages
messages
demand          tab.

net_access           on              Allows authentication through the
(outdated)           demand          service connector in Wialon Pro.

Activates the Notifications tab
notifications        periodic        and defines the cost and the
allowed number of notifications.

Service              Type            Description

Activates access to the Logistics
application and allows running the
orders               periodic
Orders report on units and drivers
in the monitoring system.

Activates the POI panel and
pois (outdated)      periodic        defines the cost and allowed
quantity of POIs.

Activates the Reports module and
defines the cost and the allowed
on              quantity of report templates. If
reports
demand          disabled, associated jobs and
notifications disappear and the trip
detector can’t be used.

Defines the number of available
retranslator_units   periodic        units attached to activated
retranslators.

Defines the number of allowed
rounds               periodic        rounds and their cost (within the
Routes module).

Defines the number of allowed
route_schedules      periodic        schedules and their cost (within
the Routes module).

on
sdk                                  Grants access to Apps.
demand

service_intervals    periodic        Defines the cost and quantity of
service intervals. If activated, the
Service intervals tab appears in
the unit properties. Allows
registering events of the

Service              Type            Description

Maintenance type, run reports and
receive notifications about
maintenance.

on              Determines the allowed quantity of
sms
demand          SMS messages and their cost.

Activates the Driver activity and
on
tacho                                Violations tables in reports on
demand
drivers.

Activates the Users tab and
storage_user         periodic        defines the cost and quantity of
users.

Activates the Trailers tab and
trailers             periodic        defines the cost and quantity of
trailers.

Defines the quantity and cost of
trailer_groups       periodic        trailers; works within the Trailers
module.

Activates the Commands tab in
the unit properties. Defines the
unit_commands        periodic
quantity (for all units in total) and
cost of commands.

Defines the number of sensors
unit_sensors         periodic        (calculated for all units in total)
and their cost.

Enables receiving notices from the
user_notifications   periodic
administrator of the service.

Service            Type            Description

Wialon_activex     on              Grants remote access to the
(outdated)         demand          system via SDK, ActiveX.

wialon_mobile      on              Activates access to the application
(outdated)         demand          for Android and iOS.

Activates access to the application
on
wialon_mobile2                     for Android and iOS. Requires the
demand
wialon_mobile service enabled.

on              Grants remote access to the
wialon_sdk
demand          system via SDK.

Activates the Geofences module
and defines the cost and quantity
of geofences. If disabled, the
zones_library      periodic        Geofences tab is not shown, and
any mention of geofences
disappears from reports and user
settings.

zone_groups        periodic        Activates groups of geofences.

AgroService (outdated)             Type          Description

agroplots                          periodic      Plots

agroplotgroups                     periodic      Groups of plots

agrocrops                          periodic      Crops

AgroService (outdated)                 Type       Description

agromachines                           periodic   Machines

agroequipments                         periodic   Equipment

agrocultivationtypes                   periodic   Cultivation types

## get_account_history

To get the account statistics, use the account/get_account_history
method:

```http
svc=account/get_account_history&params={"itemId":<long>,
                      "days":<int>,
                      "tz":<int>}
```

You can’t execute this request simultaneously with the requests from the
exchange section and the following requests:

…/report/exec_report
…/report/export_result

…/report/get_result_chart
…/report/get_result_map

…/messages/load_interval
…/render/create_messages_layer

…/unit/get_trips
…/resource/get_driver_bindings

### …/resource/get_trailer_bindings

### Parameters

The request must contain the following parameters.

| Name | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| days | Interval for which you want to request statistics, in days. |
| tz | Time zone. |

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
[
      [
          <uint>,        /* Action type: 1 — payment, 0 — charged */
          <text>,        /* Date */
          <text>,        /* Service */
          <text>,        /* Cost */
          <uint>,        /* Quantity */
          <text>,        /* Information */
          <int>     /* Registration time */
      ]
]
```

If the request fails, an error code is returned.

## get_billing_plans

The request is available only for top accounts.

To get a list consisting of your own and your subordinate billing plans, use
the account/get_billing_plans method:

```http
svc=account/get_billing_plans&params={}
```

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
{
     "plan": {                                   /* Your billing plan. */
       "parent": <text>,                         /* Parent plan name.
*/
       "name": <text>,                           /* Billing plan name. */
       "servicesModCounter": <uint>,             /* Service modification counter. */
       "historyPeriod": <int>,                   /* Period of time tostore unit messages. */
       "flags": <uint>,                          /* Flags. */
       "denyBalance": <double>,                  /* Minimum balance required for paid features to function. */
       "minDaysCounter": <int>,                  /* Minimum number ofdays before account is blocked. */
       "blockBalance": <double>,                 /* Balance thresholdfor account to be blocked. */
       "currencyFormat": <text>,                 /* Currency format.
*/
       "descr": <text>,                          /* Billing plan description. */
       "email": <text>,                          /* Email address. */
       "enable_smtp": <text>,                    /* Email SMTP state.
*/
       "smtp_host": <text>,                      /* SMTP host. */
       "smtp_port": <text>,                      /* SMTP port. */

       "smtp_login": <text>,                       /* SMTP login. */

       "nfSmsSender": <text>,                      /* Notification send
```

er phone. */

```json
"cmdSmsSender": <text>,                     /* Command sender ph
```

one. */

```json
"hwTypes": {                                /* Hardware object.
```

*/
"<hw_id>": {

```json
          "name": <text>                    /* Hardware name. */
     },
     ...
},

"personal": {
     "services": <object>                   /* Service object (s
```

ee below). */

```json
},

"combined": {
     "services": <object>                   /* Service object (s
```

ee below). */

```json
     }
},

"subPlans": [                                    /* List of subordina
```

te billing plans. */

```json
{
     "parent": <text>,                      /* Parent plan name.
```

*/

```json
"name": <text>,                        /* Billing plan nam
```

e. */

```json
"servicesModCounter": <uint>,          /* Service modificat
```

ion counter. */

```json
"historyPeriod": <int>,                /* Message retention
```

period. */

```json
"flags": <uint>,                       /* Flags. */
"denyBalance": <double>,               /* Minimum balance r
```

equired for paid features. */

```json
"minDaysCounter": <int>,                /* Number of days le
```

ft before the account is blocked. */

```json
"blockBalance": <double>,               /* Minimum number of
```

days before account is blocked. */

```json
"currencyFormat": <text>,               /* Currency format.
```

*/

```json
"descr": <text>,                        /* Description. */
"email": <text>,                        /* Email address. */
"enable_smtp": <text>,                  /* SMTP enable flag.
```

*/

```json
"smtp_host": <text>,                    /* SMTP host. */
"smtp_port": <text>,                    /* SMTP port. */
"smtp_login": <text>,                   /* SMTP login. */
"nfSmsSender": <text>,                  /* Notification send
```

er phone. */

```json
"cmdSmsSender": <text>,                 /* Command sender ph
```

one. */

```json
"hwTypes": {
     "<hw_id>": {
          "name": <text>                /* Hardware name. */
     },
     ...
},

"personal": {
     "services": <object>               /* Service object.
```

*/

```json
},

"combined": {
     "services": <object>               /* Combined service
```

object. */

```
         }
    },
    ...
]
```

}

## Services

```json
"services":{                                 /* Service object where keysare correct service names. */
                 "<service_name>":{                       /* Put correctservice name instead of <service_name>. */
                                   "type": <uint>,
                                   "maxUsage": <int>,
                                   "cost": <text>,
                                   "interval": <uint>,
                                   "descr": <text>,
                                   "flags": <uint>,
                                   "ct": <uint>,
                                   "mt": <uint>
                 },
                 ...
}
```

For a complete list of services, see account/get_account_data.

## get_business_spheres

Business fields are available only for the users of top accounts or accounts
with dealer rights.
To get available business spheres that can be used as a business field of a
client, use the get_business_spheres method:

```http
svc=account/get_business_spheres&params={"lang":""}
```

The parameter lang is optional. The default value is en.

### Response

If the request is completed successfully, the response contains a list of
available business fields. Example:

{

```json
"long_haul_transportation":{
     "name":"Long-haul transportation",
     "group":"Transportation and delivery",
     "position":1
},
"local_fmcg_delivery":{
     "name":"Local FMCG delivery",
     "group":"Transportation and delivery",
     "position":2
},
"food_and_grocery_delivery":{
     "name":"Food and grocery delivery",
     "group":"Transportation and delivery",
     "position":3
},
"cold_chain_transportation":{
     "name":"Cold chain transportation",
     "group":"Transportation and delivery",
     "position":4
},
"post_and_express_mail_services":{
     "name":"Post and express mail services",
     "group":"Transportation and delivery",
     "position":5
},
"pharmaceutical_transportation":{
     "name":"Pharmaceutical transportation",
     "group":"Transportation and delivery",
     "position":6
},
"dangerous_goods_transportation":{
     "name":"Dangerous goods transportation",
     "group":"Transportation and delivery",
     "position":7
},
"maritime_and_waterway_delivery":{
     "name":"Maritime and waterway delivery",
     "group":"Transportation and delivery",

 "position":8
```

},
"railway_cargo_transport":{

```json
"name":"Railway cargo transport",
"group":"Transportation and delivery",
"position":9
```

},
"drone_delivery":{

```json
"name":"Drone delivery",
"group":"Transportation and delivery",
"position":10
```

},
"public_transport":{

```json
"name":"Public transport",
"group":"Passenger transport",
"position":11
```

},
"taxi_limo_and_ridesharing_services":{

```json
"name":"Taxi, limo and ridesharing services",
"group":"Passenger transport",
"position":12
```

},
"student_transport":{

```json
"name":"Student transport",
"group":"Passenger transport",
"position":13
```

},
"corporate_transport":{

```json
"name":"Corporate transport",
"group":"Passenger transport",
"position":14
```

},
"railway_passenger_transport":{

```json
"name":"Railway passenger transport",
"group":"Passenger transport",
"position":15
```

},
"maritime_passenger_transport":{

```json
"name":"Maritime passenger transport",
"group":"Passenger transport",

"position":16
```

},
"government_and_ngo_vehicles":{

```json
"name":"Government and NGO vehicles",
"group":"Passenger transport",
"position":17
```

},
"food_industry":{

```json
"name":"Food industry",
"group":"Industry and manufacturing",
"position":18
```

},
"industrial_manufacturing":{

```json
"name":"Industrial manufacturing",
"group":"Industry and manufacturing",
"position":19
```

},
"electric_power_generation_and_services":{

```json
"name":"Electric power generation and services",
"group":"Industry and manufacturing",
"position":20
```

},
"consumer_goods_manufacturing":{

```json
"name":"Consumer goods manufacturing",
"group":"Industry and manufacturing",
"position":21
```

},
"crop_farming":{

```json
"name":"Crop farming",
"group":"Agriculture",
"position":22
```

},
"greenhouse_and_hydroponics":{

```json
"name":"Greenhouse and hydroponics",
"group":"Agriculture",
"position":23
```

},
"forestry":{

```json
"name":"Forestry",
"group":"Agriculture",

"position":24
```

},
"animal_breeding":{

```json
"name":"Animal breeding",
"group":"Agriculture",
"position":25
```

},
"construction_and_demolition":{

```json
"name":"Construction and demolition",
"group":"Construction",
"position":26
```

},
"landscaping":{

```json
"name":"Landscaping",
"group":"Construction",
"position":27
```

},
"ready_mix_concrete":{

```json
"name":"Ready-mix concrete",
"group":"Construction",
"position":28
```

},
"roadworks":{

```json
"name":"Roadworks",
"group":"Construction",
"position":29
```

},
"child_protection":{

```json
"name":"Child protection",
"group":"Personal monitoring",
"position":30
```

},
"field_workers":{

```json
"name":"Field workers",
"group":"Personal monitoring",
"position":31
```

},
"people_with_special_needs":{

```json
"name":"People with special needs",
"group":"Personal monitoring",

"position":32
```

},
"prisoners_in_custody_and_on_parole":{

```json
"name":"Prisoners in custody and on parole",
"group":"Personal monitoring",
"position":33
```

},
"delivery_personnel":{

```json
"name":"Delivery personnel",
"group":"Personal monitoring",
"position":34
```

},
"leasing_and_auto_loans":{

```json
"name":"Leasing and auto loans",
"group":"Rentals and sharing",
"position":35
```

},
"carsharing":{

```json
"name":"Carsharing",
"group":"Rentals and sharing",
"position":36
```

},
"micromobility":{

```json
"name":"Micromobility",
"group":"Rentals and sharing",
"position":37
```

},
"car_and_truck_rental":{

```json
"name":"Car and truck rental",
"group":"Rentals and sharing",
"position":38
```

},
"equipment_and_special_machinery_rental":{

```json
"name":"Equipment and special machinery rental",
"group":"Rentals and sharing",
"position":39
```

},
"oil_gas_fuel":{

```json
"name":"Oil, gas, fuel",
"group":"Mining and processing",

"position":40
```

},
"mining_and_quarrying":{

```json
"name":"Mining and quarrying",
"group":"Mining and processing",
"position":41
```

},
"raw_materials_processing":{

```json
"name":"Raw materials processing",
"group":"Mining and processing",
"position":42
```

},
"smart_home_and_office":{

```json
"name":"Smart home and office",
"group":"Building automation and management",
"position":43
```

},
"domestic_utilities_and_services":{

```json
"name":"Domestic utilities and services",
"group":"Building automation and management",
"position":44
```

},
"telecom_cable_tv":{

```json
"name":"Telecom, cable TV",
"group":"Building automation and management",
"position":45
```

},
"security_alarm_fire_systems":{

```json
"name":"Security, alarm, fire systems",
"group":"Building automation and management",
"position":46
```

},
"ambulance_and_emergency_services":{

```json
"name":"Ambulance and emergency services",
"group":"Security and public safety",
"position":47
```

},
"police":{

```json
"name":"Police",
"group":"Security and public safety",

"position":48
```

},
"fire_safety":{

```json
"name":"Fire safety",
"group":"Security and public safety",
"position":49
```

},
"security_services":{

```json
"name":"Security services",
"group":"Security and public safety",
"position":50
```

},
"stolen_vehicle_recovery_svr":{

```json
"name":"Stolen vehicle recovery (SVR)",
"group":"Security and public safety",
"position":51
```

},
"video_surveillance":{

```json
"name":"Video surveillance",
"group":"Security and public safety",
"position":52
```

},
"military":{

```json
"name":"Military",
"group":"Security and public safety",
"position":53
```

},
"waste_management":{

```json
"name":"Waste management",
"group":"Public utilities",
"position":54
```

},
"street_cleaning_and_roadworks":{

```json
"name":"Street cleaning and roadworks",
"group":"Public utilities",
"position":55
```

},
"towing_and_roadside_assistance":{

```json
"name":"Towing and roadside assistance",
"group":"Public utilities",

"position":56
```

},
"gas_stations":{

```json
"name":"Gas stations",
"group":"Stationary assets",
"position":57
```

},
"electric_generators_and_wind_turbines":{

```json
"name":"Electric generators and wind turbines",
"group":"Stationary assets",
"position":58
```

},
"vending_machines":{

```json
"name":"Vending machines",
"group":"Stationary assets",
"position":59
```

},
"equipment_and_tools":{

```json
"name":"Equipment and tools",
"group":"Stationary assets",
"position":60
```

},
"electric_charging_stations":{

```json
"name":"Electric charging stations",
"group":"Stationary assets",
"position":61
```

},
"consumer_goods":{

```json
"name":"Consumer goods",
"group":"Stationary assets",
"position":62
```

},
"other_stationary_assets":{

```json
"name":"Other stationary assets",
"group":"Stationary assets",
"position":63
```

},
"vehicle_maintenance_and_repair":{

```json
  "name":"Vehicle maintenance and repair",
  "group":"Vehicle servicing",

         "position":64
    },
    "insurance":{
         "name":"Insurance",
         "group":"Vehicle servicing",
         "position":65
    },
    "pet_monitoring":{
         "name":"Pet monitoring",
         "group":"Animal tracking",
         "position":66
    },
    "wildlife_tracking":{
         "name":"Wildlife tracking",
         "group":"Animal tracking",
         "position":67
    },
    "indoor_asset_tracking":{
         "name":"Indoor asset tracking",
         "group":"Indoor Tracking",
         "position":68
    },
    "indoor_person_tracking":{
         "name":"Indoor person tracking",
         "group":"Indoor Tracking",
         "position":69
    },
    "other":{
         "name":"Other",
         "group":"Other",
         "position":70
    }

}
```

If the request fails, an error code is returned.

## list_change_accounts

To get a list of accounts to which you can transfer a unit, use the
list_change_accounts method:

```http
svc=account/list_change_accounts&params={"units":[<long>]} |
```

The request must contain the unit parameter, specifying the unit ID array.

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
[
    {
    "id":<long>,        /* Account ID. */
    "name":<text>       /* Account name. */
    },
    ...                 /* Other valid accounts (if any). */
]
```

## sites

You can use the account/sites method to get a list of sites of the top
account and to update a site branch.

## Getting a list of sites

To get a list of sites (wialon_web) of the top account, set callMode to list.

```http
svc=account/sites&params={"callMode":"list"}
```

## Updating a site

To update a branch, you can use the request that applies active branches
(ADF + CMS) to wialon_web websites.

Only the branch_mode site option can be modified by this request.

The request is submitted as a JSON object, where the keys are the site
names.

Set callMode to update, specify the site name and branch:

```http
svc=account/sites&params={"callMode":"update","sites":{"<site_name
>":"<branch_value>"}}
```

where <site_name> is the text value of the site name and
<branch_value> is the site branch mode value described below.

The values stand for the following branches:

Value                    Site branch

0                        Stable.

1                        Beta.

2                        Stable and beta.

### Response

If the request is completed successfully, a response of the following format
is returned:

```json
[
    {
        "n":"video-hosting.wialon.com",            /* Site address.
```

*/

```json
"cn":"hosting_video",               /* Site common nam
```

e. */

```json
"bm":0                              /* Branch mode 0,
```

1, 2. */

```json
  },
  {
        "n":"night-hosting.wialon.com",
        "cn":"default_night",
        "bm":0
  },
  {
        "n":"beta-hosting.wialon.com",
        "cn":"hosting_beta",
        "bm":0
  },
  {
        "n":"wialonb3.gurtam.com",
        "cn":"GurtamTest",
        "bm":0
  },
  {
        "n":"my-hosting.wialon.com",
        "cn":"GurtamTest7",
        "bm":0
  },
  {
        "n":"us.hosting.wialon.net",
        "cn":"GurtamTest5",
        "bm":0
  },
  {
        "n":"qa.wialon.com",
        "cn":"GurtamTest_3",
        "bm":0
  },
  {
        "n":"sales-hosting.wialon.com",
        "cn":"GurtamTest6",
        "bm":0

    }
]
```

If the request fails, an error code is returned.

## trash

In the top account, you can get the list of deleted macro-objects in the
trash bin. You can also restore them using the account/trash method:

```http
svc=account/trash&params={"callMode":<text>,
"guids":[<text>]}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| Possible values are list and restore. List is used to | callMode         get the list of deleted objects. To restore the objects, specify the restore value. |
| GUIDs | Item GUIDs for restoring. Used for the restore callMode. |
| You can restore a deleted item only 20 minutes after it was deleted. |  |

### Response

If the request is completed successfully, the response for a list of macro-
objects in the trash bin is as follows:

```json
{
      "code":<uint>,
      "items": [
                   {
                         "guid":<text>,         /* GUID */
                         "name":<text>,         /* Item name. */
                         "tm":<uint>,           /* Time of deletion. */
                         "type":<text>,         /* Macro-object type (forexample, "avl_resource"). */
                         "creator_id":<text>, /* ID of the creator. */
                         "tm":<**int**>,         /* Deletion time. */
                         "props":
                         {
                             "prop_name":<prop_type>,    /* List of public item properties (string, int, long, double). */...
                         }
                   },
                   ...
      ]
}
```

The response for restoring macro-objects from trash:

```json
{
      "code":<uint>,
      "items": [
                   {
                         "name":<text>,         /* Item name. */
                         "result":<bool>,       /* Result: 1 — success,
0 — failure. */
                         "type":<text>,          /* Macro-object type.
*/
                         "reason":<text>            /* Reason for a possible error. */
                   },
                   ...

    ]
}
```

If the object could not be restored, the following reasons can be indicated
in the response:

MAX_ITEMS_EXCEEDED. The limit set for the resource is exceeded.

TIMEOUT_20_MIN. You can restore a deleted item only 20 minutes after it
was deleted.
INTERNAL_SERVER_ERROR. A server error occurred.

## trash_microelements

In the top account, you can get the list of deleted micro-objects in the trash
bin and restore them using the account/trash_microelements method:

```http
svc=account/trash_microelements&params={"callMode":<text>}
```

Set callmode to list to get the list of micro-objects and restore to restore
them from the trash bin.

```http
svc=account/trash_microelements&params={"callMode":"restore","items":[{"type":<text>,"guid":<text>,"props":["name":<text>,"ids":[<long>]]}]}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| type | Pass the avl_resource value in this parameter. |
| guid | Resource GUID. |
| name | Micro-object type: “drivers”, “trailers”, “tags” (passengers). |
| ids | IDs of the micro-objects (drivers, trailers, passengers). |

### Response

If the request is completed successfully, the response for a list of deleted
micro-objects is as follows:

```json
{
     "code": <uint>,
     "items": [
       {
           "type": <text>,                 /* avl_resource */
           "guid": <text>,                 /* Resource GUID */
           "name": <text>,                 /* Resource name */
           "trailers": [
                {
                    ...
                }
           ],
           "drivers": [
                {
                    ...
                }
           ],
           "tags": [

                 {
                     ...
                 }
             ]
         }
         ...
     ]
}
```

The response for restoring deleted micro-objects:

```json
{
     "code": <uint>,
     "items": [
         {
             "guid": <text>,           /* Resource GUID */
             "type": <text>,           /* avl_resource */
             "props": [
                 {
                     "name": <text>,   /* Micro-object type: "drivers", "trailers", "tags" (passengers). */
                     "id": <int>,      /* ID of the micro-object (driver, trailer, passenger) */
                     "result": <int>   /* Result: 1 — success, 0 — failure.
*/
                 }
             ]
         }
         ...
     ]
}
```

## update_billing_plan

You can use the update_billing_plan method to create, update and delete
a billing plan:

svc=account/update_billing_plan&params={

```json
"callMode": <text>,
"plan": {
    "name": <text>,
    "rename": <text>,
    "servicesModCounter": <uint>,
    "historyPeriod": <int>,
    "flags": <uint>,
    "denyBalance": <double>,
    "blockBalance": <double>,
    "minDaysCounter": <int>,
    "currencyFormat": <text>,
    "descr": <text>,
    "email": <text>,
    "enable_smtp": <text>,              /* Email SMTP state. */
    "smtp_host": <text>,               /* SMTP host. */
    "smtp_port": <text>,                /* SMTP port. */
    "smtp_login": <text>,              /* SMTP login. */
    "smtp_password": <text>,            /* SMTP password. */
    "mapserver_tags": <text>,           /* Map tags. */
    "hwTypes": {
         "<hw_id>": {
              "name": <uint>
         },
         ...
    },
    "parent": <text>,
    "personal": {
         "services": <object>
    }
}
```

}

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| callMode | Request type (create, update, delete). |
| name | Billing plan name (unique field). |
| rename | New billing plan name. You can’t edit the name of the billing plan of the top account user. The names of billing plans are unique. You can’t give the same name to two billing plans. |
| servicesModCounter | The number of modifications in the list of services. |
| historyPeriod | Time to store unit messages, in days. |
| flags | Billing plan flags (see below). |
| denyBalance | Minimum balance for the account to be active. If the balance is lower, the account is blocked. |
| Minimum balance for the paid services to be | blockBalance         available. If the balance is lower, the services are blocked. |
| Number of days left before the account is | minDaysCounter       blocked. The number of days decreases if the Block by days option is enabled. |
| currencyFormat | Currency format. |
| descr | Billing plan description. |
| email | Email address. |

## Billing plan flags

| Flag | Description |
| --- | --- |
| Block users, if the balance is lower than the blocking | 0x01 threshold. |
| If the balance is lower than the minimum, the user can’t log in | 0x02 to the system and the account is suspended. |
| 0x08 | It is forbidden to use the specified hardware types. |
| It is forbidden to use the hardware types that are not | 0x10 specified. |
| Decrease the number of days in the day counter, and block | 0x20   the account when the number of remaining days reaches the minimum. |

## Hardware types

| Name | Description |
| --- | --- |
| <hw_name> | Hardware name. |
| id | Hardware ID. |

## Services

| Name | Description |
| --- | --- |
| cost | Limit and cost in the format described on the Services page. |
| descr | Service description. |
| flags | Define action: 0 — none, 1 — create/update, 2 — delete. |
| interval | Reset frequency: 0 — none 1 — hourly 2 — daily 3 — weekly 4 — monthly |
| maxUsage | Amount of available items. |
| name | Service name. |
| type | Service type: 1 — on demand, 2 — periodic. |
| For more details about services, visit the get_account_data page. |  |

### Response

If the request is completed successfully, the response looks as follows:

```json
{
    "parent": <text>,                    /* Parent billing plan name. */
    "name": <text>,                      /* Billing plan name. */
    "servicesModCounter": <uint>,      /* Number of service modificatio
```

ns. */

```json
"historyPeriod": <uint>,               /* History period to store messa
```

ges, in days. If 0 is specified, the period is unlimited. */

```json
"flags": <uint>,                       /* Billing plan flags. */
"denyBalance": <int>,                  /* The balance value at which pa
```

id services become unavailable. */

```json
"blockBalance": <int>,                 /* The balance value at which th
```

e account is blocked. */

```json
"minDaysCounter": <int>,               /* Minimum days counter. */
"currencyFormat": <text>,              /* Currency format. */
"descr": <text>,                       /* Description. */
"email": <text>,                       /* Email. */
"mapserverTags": <text>,               /* Map server tags. */

"hwTypes": {                           /* Hardware object. */
     "<hw_id>": {                      /* Hardware ID. */
          "name": <text>               /* Hardware name. */
     },
     ...
},

"personal": {
     "services": <object>              /* Service object (see below).
```

*/

```json
},

"combined": {
     "services": {                     /* Service object where keys are
```

valid service names. */
"<service_name>": {          /* Insert service name instead o
f <service_name>. */

```json
"type": <uint>,            /* Type: 1 — on demand; 2 — peri
```

odic. */

```json
"maxUsage": <int>,         /* Number of active resources of
```

the service. */

```json
"cost": <text>,            /* Maximum number of resources.
```

*/

```json
"interval": <uint>,        /* Cost table. */
"descr": <text>,           /* Interval: 0 — none, 1 — hourl
```

y, 2 — daily, 3 — weekly, 4 — monthly. */

```json
                 "flags": <uint>
            },
            ...
        }
    }
}
```

For more details about services, visit the get_account_data page.

## update_billing_service

To manage the available services and their cost, use the
account/update_billing_service method:

```http
svc=account/update_billing_service&params={"itemId":<long>,
                               "name":<text>,
                               "type":<ubyte>,
                               "intervalType":<ubyte>,
                               "costTable":<text>
}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| name | Service name. You can find the complete list of services on the get_account_data page. |
| Parameter | Description |
| type | Service type: 1 – on demand (for example, SMS). IntervalType defines how often the indicated limit is reset. 2 – periodic services. Payments are made after a specified time interval. |
| intervalType | Reset interval type: 0 – never 1 – hourly 2 – daily 3 – weekly 4 – monthly. |
| costTable | Limit and cost in the format described on the Services page. |

### Response

If the service is updated successfully, an empty object is returned.
Otherwise, an error code is returned.

## update_business_sphere

To set a business sphere for the account, use the
account/update_business_sphere method:

```http
svc=account/update_business_sphere&params={"itemId":<long>, "sph":
<text>}
```

Only accounts (not resources) are accepted. The sph field must contain
either valid IDs (taken from the configuration file) or an empty value to
reset.

You can get the list of business spheres using the
account/get_business_spheres command.

### Response

If the business sphere is updated successfully, an empty object is returned.

Otherwise, one of the following reasons is indicated in the error:

item is not account. You have indicated the ID of an object which is not
an account.
unknown sphere id. The value in the sph field is incorrect.

```json
{"error":<**int**>,"reason":<unknown sphere id> }
```

## update_dealer_rights

To let an account use dealer rights, the account/update_dealer_rights
method is applied:

```http
svc=account/update_dealer_rights&params={"itemId":<long>,
"enable":<bool>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| enable | Enable or disable dealer rights. |

### Response

If dealer rights are enabled successfully, an empty object is returned.
Otherwise, an error code is returned.

## update_flags

To set the flags of account settings, use the account/set_flags method:

```http
svc=account/update_flags&params={"itemId":<long>,
                   "flags":<long>,
                   "blockBalance":<double>,
                   "denyBalance":<double>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| flags | Account settings flags. Read more about account flags on the get_account_data page. |
| blockBalance | The balance value at which the account is blocked. |
| denyBalance | The balance value at which the paid services become unavailable. |

### Response

If flags are updated successfully, an empty object is returned.

Otherwise, an error code is returned.

## update_history_period

To update the period during which the account data is stored, use the
account/update_history_period method:

```http
svc=account/update_history_period&params={"itemId":<long>,
                       "historyPeriod":<int>}
```

### Parameters

The request must contain the following parameters:

| Name | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| historyPeriod | History period value, in days. If the value has mask 0x10000, the history period is measured in months. |

### Response

If the history period is updated successfully, an empty object is returned.

Otherwise, an error code is returned.

## update_min_days

To update the minimum number of days, use the
account/update_min_days method:

```http
svc=account/update_min_days&params={"itemId":<long>,
                     "minDays":<int>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| minDays | Minimum number of days. |

### Response

If the number of days is updated successfully, an empty object is returned.

Otherwise, an error code is returned.

## update_plan

Prerequisites
-
To assign a billing plan to an account, the user must have the Manage
account access right to this account (see core/check_items_billing).
The user must be a direct or indirect parent of the account.

To assign a billing plan, use the account/update_plan method:

```http
svc=account/update_plan&params={"itemId":<long>,
                 "plan":<text>}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| plan | Billing plan name. |

### Response

If the plan is assigned successfully, an empty object is returned.

Otherwise, an error code is returned.

## update_sub_plans

Prerequisites
-
The user can assign only the available subordinate billing plans. To
assign a billing plan to an account, the user must be a direct or
indirect parent of the account and have the following permissions:

Manage account access right to this account (see
core/check_items_billing).
dealer rights. To enable them, use the account/update_dealer_rights
method.

To set the list of subplans that the specified account can assign, use the
account/update_sub_plans method:

```http
svc=account/update_sub_plans&params={"itemId":<long>,
                      "plans":[<text>]}
```

### Parameters

The request must contain the following parameters:

| Parameter | Description |
| --- | --- |
| itemId | Resource (account) ID. |
| plans | List of subplans. |

### Response

If the plan is updated successfully, an empty object is returned.

Otherwise, the response contains error code 7, indicating that the user has
no dealer rights.
