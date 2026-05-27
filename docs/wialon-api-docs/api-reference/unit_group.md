# unit_group

This section describes the methods that can be applied to the unit groups.
The creation of unit groups is described here.

## update_units

To add units into a group or remove them from it, use the command
unit_group/update_units:

```http
svc=unit_group/update_units&params={"itemId":<long>,
                                         "units":[<long>]}
```

### Parameters

The required parameters are marked with an asterisk (*).

| Name | Description |
| --- | --- |
| itemId* | Unit group ID. |
| units* | Array of units IDs. |
| The units parameter must contain the IDs of both the units that have | already been added and the ones you want to add. To remove a unit from the group, you must list the IDs of the units that should remain in the group. |

### Response

If the request is executed successfully, the following result is returned:

```json
{
         "u":[<long>]     /* array of unit IDs */
}
```

Otherwise, an error code is returned.

### Error codes

Error
Description
code

Failed to fetch the item with
7            ACL(ADF_ACL_ITEM_EDIT_SUB_ITEMS), or session check
failed.

6            Failed to write a new units list.

4            Wrong input parameter (units).
