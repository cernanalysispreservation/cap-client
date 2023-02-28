## Installation

The cap-client supports Python versions `2.7` and `3` and is available on PyPI. You can install it using the following command:

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command pip install cap-client]
```

> Note: If you want latest developement edition, with latest updates, follow from our `master` branch
> ```
> git clone https://github.com/cernanalysispreservation/cap-client.git
> cd cap-client
> pip install .
> ```
> After a succesfull installation, you will have the `cap-client` command


## Usage

The cap-client is designed to communicate with a CERN Analysis Preservation (CAP) server instance. You can use the [CERN Analysis Preservation Production Server](https://analysispreservation.cern.ch/), which comes with the latest production version of CAP. All further descriptions and references link to this production instance.

In order to communicate with the server, you should first generate your personal access token [here]({{book.CAP_BASE_URL}}/settings), after logging in with your CERN credentials, and export it to your local environment.

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command export CAP_ACCESS_TOKEN=<generated-access-token>]
```

Alternatively, in case you want to explore and experiment with `cap-client`, you can export and use our development server instance (which you can access [here]({{book.CAP_BASE_URL}}/settings) in order to get the assorted development server token).

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command export CAP_SERVER_URL=https://test-cap-instance.cern.ch/]
```

After setting up the environment variables, you are ready to start using CAP for various tasks, which will be described in the following chapters. In case you need a quick rundown of the command groups (or specific instructions for each command), you can use the `--help` argument:

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client --help]
Usage: cap-client [OPTIONS] COMMAND [ARGS]...

  CAP command line interface.

Options:
  -v, --verbose                      Verbose output
  -l, --loglevel [error|debug|info]  Sets log level
  --version                          Show the version and exit.
  --help                             Show this message and exit.

Commands:
  analysis      Manage your analysis.
  files         Manage analysis files.
  metadata      Manage analysis metadata.
  permissions   Manage analysis permissions.
  repositories  Manage analysis repositories and webhooks.
```
