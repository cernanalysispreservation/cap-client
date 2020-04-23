## Analysis

The `analysis` command group allows the user to interact with their analyses through the terminal. The supported commands are the following:

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis --help]
Usage: cap-client analysis [OPTIONS] COMMAND [ARGS]...

  Manage your analysis.

Options:
  --help  Show this message and exit.

Commands:
  create         Create an analysis.
  delete         Delete your analysis.
  get            List your draft analysis.
  get-published  List your published analysis.
  publish        Publish analysis with given pid.
  schema         Get JSON schema for analysis metadata.
  types          List all types of analysis you can create.
```


#### List available analysis types

**Description:**

Using this command the user can take a quick look at which analysis types are available to them, in order to use it for the creation of a new analysis.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis types]
[
    "alice-analysis",
    "atlas-analysis".
    ...
]
```


#### Retrieve the schema of an analysis type

**Description:**

Allows the user retrieve the JSON schema of a specified analysis type.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis schema <ANALYSIS-TYPE>]
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "additionalProperties": true,
    "dependencies": {
        "analysis_reuse_mode": {
            "properties": {
    ...
}
```

**Options:**

| Name            | Type   | Desc                                                                    |
| :-------------- | :----- | :---------------------------------------------------------------------- |
| ANALYSIS_TYPE   | TEXT   | Type of analysis  [required]                                            |
| --version       | TEXT   | Version of the schema                                                   |
| --for-published | FLAG   | Show schema for published analysis (may be different than draft schema) |


#### Create a new analysis

**Description:**

Allows the user to create a new analysis.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis create --json {} --type <analysis-type>]
{
    "created": "2020-04-23T12:15:20.148324+00:00",
    "metadata": {},
    "pid": "b9e79ac9b8184ba3920e40daa694fcf7",
    "updated": "2020-04-23T12:15:20.555897+00:00"
}
```

**Extended Description:**

In order to create a new analysis, the user needs to pass metadata in a JSON format (either from a file or directly from the terminal). The user needs to know the structure of the analysis, in order to provide valid metadata (use `analysis schema <your-analysis-type>` command to check).

**Options:**

| Name        | Type     | Desc                                                              |
| :---------- | :------- | :---------------------------------------------------------------- |
| --json      | TEXT     | JSON data from command line. (mutually exclusive with --jsonfile) |
| --jsonfile  | FILENAME | JSON file. (mutually exclusive with --json)                       |
| --type / -t | TEXT     | Type of analysis                                                  |


#### Delete an analysis

**Description:**

Allows the user to delete an analysis draft.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis delete --pid <analysis-pid>]
Analysis has been deleted
```

**Options:**

| Name        | Type     | Desc                                                  |
| :---------- | :------- | :---------------------------------------------------- |
| --pid / -p  | TEXT     | Your analysis PID (Persistent Identifier)  [required] |


#### Publish an analysis

**Description:**

Allows the user to publish an analysis (removing it from the drafts), and get the new PID of the published analysis.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis publish --pid <analysis-pid>]
Your analysis has been published with PID: CAP.XXX.ABCD.ABCD
```

**Options:**

| Name        | Type     | Desc                                                  |
| :---------- | :------- | :---------------------------------------------------- |
| --pid / -p  | TEXT     | Your analysis PID (Persistent Identifier)  [required] |


#### Get analysis drafts

**Description:**

Allows the user to retrieve one or more analysis drafts, that they have access to.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get]
[
    {
        "created": "2020-04-23T12:15:20.148324+00:00",
        "metadata": {},
        "pid": "b9e79ac9b8184ba3920e40daa694fcf7",
        "updated": "2020-04-23T12:15:20.555897+00:00"
    }
]
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get --pid <analysis-pid>]
{
    "created": "2020-04-23T12:15:20.148324+00:00",
    "metadata": {},
    "pid": "kj8dhdc9b8184ba3920e40daa694fcf7",
    "updated": "2020-04-23T12:15:20.555897+00:00"
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get --all]
[
    {
        "created": "2020-04-23T12:15:20.148324+00:00",
        "metadata": {},
        "pid": "b9e79ac9b8184ba3920e40daa694fcf7",
        "updated": "2020-04-23T12:15:20.555897+00:00"
    },
    {
        "created": "2020-04-23T12:15:20.148324+00:00",
        "metadata": {},
        "pid": "kj8dhdc9b8184ba3920e40daa694fcf7",
        "updated": "2020-04-23T12:15:20.555897+00:00"
    }
]
```

**Extended Description:**

There are 3 separate situations, that the user may need to use the `get` command for:

1. Retrieve all the draft analysis they have created.
2. Retrieve a single draft analysis by its PID.
3. Retrieve the draft analyses available to them (both created by them and given access to them by other users).

The two additional arguments presented above, are used for cases 2 and 3.

**Options:**

| Name        | Type     | Desc                                      |
| :---------- | :------- | :---------------------------------------- |
| --pid / -p  | TEXT     | Your analysis PID (Persistent Identifier) |
| --all       | FLAG     | Show all (not only yours)                 |


#### Get published analyses

**Description:**

Allows the user to retrieve one or more published analyses, that they have access to.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get-published]
[
    {
        "created": "2020-04-23T12:15:20.148324+00:00",
        "metadata": {},
        "pid": "b9e79ac9b8184ba3920e40daa694fcf7",
        "recid": "CAP.XXX.ABCD.ABCD",
        "updated": "2020-04-23T12:15:20.555897+00:00"
    }
]
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get-published --pid <analysis-pid>]
{
    "created": "2020-04-23T12:15:20.148324+00:00",
    "metadata": {},
    "pid": "kj8dhdc9b8184ba3920e40daa694fcf7",
    "recid": "CAP.XXX.ABCD.ABCD",
    "updated": "2020-04-23T12:15:20.555897+00:00"
}
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get-published --all]
[
    {
        "created": "2020-04-23T12:15:20.148324+00:00",
        "metadata": {},
        "pid": "b9e79ac9b8184ba3920e40daa694fcf7",
        "recid": "CAP.XXX.ABCD.ABCD",
        "updated": "2020-04-23T12:15:20.555897+00:00"
    },
    {
        "created": "2020-04-23T12:15:20.148324+00:00",
        "metadata": {},
        "pid": "kj8dhdc9b8184ba3920e40daa694fcf7",
        "recid": "CAP.XXX.FGRE.KJHN",
        "updated": "2020-04-23T12:15:20.555897+00:00"
    }
]
```

**Extended Description:**


There are 3 separate situations, that the user may need to use the `get-published` command for:

1. Retrieve all the published analysis they have created.
2. Retrieve a single published analysis by its PID.
3. Retrieve the published analyses available to them (both created by them and given access to them by other users).

The two additional arguments presented above, are used for cases 2 and 3.

**Options:**

| Name        | Type     | Desc                                      |
| :---------- | :------- | :---------------------------------------- |
| --pid / -p  | TEXT     | Your analysis PID (Persistent Identifier) |
| --all       | FLAG     | Show all (not only yours)                 |