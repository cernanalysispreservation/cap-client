# Files

For all the file commands you will need to specify

`--pid | the PID of an analysis you want to list all the contained files.`

In case of additional arguments, they will be explained.


### List

You can list all the files from an analysis only if you have at least read access to it.

    $ cap-client files list --pid/-p <existing pid>
    e.g.
    $ cap-client files list -p 89b593c498874ec8bcafc88944c458a7

```json
[
    {
        "checksum": "md5:f0428126e7cf7b0d4af7091c68ae2a9f",
        "filename": "file.json",
        "filesize": 25,
        "id": "25852e50-be6d-47a5-897b-1f3df015fac7"
    },
    {
        "checksum": "md5:926fb9c44251d70614ee42d34c5365b6",
        "filename": "Receipt.pdf",
        "filesize": 160898,
        "id": "89743c9b-106d-4235-8e96-23a164c7b1f4"
    }
]
```


### Upload

You can upload a file to an analysis only if you have at least read access to it.

    $ cap-client files upload <file path> --pid/-p <existing pid>
    e.g.
    $ cap-client files upload file.json -p 89b593c498874ec8bcafc88944c458a7

    $ File uploaded successfully.


### Download

You can download a file of an analysis only if you have at least read access to it. You need to specify (in addition to pid):

`--output-file | save the downloaded file as <desired file name>`

    $ cap-client files download <file key> --output-file/-o <file name> --pid/-p <existing pid>
    e.g.
    $ cap-client files download file.json -o local_file.json -p 89b593c498874ec8bcafc88944c458a7

    $ File saved as local_file.json


### Remove

You can remove a file of an analysis only if you have at least read access to it.

    $ cap-client files remove <file path> --pid/-p <existing pid>
    e.g.
    $ cap-client files upload file.json -p 89b593c498874ec8bcafc88944c458a7

    $ File file.json removed.