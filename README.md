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
branchesdiff.cli with no commands show help information:

```bash
usage: branchesdiff.cli [-h] {update,generate} ...

Print differences between branches sisyphus and p10 in json format

positional arguments:
  {update,generate}
    update           Update packages metadata
    generate         Generate json with differences between branches

options:
  -h, --help         show this help message and exit

Version 1.0.0
```
commands description
* update 
  * download branches data and save it in os temp folder. File names are `p10.json` and `sisyphus.json`. If success prints `Update complete`.
* generate
  * Generates and prints to standard output json with differences information.
  
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
* using git: `git clone https://github.com/MakedonskyLF/test_cases.git`
* just download [zip archive](https://github.com/MakedonskyLF/test_cases/archive/refs/heads/main.zip)
  * unzip downloaded archive

#### Integrating with bash
You can put symlink for `branchesdiff.cli.py` in any folder from PATH variable.
Check you PATH variable: `echo $PATH`

Example output:
> **/home/paa/.local/bin**:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

Let assume what `branchesdiff.cli.py` located in `/home/paa/test/`
Than command for creating symlink:
> ln -s /home/paa/test/branchesdiff.cli.py /home/paa/.local/bin/branchesdiff.cli