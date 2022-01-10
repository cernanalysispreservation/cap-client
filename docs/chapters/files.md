## Files

The `files` command group allows users to manage files attached to their analyses and upload local files and attach them to analysis. The supported commands are the following:

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
  remove    Remove a file from deposit with given PID.
  upload    Upload a file to your analysis.
```

### Download a file from an analysis

#### Description

- Allows the user to download a previously attached file to a specified analysis.
- The supported options are the following:

| Name               | Type   | Desc                                                  |
| :----------------- | :----- | :---------------------------------------------------- |
| FILENAME           | TEXT   | The name of the file to be downloaded  [required]     |
| --pid / -p         | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --output-file / -o | PATH   | Download file as                                      |

#### Usage

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

### Retrieve all the files of an analysis

#### Description

- Allows the user to get a list of the files attached to an analysis with a given PID.
- The supported options are the following:

| Name               | Type   | Desc                                                  |
| :----------------- | :----- | :---------------------------------------------------- |
| --pid / -p         | TEXT   | Your analysis PID (Persistent Identifier)  [required] |

#### Usage

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

### Remove a file from an analysis

#### Description

- Allows the user to get a list of the files attached to an analysis with a given PID.
- The supported options are the following:

| Name               | Type   | Desc                                                  |
| :----------------- | :----- | :---------------------------------------------------- |
| --pid / -p         | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files remove --pid <analysis-pid> FILENAME]
File FILENAME removed.
```

### Upload a file to an analysis

#### Description

- Allows the user to upload and attach a file to analysis or a whole directory as a tar.gz file.
- The command enables the user to upload a single file of any type, as well as a whole directory. After a prompt asks the user for confirmation, the directory will be zipped and uploaded as a `.tar.gz` file.
- To avoid the prompt and enable the usage of cap-client inside a CLI script, the flag `--yes-i-know` can be added.
- The supported options are the following:

| Name                   | Type   | Desc                                                         |
| :--------------------- | :----- | :----------------------------------------------------------- |
| FILE                   | TEXT   | The name of the file/s to be uploaded [required]             |
| --pid / -p             | TEXT   | Your analysis PID (Persistent Identifier)  [required]        |
| --output-filename / -o | PATH   | Upload file as..                                             |
| --yes-i-know           | FLAG   | Bypasses prompts..Say YES to everything                      |
| --dir-files / -df      | TEXT   | Upload all the files individually of the specified directory.|

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files upload --pid <analysis-pid> FILE1]
File File1 uploaded successfully.
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files upload --pid <analysis-pid> FILE1 FILE2]
File File1 uploaded successfully.
File File2 uploaded successfully.
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files upload --pid <analysis-pid> --yes-i-know DIR]
Directory DIR uploaded successfully.
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client files upload --pid <analysis-pid> --dir-files DIR]
File DIR/File1 uploaded successfully.
File DIR/File2 uploaded successfully.
...
```
