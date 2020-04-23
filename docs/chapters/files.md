## Files

The `files` command group allows the user to manage files attached to their analyses, as well as upload local files and attach them to an analysis.

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files --help]
Usage: cap-client files [OPTIONS] COMMAND [ARGS]...

  Manage analysis files.

Options:
  --help  Show this message and exit.

Commands:
  download  Download file uploaded with given deposit.
  get       Get list of files attached to analysis with given PID.
  remove    Removefile from deposit with given pid.
  upload    Upload a file to your analysis.
```


#### Download a file from an analysis

**Description:**

Allows the user to download a file, that was previously attached to a specified analysis.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files download --pid <analysis-pid> FILENAME]
File saved as FILENAME.
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files download --pid <analysis-pid> --output-file dir/NEWFILE FILENAME]
File saved as dir/NEWFILE.
```

**Options:**

| Name               | Type   | Desc                                                  |
| :----------------- | :----- | :---------------------------------------------------- |
| FILENAME           | TEXT   | The name of the file to be downloaded  [required]     |
| --pid / -p         | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --output-file / -o | PATH   | Download file as                                      |


#### Retrieve all the files of an analysis

**Description:**

Allows the user to get a list of the files, attached to an analysis with a given PID.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files get --pid <analysis-pid>]
[
    {
        "id": "c033caa6-a97e-4f10-92e8-50193eebb6c5",
        "filename": "FILENAME",
        "filesize": 10,
        "checksum": "md5:5065fe1d609d403918ac99b172b88ace"
    }
]
```

**Options:**

| Name               | Type   | Desc                                                  |
| :----------------- | :----- | :---------------------------------------------------- |
| --pid / -p         | TEXT   | Your analysis PID (Persistent Identifier)  [required] |


#### Remove a file from an analysis

**Description:**

Allows the user to get a list of the files, attached to an analysis with a given PID.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files remove --pid <analysis-pid> FILENAME]
File FILENAME removed.
```

**Options:**

| Name               | Type   | Desc                                                  |
| :----------------- | :----- | :---------------------------------------------------- |
| --pid / -p         | TEXT   | Your analysis PID (Persistent Identifier)  [required] |


#### Upload a file to an analysis

**Description:**

Allows the user to upload and attach a file to an analysis, or a whole directory as a tar.gz file.

**Usage:**

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files upload --pid <analysis-pid> FILE]
File uploaded successfully.
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files upload --pid <analysis-pid> --yes-i-know DIR]
File uploaded successfully.
```

**Extended Description:**

The command enables the user to upload a single file of any type, as well as a whole directory. After a prompt asks the user for confirmation, the directory will be zipped and uploaded as a `.tar.gz` file. In order to avoid the prompt, and enable the usage of CAP-Client inside a cli script, the flag `--yes-i-know` can be added.

**Options:**

| Name                   | Type   | Desc                                                  |
| :--------------------- | :----- | :---------------------------------------------------- |
| FILE                   | TEXT   | The name of the file to be downloaded  [required]     |
| --pid / -p             | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --output-filename / -o | PATH   | Upload file as                                        |
| --yes-i-know           | FLAG   | Bypasses prompts..Say YES to everything               |
