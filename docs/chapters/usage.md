# Usage

This guide assumes that you have successfully installed the *cap-client* package, available on PyPI. If not, please follow the [installation](installation.md) instructions first.

The cap-client is designed to communicate with a *CERN Analysis Preservation (CAP)* server instance. You can use the [CERN Production Server](https://analysispreservation.cern.ch/), which comes with the most stable version of CAP. All further descriptions and references link to this production instance.  

In order to communicate with the server, you first need to generate a personal access token [here](https://analysispreservation-dev.cern.ch/settings). Afterwards, set the required environment variables for the cap-client. If you like to select a CAP server different than the production instance, you can change the URL here.

```bash
$ export CAP_SERVER_URL=https://analysispreservation.cern.ch/
$ export CAP_ACCESS_TOKEN=<your generated access token from server>
```

Note that *CAP_ACCESS_TOKEN* can also be passed as an argument in the command line interface. We will present the supported commands with some example outputs.


## Retrieve the current user information {#retrieve-user}

```bash
$ cap-client me
```

```json
{
    "collaborations": ["ATLAS", "LHCb", "CMS", "ALICE"],
    "id": 1,
    "email": "user@cern.ch"
}
```


### Get all types of analyses available {#get-all}

```bash
$ cap-client types
```

```bash
$ Available types:
        atlas-workflows
        alice-analysis
        atlas-analysis
        lhcb
        cms-questionnaire
        cms-analysis
```


### Get the schema of analysis type {#get-schema}

You can retrieve analysis schema details if you have read or write access to the analysis. For more information about JSON schema you can visit this [link](http://json-schema.org/). You need to specify

`--type | the type of an analysis.`

and use the command:

```bash
$ cap-client get-schema --type/t <type of analysis>
```
e.g.

```bash
$ cap-client get-schema --type lhcb
```

which returns

```json
{
    "general_title": {
        "type": "string"
    }
}
```


### Retrieve an analysis {#retrieve-analysis}

You can retrieve all analyses, for which you have either write or read access, using certain arguments to narrow down the search.

`--pid | the PID of an analysis.`

For all analyses with write access:
```bash
$ cap-client get
```
	
For all analyses with read access:
```bash
$ cap-client get --all
```

For an analysis with a specified PID
```bash
$ cap-client get --pid/-p <existing pid>
```

So in the case of a certain PID, we have:
```bash
$ cap-client get --pid 883090d3c1784aeabe9e23412a81239e
```

```json
{
    "pid": "883090d3c1784aeabe9e23412a81239e",
    "basic_info": {
        "abstract": "Example abstract",
        "people_info": [{
            "name": "John doe"
        }, {
            "name": "J doe"
        }],
        "analysis_number": "test"
    }
}
```


### Create an analysis {#create}

You can create a new analysis by specifying:

`--file | a file with the json data corresponding to the analysis JSON Schema.`

`--type | the type of analysis you want to create.`

If you don't know what is the type of analyses you want to create use this [link](#get-all-types-of-analyses-available)

You can create analyses that correspond to your affiliation with a collaboration. For example: if you are a member of the CMS collaboration, you can create analyses with type *cms-analysis* or *cms-questionnaire*.

**NOTE**: In order to upload a file or a repository in your analysis, you should specify it according to a specified schema. Let's say for example you have this schema in your JSON file:

```json
{
    "user_analysis": {
        "type": "object",
        "properties": {
            "basic_script": {
                "x-cap-file": {
                    "fetch_from": "/url",
                    "file_key": "/key"
                },
                "type": "object",
                "properties": {
                    "url": {
                        "pattern": "^(http|https|root)://",
                        "type": "string"
                    },
                    "version_id": {
                        "type": "string"
                    },
                    "key": {
                        "type": "string"
                    }
                }
            }
        },
        "title": "User Analysis"
    }
}
```

Then you should specify the link like this:

```json
{
    "user_analysis": {
        "basic_script": {
            "url": "https://gitlab.cern.ch/cap/test"
        }
    }
}
```

Another example could be:

    $ cap-client create --file/-f <file with JSON data>  --type/-t <type of analysis> 
    e.g.
	$ cap-client create --file test.json --type cms-analysis

```json
{
    "status": 200, 
    "data": {   
        "pid": "883090d3c1784aeabe9e23412a81239e",
        "basic_info": {
            "abstract": "Example abstract",
            "people_info": [{
                "name": "John doe"
            }, {
                "name": "J doe"
            }],
            "analysis_number": "test"
        }
    }
}
```


### Delete an analysis {#delete}

You can delete an existing analysis by using the following:

`--pid | the PID of an analysis.`

    $ cap-client delete --pid/-p <existing pid>
    e.g.
    $ cap-client delete --pid 4c734c3ae5b14a2195e3b17dc9ff63ae

```json   
{
    'status': 204, 
    'data': None
}
```


### Patch an analysis {#patch}

You can patch an existing analysis by using:

`--file | a file with the json data corresponding to the analysis JSON Schema.`

`--pid | the PID of an analysis.`

Example changes in JSON patch format:

```json
[{
    "op": "add",
    "path": "/basic_info/analysis_number",
    "value": "22"
}]
```

    $ cap-client patch --pid/-p <existing pid> --file/-f <file with JSON data>
    e.g.
    $ cap-client patch --pid 883090d3c1784aeabe9e23412a81239e --file test.json

```json
{
    "status": 200, 
    "data": {   
        "pid": "883090d3c1784aeabe9e23412a81239e",
        "basic_info": {
            "abstract": "Example abstract",
            "people_info": [{
                "name": "John doe"
            }, {
                "name": "J doe"
            }],
            "analysis_number": "test"
        }
    }
}
```


### Publish an analysis {#publish}

By publishing your analysis, you are allowing your collaboration to access its resources on CAP (internal access only). This is done by using the command `publish` and specifying.

`--pid | the PID of an analysis.`


    $ cap-client publish --pid/-p <existing pid>
    e.g.
    $ cap-client publish -p a85dc95be2a04d70973de8a39065fc8d

```json
{
    "updated": "2018-02-16T13:25:45.999349+00:00",
    "metadata": {
        "$schema": "https://ioanniss-mbp.dyndns.cern.ch:5000/schemas/deposits/records/lhcb-v0.0.1.json",
        "user_analysis": {
            "basic_script": {
                "source": {
                    "preserved": true
                }
            },
            "gitlab_link": {
                "source": {
                    "preserved": true
                }
            }
        },
        "general_title": "LHCb Analysis 16/02/2018, 14:21:00",
        "control_number": "2"
    },
    "pid": "a85dc95be2a04d70973de8a39065fc8d",
    "created": "2018-02-16T13:21:10.968585+00:00"
}
```


### Clone an analysis {#clone}

You can clone an existing analysis by specifying

`--pid | the PID of the analysis you want to share.`

    $ cap-client clone --pid/-p <existing pid>
    e.g.
    $ cap-client clone -p 046ee5e83d084241a7b0767432e9682c

```json
{
    "updated": "2018-02-16T13:32:23.749106+00:00",
    "metadata": {
        "$schema": "https://ioanniss-mbp.dyndns.cern.ch:5000/schemas/deposits/records/atlas-analysis-v0.0.1.json",
        "general_title": "ATLAS Analysis 16/02/2018, 14:31:20",
        "basic_info": {
            "analysis_title": "testing",
            "glance_id": "123"
        }
    },
    "pid": "046ee5e83d084241a7b0767432e9682c",
    "created": "2018-02-16T13:32:23.691479+00:00"
}
```
