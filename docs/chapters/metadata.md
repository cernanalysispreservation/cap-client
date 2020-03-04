# Metadata

For all the metadata-related commands, you will need to define the pid needed:

`--pid  | the PID as a parameter.`


### Get

You can get existing analysis metadata only if you have at least read access to it.

    $ cap-client metadata get <field> --pid/-p <existing pid>
    e.g.
    $ cap-client metadata get --pid 4b2924db6c32467bb2de6221f4faf167

```json
{
    "$ana_type": "lhcb",
    "$schema": "https://macbook-trzcinska.cern.ch:5000/schemas/deposits/records/lhcb-v0.0.1.json"
}
```

You can also request more specific information, if you know the schema model:

    $ cap-client metadata get basic_info.description --pid 4b2924db6c32467bb2de6221f4faf167
    with response:
    $ "Very Interesting Description"


### Edit

You can edit and change existing metadata details if you have at least read access to it.

    $ cap-client metadata set <field> <new value> --pid/p <existing pid>
    e.g.
    $ cap-client metadata set basic_info.description "Very Interesting Description" --pid 4b2924db6c32467bb2de6221f4faf167

```json
{
    "$ana_type": "lhcb",
    "$schema": "https://macbook-trzcinska.cern.ch:5000/schemas/deposits/records/lhcb-v0.0.1.json",
    "basic_info": {
        "description": "Very Interesting Description"
    }
}
```

Ypou can also add more information, by providing the exact location that you want to save it.

    $ cap-client --verbose metadata append basic_info.my_array "New element" --pid 0af85220ef0c492889658539d8b3d4e2

```json
{
    "$ana_type": "lhcb",
    "$schema": "https://macbook-trzcinska.cern.ch:5000/schemas/deposits/records/lhcb-v0.0.1.json",
    "basic_info": {
        "my_array": [
            "New element"
        ],
        "description": "Very Interesting Description"
    }
}
```

### Remove

You can remove existing metadata details if you have at least read access to it.

    $ cap-client metadata remove <field> -p 0af85220ef0c492889658539d8b3d4e2
    e.g.
    $ cap-client metadata remove basic_info.my_array.0 -p 0af85220ef0c492889658539d8b3d4e2

```json
{
    "$ana_type": "lhcb",
    "$schema": "https://macbook-trzcinska.cern.ch:5000/schemas/deposits/records/lhcb-v0.0.1.json",
    "basic_info": {
        "my_array": [],
        "description": "Very Interesting Description"
    }
}
```