mcinstall
=========

.. image:: https://img.shields.io/travis/deeplook/mcinstall/master.svg
  :target: https://travis-ci.org/deeplook/mcinstall

.. image:: https://img.shields.io/pypi/pyversions/mcinstall.svg
  :target: https://pypi.org/project/mcinstall

.. image:: https://img.shields.io/pypi/v/mcinstall.svg
  :target: https://pypi.org/project/mcinstall

.. image:: https://img.shields.io/pypi/status/mcinstall.svg
  :target: https://pypi.org/project/mcinstall

.. image:: https://img.shields.io/pypi/format/mcinstall.svg
  :target: https://pypi.org/project/mcinstall

.. image:: https://img.shields.io/pypi/l/mcinstall.svg
  :target: https://pypi.org/project/mcinstall
  
.. image:: https://img.shields.io/badge/platform-unix%20|%20win%20|%20osx%20|%20arm-informational.svg
  :target: https://pypi.org/project/mcinstall

.. image:: https://img.shields.io/badge/likes-Raspberry%20Pi-%23C51A4A?logo=raspberry%20pi
  :target: https://pypi.org/project/mcinstall

.. image:: https://img.shields.io/lgtm/alerts/g/deeplook/mcinstall.svg?logo=lgtm&logoWidth=18
  :target: https://lgtm.com/projects/g/deeplook/mcinstall/alerts/

.. image:: https://img.shields.io/lgtm/grade/python/g/deeplook/mcinstall.svg?logo=lgtm&logoWidth=18
  :target: https://lgtm.com/projects/g/deeplook/mcinstall/context:python

A script to quickly make/provision a fresh Miniconda installation from scratch.
     
The goal of this script is to quickly install a fresh Miniconda across different
operating systems and use it in a CI/CD context, too. It will download a Miniconda
binary based on your operating system, unpack the binary and install it locally.
It was tested on MacOS and Linux ok, has decent Windows support and also aims to
support ARM6 and ARM7 on the Raspberry Pi via `Berryconda 
<https://github.com/jjhelmus/berryconda/releases>`_ (sadly no longer maintained).

This script has no external dependencies, but expects to be run with Python 3.5+,
3.5 only because this is likely still the prevalent Python 3 version on Rasbian.

N.B. This project is often updated online which is why its git history might look
strange...

Installation
------------

Very briefly, it's ``pip install mcinstall``. More details are available in
`INSTALL.rst <INSTALL.rst>`_.

Sample Usage
------------

If you run it like this::

    mcinstall ~/Downloads/mc3

it will run a command like this on macOS (using some defaults and decent
system introspection) to create a conda base installation::

    bash Miniconda3-latest-MacOSX-x86_64.sh -b -f -p ~/Downloads/mc3

This can be activated then with a command like this::

    source ~/Downloads/mc3/bin/activate

Windows Example:

On Windows if you execute this command::

    mcinstall %USERPROFILE%\downloads\mc3

it will run a command like this::

    start /wait "" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%USERPROFILE%\downloads\mc3

This conda installation can be activated then with a command like this::

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
