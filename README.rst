mcinstall
=========

A script to quickly make/provision a fresh Miniconda installation from scratch.

The goal of this script is to quickly install a fresh Miniconda across different
operating systems and use it in a CI/CD context, too. It will download a Miniconda
binary based on your operating system, unpack the binary and install it locally.
It was tested on MacOS and Linux ok, has decent Windows support and also aims to
support ARM6 and ARM7 on the Raspberry Pi via the (sadly no longer maintained)
[Berryconda](https://github.com/jjhelmus/berryconda/releases).

This script has no external dependencies, but expects to be run with Python 3.6+.

N.B. This project is often updated online which is why its git history might look
strange...

Installation
------------

For now you can install and uninstall this like the following without cloning
the repo::

     pip3 install -e git+https://github.com/deeplook/mcinstall#egg=mcinstall
     pip3 uninstall mcinstall

If you clone the repo locally you can also install and uninstall like this::

     git clone https://github.com/deeplook/mcinstall.git
     cd mcinstall
     pip3 install -e .
     pip3 uninstall mcinstall

Sample Usage
------------

If you run it like this::

    mcinstall ~/Downloads/mc3

it will run a command like this on macOS (using some defaults and decent
system introspection)::

    bash Miniconda3-latest-MacOSX-x86_64.sh -b -f -p ~/Downloads/mc3

This can be used then with a command like this::

    source ~/Downloads/mc3/bin/activate

Windows Example:

On Windows if you run like this::

    mcinstall %USERPROFILE%\downloads\mc3

it will run a command like this::

    start /wait "" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%USERPROFILE%\downloads\mc3

This can be used then with command like this::

    %USERPROFILE%\mc3\condabin\activate

Suggested test::

    mcinstall --verbose --pip-dependencies jupyter,torch ~/Downloads/torchy
    source ~/Downloads/torchy/bin/activate
    python -c "import torch; print('ok')"

Suggested test dependencies files::

    $ more ~/Downloads/reqs.txt
    asciinema
    torch
    torchvision

    $ more ~/Downloads/env.yml
    name: test
    channels:
      - conda-forge
    dependencies:
      - voila

Sample run (replaced home directory with ``~`` manually)::

    $ mcinstall --verbose --pip-dependencies jupyter,torch ~/Downloads/torchy
    Making directory ~/Downloads/torchy.
    Downloading https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh ...
    Copying to ~/Downloads/Miniconda3-latest-MacOSX-x86_64.sh ...
    Running command: bash ~/Downloads/Miniconda3-latest-MacOSX-x86_64.sh -b -f -p ~/Downloads/torchy
    PREFIX=~/Downloads/torchy
    Unpacking payload ...
    Collecting package metadata (current_repodata.json): ...working... done
    Solving environment: ...working... done

    [...]

    Preparing transaction: ...working... done
    Executing transaction: ...working... done
    installation finished.

    Running command: ~/Downloads/torchy/bin/pip install jupyter
    [...]

    Running command: ~/Downloads/torchy/bin/pip install torch
    [...]

    Run this to start using your fresh Miniconda: "source ~/Downloads/torchy/bin/activate".

Sample log file (``mcinstall.log``)::

    wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    mv Miniconda3-latest-MacOSX-x86_64.sh ~/Downloads/Miniconda3-latest-MacOSX-x86_64.sh
    bash ~/Downloads/Miniconda3-latest-MacOSX-x86_64.sh -b -f -p ~/Downloads/torchy
    source ~/Downloads/torchy/bin/activate
    ~/Downloads/torchy/bin/pip install jupyter
    ~/Downloads/torchy/bin/pip install torch

TO DO
-----

- improve logging executed commands to reproduce them as a shell script
- add self.clean_dest_path to MinicondaInstaller.__init__
- same with self.download_path
- consolidate Windows support
- improve configuration
- turn this into a nice package
- make a sample screencast with asciinema
