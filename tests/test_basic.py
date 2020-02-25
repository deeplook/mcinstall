"""
Test creating Miniconda installation and provisioning.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

from mcinstall import config, MinicondaInstaller


def test_show_config():
    print(json.dumps(config, indent=4))


def test_uname_m():
    out = subprocess.check_output(["uname", "-m"])
    print(out.decode("utf-8"))


def test_pip():
    verbose = True
    with tempfile.TemporaryDirectory() as tempdir:
        mci = MinicondaInstaller(tempdir, verbose=verbose)
        mci.download()
        mci.install_miniconda()
        mci.install_pip(dependencies=["geopy"])

        # Run Miniconda's Python  and import the installed dependency.
        cmd = [
            f"{tempdir}/bin/python", "-c",
            "import geopy; print('Imported geopy ' + geopy.__version__)"
        ]
        out = subprocess.check_output(cmd).decode("utf-8").strip()
        print(out)

    assert not os.path.exists(tempdir)


def test_conda():
    verbose = True
    with tempfile.TemporaryDirectory() as tempdir:
        mci = MinicondaInstaller(tempdir, verbose=verbose)
        mci.download()
        mci.install_miniconda()
        mci.install_conda(channel="conda-forge", dependencies=["numpy"])

        # Run Miniconda's Python  and import the installed dependency.
        cmd = [
            f"{tempdir}/bin/python", "-c",
            "import numpy; print('Imported numpy '+numpy.__version__)"
        ]
        out = subprocess.check_output(cmd).decode("utf-8").strip()
        print(out)

    assert not os.path.exists(tempdir)
