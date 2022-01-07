## Analysis

The `analysis` command group allows users to interact with their analyses through the terminal. The supported commands are the following:

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
  publish        Publish analysis with given PID.
  schema         Get JSON schema for analysis metadata.
  types          List all types of analysis you can create.
```

### Create an analysis
#### Description

- Allows the user to create a new analysis.
- To create a new analysis, the user needs to pass metadata in a JSON format (either from a file or directly from the terminal).
- The user needs to know the structure of the analysis, use the `analysis schema <your-analysis-type>` command to check for valid metadata.
- The supported options are the following:

| Name             | Type     | Desc                                                              |
| :--------------- | :------- | :---------------------------------------------------------------- |
| --json / -j      | TEXT     | JSON data from command line. (mutually exclusive with --jsonfile) |
| --jsonfile / -f  | FILENAME | JSON file. (mutually exclusive with --json)                       |
| --type / -t      | TEXT     | Type of analysis                                                  |
#### Usage

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

### Delete an analysis
#### Description

- Allows the user to delete an analysis draft.
- Note that the published analysis cannot be deleted.
- The supported options are the following:

| Name        | Type     | Desc                                                  |
| :---------- | :------- | :---------------------------------------------------- |
| --pid / -p  | TEXT     | Your analysis PID (Persistent Identifier)  [required] |
#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis delete --pid <analysis-pid>]
Analysis has been deleted
```

### Get drafts analyses
#### Description

- Allows retrieving one or more drafts analyses accessible to the user.
- The user can use the `get` command for three cases:
    - Retrieve all the draft analyses they have created.
    - Retrieve a single draft analysis by its PID.
    - Retrieve the draft analyses available to them (both created by them and given access to them by other users).
- The supported options are the following:

| Name            | Type     | Desc                                                                   |
| :-----------    | :------- | :--------------------------------------------------------------------- |
| --pid / -p      | TEXT     | Your analysis PID (Persistent Identifier)                              |
| --all           | FLAG     | Show all (not only yours)                                              |
| --query / -q    | TEXT     | A free text query (e.g `test` or `basic_info.analysis_title:test`)     |
| ----search / -s | TEXT     | Search through facets (e.g. `type=my-analysis`)                        |
| --type / -t     | TEXT     | Type of analysis                                                       |
| --sort          | TEXT     | The available values are "bestmatch", "mostrecent" [default=mostrecent]|
| --page          | INT      | Shows results on the specified page. [default=1]                       |
| --size          | INT      | Number of results on a page. [default=10]                              |
#### Usage

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

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get -q basic_info.analysis_title:test]
[
    {
        "created": "2022-01-05T08:57:08.661809+00:00",
        "metadata": {
            "basic_info": {
                "analysis_title": "Test"
            },
            "general_title": "Test Alice"
        },
        "pid": "3ec3b81e4f3643ce91e4396891dbcb03",
        "updated": "2022-01-05T08:57:22.734703+00:00"
    }
]
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis get -s type=alice-analysis]
[
    {
        "created": "2022-01-05T08:57:08.661809+00:00",
        "metadata": {
            "basic_info": {
                "analysis_title": "Test"
            },
            "general_title": "Test Alice"
        },
        "pid": "3ec3b81e4f3643ce91e4396891dbcb03",
        "updated": "2022-01-05T08:57:22.734703+00:00"
    }
]
```

### Get published analyses

#### Description

- Allows retrieving one or more published analyses accessible to the user.
- The user can use the `get-published` command for three cases
    - Retrieve all the published analyses they have created.
    - Retrieve a single published analysis by its PID.
    - Retrieve the published analyses available to them (both created by them and given access to them by other users).
- The supported options are the following:

| Name            | Type     | Desc                                                                   |
| :-----------    | :------- | :--------------------------------------------------------------------- |
| --pid / -p      | TEXT     | Your analysis PID (Persistent Identifier)                              |
| --all           | FLAG     | Show all (not only yours)                                              |
| --query / -q    | TEXT     | A free text query (e.g `test` or `basic_info.analysis_title:test`)     |
| ----search / -s | TEXT     | Search through facets (e.g. `type=my-analysis`)                        |
| --type / -t     | TEXT     | Type of analysis                                                       |
| --sort          | TEXT     | The available values are "bestmatch", "mostrecent" [default=mostrecent]|
| --page          | INT      | Shows results on the specified page. [default=1]                       |
| --size          | INT      | Number of results on a page. [default=10]                              |

#### Usage

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

### Retrieve the schema of an analysis type

#### Description

- Allows the user to retrieve the JSON schema of a specified analysis type.
- The supported options are the following:

| Name            | Type   | Desc                                                                    |
| :-------------- | :----- | :---------------------------------------------------------------------- |
| ANALYSIS_TYPE   | TEXT   | Type of analysis  [required]                                            |
| --version       | TEXT   | Version of the schema                                                   |
| --for-published | FLAG   | Show schema for published analysis (may be different from draft schema) |

#### Usage

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

### List available analysis types

#### Description

- The user can take a quick look at which analysis types are available to create a new analysis.

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client analysis types]
[
    "alice-analysis",
    "atlas-analysis".
    ...
]
```
