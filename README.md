# Branchesdiff

- [Branchesdiff](#branchesdiff)
    - [Features of work](#features-of-work)
  - [Usage](#usage)
  - [Installation](#installation)
    - [Requirements](#requirements)
    - [Install](#install)
      - [Downloading](#downloading)
      - [Integrating with bash](#integrating-with-bash)

  
Software for check differences in branches sisyphus and p10:
- packages only in sisyphus
- packages only in p10
- packages with version-release greater in sisyphus than in p10

### Features of work
Downloaded branch data stored in system temp folder

## Usage
`branchesdiff.cli -h` show help information:

```bash
usage: branchesdiff.cli.py [-h] [-f FILE] [-v] [--dev DEV] [--stable STABLE] [--api API]

Report differences between development branch and stable branch in json format

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  output to file FILE
  -v, --verbose         print work log
  --dev DEV             development branch name
  --stable STABLE       stable branch name
  --api API             URL for API requests

Version 2.0.3
```

Development branch name, stable branch name and URL for API requests can be specified in config file `config.ini`.
For example `config.ini` can be:
```ini
[branchesdiff]
API_URL = https://rdb.altlinux.org/api/export/branch_binary_packages/
DEV_BRANCH = sisyphus
STABLE_BRANCH = p10
```

In case of error print error type and description. Set exit code to 1.

## Installation

### Requirements
- python3 3.9
- requests
  - can be installed by pip: `pip install requests`
- rpm-vercmp
  - can be installed by pip: `pip install rpm-vercmp`

### Install
#### Downloading
1. Download cli file: [branchesdiff.cli.py](https://github.com/MakedonskyLF/test_cases/raw/main/branchesdiff.cli.py)
2. Install dependencies: `python3 -m pip install --index-url https://test.pypi.org/simple/ branchesdiff`

#### Integrating with bash
You can put symlink for `branchesdiff.cli.py` in any folder from PATH variable.
Check you PATH variable: `echo $PATH`

Example output:
> **/home/paa/.local/bin**:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

Let assume what `branchesdiff.cli.py` located in `/home/paa/test/`
Than command for creating symlink:
> ln -s /home/paa/test/branchesdiff.cli.py /home/paa/.local/bin/branchesdiff.cli