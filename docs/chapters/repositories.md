## Repositories

The `repositories` command group allows the user to manage the repositories attached to an analysis. The user can:
- retrieve the repositories attached to an analysis,
- upload a repository to an analysis using its GitHub/GitLab URL, and
- connect a repo to the analysis through webhooks.

The users can define release and push actions that will trigger an update to their analysis repository by leveraging the webhook API of GitHub/GitLab. That way, every time, e.g., a new release happens on a repo, the analysis repo will be updated, enabling the user to have the most up-to-date code saved to the CAP analysis.

Every time the repo is updated, a new `snapshot` of the repo will be created, which means that although the most recent version is readily available, older versions are also preserved.

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client repositories --help]
Usage: cap-client repositories [OPTIONS] COMMAND [ARGS]...

  Manage analysis repositories and webhooks.

Options:
  --help  Show this message and exit.

Commands:
  connect  Connect repository with your analysis.
  get      Get all repositories connected with your analysis.
  upload   Upload repository tarball to your analysis.
```

### Get the repositories connected to an analysis

#### Description

- Allows the user to retrieve connected repositories of analysis, including the different snapshots of every repo.
- Snapshot is the local copy of the repository created after an event triggered the specified webhook.
- The supported options are the following:

| Name                   | Type   | Desc                                                  |
| :--------------------- | :----- | :---------------------------------------------------- |
| --pid / -p             | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --with-snapshots / -ws | FLAG   | Show snapshots.                                       |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client repositories get --pid <analysis-pid>]
[{
    "branch": 'test',
    "event_type": "release",
    "host": "github.com",
    "id": 1,
    "name": "test-repo",
    "owner": "test-user"
}]
```

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client repositories get --pid <analysis-pid> --with-snapshots]
[{
    "branch": 'test',
    "event_type": "release",
    "host": "github.com",
    "id": 1,
    "name": "test-repo",
    "owner": "test-user",
    'snapshots': []
}]
```

### Upload a repository to an analysis

#### Description

- Allows the user to upload a repository and attach it to their analysis by providing the correct GitHub/GitLab URL.
- The supported options are the following:

| Name       | Type   | Desc                                                  |
| :--------- | :----- | :---------------------------------------------------- |
| URL        | TEXT   | The GitHub/GitLab url [required]                      |
| --pid / -p | TEXT   | Your analysis PID (Persistent Identifier)  [required] |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client repositories upload --pid <analysis-pid> https://github.com/test-user/test-repo]
Repository tarball was saved with your analysis files. (access using `cap-client files` methods)
```

### Connect a repository to an analysis

#### Description

- Allows the user to connect a repository to a specified analysis.
- The user can specify in which event the repo will get updated on the CAP analysis.
- The supported options are the following:

| Name       | Type   | Desc                                                  |
| :--------- | :----- | :---------------------------------------------------- |
| URL        | TEXT   | The GitHub/GitLab url [required]                      |
| --pid / -p | TEXT   | Your analysis PID (Persistent Identifier)  [required] |
| --event    | TEXT   | Download repository tarball on every (push / release) |

#### Usage

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client repositories connect --pid <analysis-pid> --event release https://github.com/test-user/test-repo]
Repository was connected with analysis.
Now on every release, we will attach the latest version to your analysis.
```
