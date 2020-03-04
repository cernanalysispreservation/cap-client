# Permissions


### Get

You can get existing analysis user permissions only if you have at least read access to it. You need to specify:

`--pid | the PID of an analysis`

    $ cap-client permissions get --pid/p <existing pid>

```json
{
    "updated": "2018-02-12T15:57:31.824619+00:00",
    "metadata": {
        "deposit-admin": {
            "user": [],
            "roles": []
        },
        "deposit-update": {
            "user": [],
            "roles": []
        },
        "deposit-read": {
            "user": [
                "alice@inveniosoftware.org"
            ],
            "roles": []
            }
        },
    "created": "2018-02-12T15:15:40.697516+00:00"
}
```


### Set

You can set existing analysis user permissions only if you have at least read access to it. You need to specify:

`--rights | the permission rights. You can choose between read, update and admin`

`--user   | the email of the user to grant permissions`

`--pid    | the PID of an analysis you want to set permissions`

    $ cap-client permissions add --rights/-r [read | update | admin] --user/-u <email> --pid/p <existing pid>
    e.g.
    $ cap-client permissions add -r update -u alice@inveniosoftware.org -p 0af85220ef0c492889658539d8b3d4e2

```json
{
    "updated": "2018-02-12T15:57:31.824619+00:00",
    "metadata": {
        "deposit-admin": {
            "user": [],
            "roles": []
        },
        "deposit-update": {
            "user": [
                "alice@inveniosoftware.org"
            ],
            "roles": []
        },
        "deposit-read": {
            "user": [
                "alice@inveniosoftware.org"
            ],
            "roles": []
            }
        },
    "created": "2018-02-12T15:15:40.697516+00:00"
}
```

### Remove

You can remove existing analysis user permissions only if you have at least read access to it. You need to specify:

`--rights | the permission rights. You can choose between read, update and admin`

`--user   | the email of the user to grant permissions`

`--pid    | the PID of an analysis you want to set permissions`

    $ cap-client permissions remove --rights/-r [read | update | admin] --user/-u <email> --pid/p <existing pid>
    e.g.
    $ cap-client permissions remove -r update -u alice@inveniosoftware.org -p 0af85220ef0c492889658539d8b3d4e2

```json
{
    "updated": "2018-02-12T15:57:31.824619+00:00",
    "metadata": {
        "deposit-admin": {
            "user": [],
            "roles": []
        },
        "deposit-update": {
            "user": [],
            "roles": []
        },
        "deposit-read": {
            "user": [
                "alice@inveniosoftware.org"
            ],
            "roles": []
            }
        },
    "created": "2018-02-12T15:15:40.697516+00:00"
}
```