# Unit groups

Depending on the specified flags, the response format may vary.

This chapter describes the flags that can be applied to unit groups and the
corresponding parts of the resulting JSON they control. If multiple flags are
specified, their respective parts are combined into a single JSON.

All flags are used only in DEC format.

## Unit group flags

The following flags can be applied to unit groups:

HEX value             DEC value                  Description

General properties (base
0x00000001           1
flag)

0x00000002           2                        Custom properties

0x00000004           4                        Billing information

0x00000008           8                        Custom fields

0x00000010           16                       Image

0x00000040           64                       GUID

0x00000080           128                      Administrative fields

0x3FFFFFFFFFFFF      461168601842738
Set all unit group flags
FFF                  7903

## General properties

The flag of general properties is 0x00000001.

```json
{
        "nm": <text>,     /* Name */
        "cls": <uint>,    /* Superclass ID: avl_unit_group */
        "id": <uint>,     /* Group ID */
        "u": [<long>],    /* Array of group units */
        "uacl": <uint>    /* User's access rights to the unit group
*/
}
```

## Custom properties

The flag of custom properties is 0x00000002.

You can store any data in custom properties.

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

## Custom fields

The flag of custom fields is 0x00000008.

```json
{
        "flds": {                            /* Custom fields */
                 <text>: {                       /* Sequence number */
                         "id": <uint>,       /* ID */
                         "n": <text>,        /* Name */
                         "v": <text>                /* Value */
                 },
                 ...
        },
        "fldsmax": <long>                    /* Maximum number of custom fields (-1 for unlimited) */

}
```

## Unit group image

The flag of the unit group image is 0x00000010.

```json
{
        "ugi": <uint>    /* Number of image changes */
}
```

## GUID

The flag of GUID is 0x00000040.

```json
{
        "gd": <text>     /* group GUID */
}
```

## Administrative fields

The flag of administrative fields is 0x00000080.

```json
{
        "aflds": {                      /* Administrative fields */
                 <text>: {                  /* Sequence number */
                         "id": <uint>,      /* ID */
                         "n": <text>,       /* Name */
                         "v": <text>            /* Value */
                 },
                 ...

        },
        "afldsmax": <long>,        /* Maximum number of administrative fields (-1 for unlimited) */
```
