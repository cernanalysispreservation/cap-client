## Metadata

The `metadata` command group allows the user to access, retrieve, and change the metadata of a specified analysis.

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata --help]
Usage: cap-client metadata [OPTIONS] COMMAND [ARGS]...

  Manage analysis metadata.

Options:
  --help  Show this message and exit.

Commands:
  get     Get analysis metadata.
  remove  Remove from analysis metadata.
  update  Update analysis metadata.
```


### Retrieve analysis metadata

#### Description

- Allows the user to retrieve the metadata of a specified analysis.
- The user can retrieve the whole JSON object, or select a specific field to be returned.
- The command supports the dot operator (e.g. `basic_info.abstract`) to define nested fields or list indices, allowing the user to retrieve every piece of metadata autonomously.
- The supported options are the following:

| Name        | Type   | Desc                                                  |
| :---------- | :----- | :---------------------------------------------------- |
| --pid / -p  | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --field     | TEXT   | Specify field, eg. object.nested_array.0              |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata get --pid <analysis-pid>]
{
    "basic_info": {
        "abstract": "test abstract",
        "ana_notes": [
            "AN-1234/123",
            "AN-3456/789"
        ]
    },
    "general_title": "test"
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata get --pid <analysis-pid> --field general_title]
"test"
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata get --pid <analysis-pid> --field basic_info.ana_notes.0]
"AN-1234/123"
```

### Update an analysis

#### Description

- Allows the user to update the metadata of an analysis.
- The JSON object can be passed as it is through the cli or bypassing the file name of the JSON file that contains it.
- The supported options are the following:

| Name            | Type     | Desc                                                              |
| :-------------- | :------- | :---------------------------------------------------------------- |
| --pid / -p      | TEXT     | Your analysis PID (Persistent Identifier)  [required]             |
| --field         | TEXT     | Specify an existing field, eg. object.nested_array.0              |
| --json / -j     | TEXT     | JSON data (mutually exclusive with --jsonfile, --text, --num)     |
| --jsonfile / -f | FILENAME | JSON file (mutually exclusive with --json, --text, --num)         |
| --text / -t     | TEXT     | Text data (mutually exclusive with --jsonfile, --json, --num)     |
| --num / -n      | FILENAME | Numeric data (mutually exclusive with --json, --jsonfile, --text) |
#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata update --pid <analysis-pid> --field basic_info --json '{"abstract": "new abstract"}']
{
    "created": "2020-04-23T14:24:44.068071+00:00",
    "metadata": {
        "basic_info": {
            "abstract": "new abstract"
        },
        "general_title": "test"
    },
    "pid": "796be0cc6d314e25b9c11dc0864e8d32",
    "updated": "2020-04-23T14:36:45.175490+00:00"
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata update --pid <analysis-pid> --field basic_info.abstract --json \"new abstract\"]
{
    "created": "2020-04-23T14:24:44.068071+00:00",
    "metadata": {
        "basic_info": {
            "abstract": "new abstract"
        },
        "general_title": "test"
    },
    "pid": "796be0cc6d314e25b9c11dc0864e8d32",
    "updated": "2020-04-23T14:36:45.175490+00:00"
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata update --pid <analysis-pid> --jsonfile JSONFILE]
{
    "created": "2020-04-23T14:24:44.068071+00:00",
    "metadata": {
        "basic_info": {
            "abstract": "new abstract"
        },
        "general_title": "test"
    },
    "pid": "796be0cc6d314e25b9c11dc0864e8d32",
    "updated": "2020-04-23T14:36:45.175490+00:00"
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata update --pid <analysis-pid> --field general_title --text new-test]
{
    "created": "2020-04-23T14:24:44.068071+00:00",
    "metadata": {
        "basic_info": {
            "abstract": "new abstract"
        },
        "general_title": "new-test"
    },
    "pid": "796be0cc6d314e25b9c11dc0864e8d32",
    "updated": "2020-04-23T14:36:45.175490+00:00"
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata update --pid <analysis-pid> myfield  --num 1.2]
{
    "created": "2020-04-23T14:24:44.068071+00:00",
    "metadata": {
        "myfield": 1.2
    },
    "pid": "796be0cc6d314e25b9c11dc0864e8d32",
    "updated": "2020-04-23T14:36:45.175490+00:00"
}
```

### Remove a metadata field

#### Description

- Allows the user to remove a specified metadata field from an analysis.
- The supported options are the following:

| Name       | Type     | Desc                                                            |
| :--------- | :------- | :-------------------------------------------------------------- |
| --pid / -p | TEXT     | Your analysis PID (Persistent Identifier)  [required]           |
| --field    | TEXT     | Specify an existing field, eg. object.nested_array.0 [required] |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client metadata remove --pid <analysis-pid> --field basic_info.abstract]
{
    "basic_info": {},
    "general_title": "test"
}
```
