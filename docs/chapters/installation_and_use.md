## Installation

CAP-client supports Python versions `2.7` and `3.5+`, and is available on PyPI. You can install it using the following command:

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command pip install cap-client]
```

## Usage

The cap-client is designed to communicate with a *CERN Analysis Preservation (CAP)* server instance. You can use the [CERN Analysis Preservation Production Server](https://analysispreservation.cern.ch/), which comes with the latest production version of CAP. All further descriptions and references link to this production instance.  

In order to communicate with the server, you first need to generate your personal access token [here](https://analysispreservation-dev.cern.ch/settings), after logging in with your CERN credentials, and export it to your local environment.

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command export CAP_ACCESS_TOKEN=<generated-access-token>]
```

Alternatively, in case you want to explore and experiment with CAP-Client, you can export and use our development server instance (which you can access [here](https://analysispreservation-dev.cern.ch/settings) in order to get the assorted dev server token).

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command export CAP_SERVER_URL=https://analysispreservation-dev.cern.ch/]
```

After setting up the environment variables, you are ready to start using CERN Analysis Preservation for a variety of tasks, that will be described in the following chapters. In case you need a quick rundown of the command groups (or specific instructions for each command), you can use the `--help` argument:

```
**[terminal]
**[prompt user@pc]**[path ~]**[delimiter  $ ]**[command cap-client --help]
Usage: cap-client [OPTIONS] COMMAND [ARGS]...

  CAP command line interface.

Options:
  -v, --verbose                   Verbose output
  -l, --loglevel [error|debug|info]
                                  Sets log level
  --help                          Show this message and exit.

Commands:
  analysis      Manage your analysis.
  files         Manage analysis files.
  metadata      Manage analysis metadata.
  permissions   Manage analysis permissions.
  repositories  Manage analysis repositories and webhooks.
```