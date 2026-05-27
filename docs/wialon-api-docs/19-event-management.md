# Event management

Event management is a process which can be divided into two parts:

adding the necessary items to the session, specifying the necessary
event types;
receiving and handling events.

## Adding items to the session

To get events from items, you must add these items to the session using
the core/update_data_flags method.

There are three ways to add items to the session:

by type
by ID
by list of IDs

## Example 1

Let’s add three units to the session: Bavarian Tractor, Alabama, and
Touareg. Their IDs are known, so we add these units specifying the value
col for the type parameter:

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/update_data_flags&params={
     "spec": [
         {
             "type": "col",
             "data": [34868, 22800, 553632],
             "flags": 1,
             "mode": 0
         }
     ]
}&sid=<your_sid>
```

As only the base flag is set, we will be able to get events only about
renaming of these units.

As the value of the mode parameter is set to 0, all the previous flags of the
item will be replaced by the ones from the request.

Response:

```json
[
    {
        "i": 34868,
        "d": null,
        "f": 1
    },
    {
        "i": 22800,
        "d": null,
        "f": 1
    },
    {
        "i": 553632,
        "d": null,
        "f": 1
    }
]
```

## Example 2

If you don’t need to get events from the unit Touareg any more, you can
remove it from the session. As the removal applies only to one unit, set the
value id for the type parameter in the request.

```http
https://hst-api.wialon.com/wialon/ajax.html?svc=core/update_data_flags&params={
    "spec": [
        {
            "type": "id",

             "data": 553632,
             "flags": 1,
             "mode": 2     /* removing flag */
         }
     ]
}&sid=<your_sid>
```

To completely remove a unit from the session, set the flags parameter to
1. You can only stop receiving all messages from a unit by specifically
requesting removal of the base flag.

For example, if you initially added a unit with flag 3 (which combines flags
1 and 2) and later remove only flag 2, flag 1 will still remain active. As a
result, you’ll no longer receive events associated with flag 2, but you’ll
continue to receive events associated with flag 1.

Ressponse:

```json
[
     {
         "i": 553632,
         "d": null,
         "f": 0
     }
]
```

As the f returns a value of 0, it confirms that the unit has been successfully
removed from the session.
