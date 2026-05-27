# Retranslators

Depending on the specified flags, the response format may vary.

This chapter describes the flags that can be applied to retranslators and
the corresponding parts of the resulting JSON they control. If multiple flags
are specified, their respective parts are combined into a single JSON.

All flags are used only in DEC format.

## Retranslator flags

The following flags can be applied to retranslators:

HEX value            DEC value                 Description

0x00000001           1                         Base flag

0x00000002           2                         Custom properties

0x00000004           4                         Billing information

0x00000040           64                        GUID

0x00000080           128                       Administrative fields

0x00000100           256                       State and configuration

0x00000200           512                       Retranslator units

0x3FFFFFFFFFFF       461168601842738           Set all possible
FFFF                 7903                      retranslator flags

## General properties

The flag of general properties is 0x00000001.

```json
{
        "nm":<text>,      /* Name */
        "cls":<uint>,     /* Superclass ID: "avl_retranslator" */

        "id":<long>,     /* Retranslator ID */
        "uacl":<uint>    /* User's access rights to the retranslator */
}
```

## Custom properties

The flag of custom properties is 0x00000002.

You can store any retranslator data in custom properties.

```json
{
        "prp": {}        /* Custom properties */
}
```

## Billing information

The flag of billing information is 0x00000004.

```json
{
        "crt": <uint>,   /* Creator ID */
        "bact": <uint>   /* Account ID */
}
```

## GUID

The flag of GUID is 0x00000040.

```json
{
        "gd": <text>     /* Retranslator GUID */

}
```

## Administrative fields

The flag of administrative fields is 0x00000080.

```json
{
     "aflds": {                 /* Administrative fields */
          <text>: {            /* Sequence number */
               "id": <uint>,   /* ID */
               "n": <text>,    /* Name */
               "v": <text>     /* Value */
          },
          ...
     },
     "afldsmax": <long>        /* Maximum number of administrative fields
(-1 for unlimited) */
}
```

## State and configuration

The flag of state and configuration is 0x00000100.

```json
{
     "rtro": <int>,                 /* State: 0 for disabled, 1 for enabled */
     "rtrc": {                     /* Configuration */
          "protocol": <text>,      /* Protocol */
          "server": <text>,        /* Server for retransmission */
          "port": <ushort>,        /* Port (for all protocols except NIS)
*/
          "auth": <text>,          /* Authorization (only for NIS and Wialon IPS) */

         "ssl": <int>,              /* Secure connection (for NIS): 1 — yes, 0 — no */
         "v6type": <int>,           /* Use protocol version 6 (only for Granit Navigator): 0 — no, 1 — yes */
         "login": <text>,           /* Login */
         "password": <text>,        /* Password */
         "notauth": <int>           /* Disable authorization (only for EGT
S): 0 — no, 1 — yes */
    }
}
```

Protocol types are described on the update_config page.

## Retranslator units

The flag of retranslator units is 0x00000200.

```json
{
           "rtru":    [{                         /* List of units */
                     "i": <long>,       /* Unit ID */
                     "a": <text>                     /* Hardware ID */
           }]
}
```
