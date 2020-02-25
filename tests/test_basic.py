"""
Test creating Miniconda installation and provisioning.
"""

import json
import os
import subprocess
import sys
import tempfile

from mcinstall import config, MinicondaInstaller


def test_show_config():
    print(json.dumps(config, indent=4))


def test_uname_m():
    out = subprocess.check_output(["uname", "-m"])
    print(out.decode("utf-8"))


def test_pip_sklearn():
    verbose = True
    with tempfile.TemporaryDirectory() as tempdir:
        mci = MinicondaInstaller(tempdir, verbose=verbose)
        mci.download()
        mci.install_miniconda()
        mci.install_pip(dependencies=["scikit-learn"])

        # Find Python version used by the installed Miniconda, and add it to the
        # search path:
        cmd = [
            f"{tempdir}/bin/python", "-c",
            '''import sys;v='.'.join(map(str,sys.version_info[:2]));print('python'+v)'''
        ]
        out = subprocess.check_output(cmd)
        py_version = out.decode("utf-8").strip()
        sys.path.insert(0, f"{tempdir}/lib/{py_version}/site-packages")

        # Import the installed test package.
        import sklearn
        print(f"Sklearn location: {sklearn.__file__}")
        print(f"Sklearn version: {sklearn.__version__}")

    assert not os.path.exists(tempdir)
