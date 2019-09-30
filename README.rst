mcinstall
=========

A script to quickly make/provision a fresh Miniconda installation from scratch.

This will download a Miniconda binary from https://repo.continuum.io/miniconda/
like https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh,
unpack and install it locally. It was tested on macOS and Linux ok, but will
fail on Windows (patches welcome).

This script has no external dependencies, but expects to be run with Python 3.

If you run it like this::

    python3 mcinstall.py ~/Downloads/mc3

it will run a command like this on macOS (using some defaults and decent
system introspection)::

    bash Miniconda3-latest-MacOSX-x86_64.sh -b -f -p ~/Downloads/mc3

This can be used then with a command like this::

    source ~/Downloads/mc3/bin/activate

Suggested test::

    python3 mcinstall.py --verbose --pip-dependencies jupyter,torch ~/Downloads/torchy
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

    $ python3 mcinstall.py --verbose --pip-dependencies jupyter,torch ~/Downloads/torchy
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
- support Windows
    - https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html
- improve configuration
