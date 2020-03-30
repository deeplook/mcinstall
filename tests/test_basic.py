"""
Test creating Miniconda installation and provisioning.
"""

import json
import os
import re
import subprocess
import sys
import pytest
import platform
import tempfile
import shutil

from mcinstall import MinicondaInstaller, config


def test_show_config():
    print(json.dumps(config, indent=4))


@pytest.mark.skipif(platform.system() == "Windows", reason="uname command will not run on Windows.")
def test_uname_m():
    out = subprocess.check_output(["uname", "-m"])
    print(out.decode("utf-8"))


def test_install_dependencies():
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            mci = MinicondaInstaller(tempdir, verbose=True)
            mci.download()
            mci.install_miniconda()
            mci.update_miniconda_base()
            mci.install_pip(dependencies=["geopy"])
            mci.install_conda(channel="conda-forge", dependencies=["pyyaml"])

            if platform.system() == "Windows":
                py_exe = "%s\\python" % tempdir
            else:
                py_exe = "%s/bin/python" % tempdir

            # Run Miniconda's Python and import the installed dependencies.
            for pkg_name in ["geopy", "pyyaml"]:
                if pkg_name == "pyyaml":
                    pkg_name = "yaml"
                if platform.system() == "Windows":
                    cmd = [
                        "%s\\condabin\\activate"%(tempdir),
                        "&&",
                        py_exe,
                        "-c",
                        '''import %s; print("%s %%s ok" %% %s.__version__)''' % \
                            (pkg_name, pkg_name, pkg_name)
                    ]
                else:
                    cmd = [
                        py_exe,
                        "-c",
                        '''import %s; print("%s %%s ok" %% %s.__version__)''' % \
                            (pkg_name, pkg_name, pkg_name)
                    ]

                if platform.system() == "Windows":
                    out = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                else:
                    out = subprocess.check_output(cmd).decode("utf-8").strip()
                print(out)
                if platform.system() == "Windows":
                    assert re.search("%s .+ ok" % pkg_name, out)
                else:
                    assert re.match("%s .+ ok" % pkg_name, out)
    except NotADirectoryError as err:
        print(err)
        shutil.rmtree(tempdir)

    print()
    assert not os.path.exists(tempdir)


def test_install_dependencies_index_url():
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            mci = MinicondaInstaller(tempdir, verbose=True)
            mci.download()
            mci.install_miniconda()
            mci.update_miniconda_base()
            mci.install_pip(dependencies=["pypi_pkg_test"], index_url="https://test.pypi.org/simple/")

            if platform.system() == "Windows":
                py_exe = "%s\\python" % tempdir
            else:
                py_exe = "%s/bin/python" % tempdir

            # Run Miniconda's Python and import the installed dependencies.
            for pkg_name in ["pypi_pkg_test"]:
                cmd = [
                    py_exe,
                    "-c",
                    '''import %s; print("%s %%s ok" %% %s)''' % \
                    (pkg_name, pkg_name, pkg_name)
                ]
                if platform.system() == "Windows":
                    out = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                else:
                    out = subprocess.check_output(cmd).decode("utf-8").strip()
                print(out)
                assert re.match("%s .+ ok" % pkg_name, out)
    except NotADirectoryError:
        shutil.rmtree(tempdir)
    print()
    assert not os.path.exists(tempdir)


def test_install_dependencies_extra_index_url():
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            mci = MinicondaInstaller(tempdir, verbose=True)
            mci.download()
            mci.install_miniconda()
            mci.update_miniconda_base()
            mci.install_pip(dependencies=["pypi_pkg_test"], index_url="https://test.pypi.org/simpletest/", extra_index_url="https://test.pypi.org/simple/")

            if platform.system() == "Windows":
                py_exe = "%s\\python" % tempdir
            else:
                py_exe = "%s/bin/python" % tempdir

            # Run Miniconda's Python and import the installed dependencies.
            for pkg_name in ["pypi_pkg_test"]:
                cmd = [
                    py_exe,
                    "-c",
                    '''import %s; print("%s %%s ok" %% %s)''' % \
                    (pkg_name, pkg_name, pkg_name)
                ]
                if platform.system() == "Windows":
                    out = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                else:
                    out = subprocess.check_output(cmd).decode("utf-8").strip()
                print(out)
                assert re.match("%s .+ ok" % pkg_name, out)
    except NotADirectoryError:
        shutil.rmtree(tempdir)
    print()
    assert not os.path.exists(tempdir)


def test_install_dependencies_extra_index_urls():
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            mci = MinicondaInstaller(tempdir, verbose=True)
            mci.download()
            mci.install_miniconda()
            mci.update_miniconda_base()
            mci.install_pip(dependencies=["pypi_pkg_test"], index_url="https://test.pypi.org/simpletest/", extra_index_url="https://test.pypi.org/simpletest1/, https://test.pypi.org/simple/")

            if platform.system() == "Windows":
                py_exe = "%s\\python" % tempdir
            else:
                py_exe = "%s/bin/python" % tempdir

            # Run Miniconda's Python and import the installed dependencies.
            for pkg_name in ["pypi_pkg_test"]:
                cmd = [
                    py_exe,
                    "-c",
                    '''import %s; print("%s %%s ok" %% %s)''' % \
                    (pkg_name, pkg_name, pkg_name)
                ]
                if platform.system() == "Windows":
                    out = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                else:
                    out = subprocess.check_output(cmd).decode("utf-8").strip()
                print(out)
                assert re.match("%s .+ ok" % pkg_name, out)
    except NotADirectoryError:
        shutil.rmtree(tempdir)
    print()
    assert not os.path.exists(tempdir)
