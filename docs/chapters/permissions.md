## Permissions

The `permissions` command group allows the user to access, retrieve, and change the permissions of a specified analysis.

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client permissions --help]
Usage: cap-client permissions [OPTIONS] COMMAND [ARGS]...

  Manage analysis permissions.

Options:
  --help  Show this message and exit.

Commands:
  add     Add user/egroup permissions for your analysis.
  get     List analysis permissions.
  remove  Remove user/egroup permissions for your analysis.
```

### Add user/e-group permissions to an analysis

#### Description

- Allows the user to add permissions of a specified analysis.
- The user can add permissions to a specific user or a whole e-group.
- The supported options are the following:

| Name          | Type   | Desc                                                  |
| :------------ | :----- | :---------------------------------------------------- |
| --pid / -p    | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --user / -u   | TEXT   | User mail. (mutually exclusive with --egroup)         |
| --egroup / -e | TEXT   | Egroup mail. (mutually exclusive with --user)         |
| --rights / -r | TEXT   | Options: read / update / admin  [required]            |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client permissions add --pid <analysis-pid> --user info@inveniosoftware.org --rights read|update]
{
    'deposit-admin': {
        'roles': [],
        'users': ['user@inveniosoftware.org']
    },
    'deposit-read': {
        'roles': [],
        'users': ['user@inveniosoftware.org', info@inveniosoftware.org]
    },
    'deposit-update': {
        'roles': [],
        'users': ['user@inveniosoftware.org', info@inveniosoftware.org]
    }
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client permissions add --pid <analysis-pid> --egroup egroup@inveniosoftware.org --rights read]
{
        "deposit-admin": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        },
        "deposit-read": {
            "roles": ['egroup@inveniosoftware.org'],
            "users": ["info@inveniosoftware.org"]
        },
        "deposit-update": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        }
    }
```

### Retrieve the permissions of an analysis

#### Description

- Allows the user to retrieve the permissions of a specified analysis.
- The supported options are the following:

| Name        | Type   | Desc                                                  |
| :---------- | :----- | :---------------------------------------------------- |
| --pid / -p  | TEXT   | Your analysis PID (Persistent Identifier)  [required] |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client permissions get --pid <analysis-pid>]
{
    'deposit-admin': {
        'roles': [],
        'users': ['user@inveniosoftware.org']
    },
    'deposit-read': {
        'roles': [],
        'users': ['user@inveniosoftware.org']
    },
    'deposit-update': {
        'roles': [],
        'users': ['user@inveniosoftware.org']
    }
}
```

### Remove user/e-group permissions from an analysis

#### Description

- Allows the user to remove permissions from a specified analysis.
- The user can remove permissions from a specific user or a whole e-group.
- The supported options are the following:

| Name          | Type   | Desc                                                  |
| :------------ | :----- | :---------------------------------------------------- |
| --pid / -p    | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --user / -u   | TEXT   | User mail. (mutually exclusive with --egroup)         |
| --egroup / -e | TEXT   | Egroup mail. (mutually exclusive with --user)         |
| --rights / -r | TEXT   | Options: read / update / admin  [required]            |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client permissions remove --pid <analysis-pid> --user info@inveniosoftware.org --rights read]
{
    'deposit-admin': {
        'roles': [],
        'users': ['user@inveniosoftware.org']
    },
    'deposit-read': {
        'roles': [],
        'users': ['user@inveniosoftware.org']
    },
    'deposit-update': {
        'roles': [],
        'users': ['user@inveniosoftware.org']
    }
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client permissions remove --pid <analysis-pid> --egroup egroup@inveniosoftware.org --rights read]
{
        "deposit-admin": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        },
        "deposit-read": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        },
        "deposit-update": {
            "roles": [],
            "users": ["info@inveniosoftware.org"]
        }
    }
```
