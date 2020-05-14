#! /usr/bin/env python3

"""
A script to quickly make/provision a fresh Miniconda installation from scratch.

This downloads a Miniconda binary e.g. from https://repo.continuum.io/miniconda/
like https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh for
MacOS or https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
for Windows, and unpacks and installs it locally.

This is tested on MacOS, Linux and Windows.

For additional information please read the README! ;)
"""

import argparse
import os
import platform
import re
import sys
from pathlib import Path
from subprocess import PIPE, Popen, check_output
from typing import List, Optional
from urllib import request

__version__ = "0.3.1"
__license__ = "MIT"


# config data
config = dict(
    mc_base_url="https://repo.continuum.io/miniconda/",
    mc_name="Miniconda3",
    mc_version="latest",
    machine=platform.machine(),
    system=platform.system(),
    downloads_dir="~/Downloads",
    log_path="./mcinstall.log",
)

# derived config data
if config["system"] == "Darwin":
    config["system"] = "MacOSX"

known_systems = ["MacOSX", "Linux", "Windows"]

if config["system"] in known_systems:
    if config["system"] == "Windows":
        ext = "exe"
        config["machine"] = "x86_64"
    else:
        ext = "sh"

    if re.match("armv[67]l", config["machine"]):
        config["mc_base_url"] = (
            "https://github.com/jjhelmus/berryconda"
            "/releases/download/v2.0.0/"
        )
        config["mc_name"] = "Berryconda3"
        config["mc_version"] = "2.0.0"

    config["mc_blob_name"] = "%s-%s-%s-%s.%s" % (
        config["mc_name"],
        config["mc_version"],
        config["system"],
        config["machine"],
        ext,
    )


class MinicondaInstaller:
    """A tiny installer to bring you up to Python/Pip/Conda speed in seconds.

    This is mainly meant to install a fresh Miniconda distribution. It also
    allows to provision the installed base environment with additional packages
    via ``pip`` or ``conda``.

    N.B.:

    - Dependencies specified via ``conda`` environment files will not be
      available together with dependencies specified separately via ``pip``!
    """

    def __init__(self, dest_path: str, verbose: bool = False):
        self.dest_path = dest_path
        self.verbose = verbose
        self.installed_ok = False
        self.clean_dest_path = Path(dest_path).expanduser().absolute()
        self.download_path = (
            Path(config["downloads_dir"]).expanduser().absolute()
        )

    def __del__(self):
        if self.verbose and self.installed_ok:
            if config["system"] == "Windows":
                cmd = r"%s\condabin\activate" % self.clean_dest_path
            else:
                cmd = "source %s/bin/activate" % self.clean_dest_path
            print('Run this to start using your fresh Miniconda: "%s".' % cmd)

    def log(self, command: str):
        """Logger method to log results to ``log_path`` from ``config``.

        :param command: The shell command to add to the logfile.
        """
        log_path = Path(config["log_path"]).expanduser().absolute()
        with log_path.open("a") as f:
            f.write("%s\n" % command)

    def download(self):
        """Download Miniconda locally at desired destination.
        """
        if not self.clean_dest_path.exists():
            if self.verbose:
                print("Making directory %s." % self.clean_dest_path)
            self.clean_dest_path.mkdir(parents=True)

        if not self.download_path.exists():
            if self.verbose:
                print("Making directory %s." % self.download_path)
            self.download_path.mkdir()

    def install_miniconda(self):
        """Install Miniconda locally at desired destination.

        :raises ValueError: Is raised if the download fails.
        """
        dest_path = self.clean_dest_path
        mc_blob_path = self.download_path / config["mc_blob_name"]
        if not mc_blob_path.exists():
            url = config["mc_base_url"] + config["mc_blob_name"]
            if self.verbose:
                print("Downloading %s ..." % url)
            user_agent = "Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36"
            headers = {"User-Agent": user_agent}
            req = request.Request(url, headers=headers)
            resp = request.urlopen(req)
            self.log("wget %s" % url)
            if resp.status >= 400:
                msg = "Cannot download %s. Verify URL components!" % url
                raise ValueError(msg)
            mc_blob = resp.read()
            if self.verbose:
                print("Copying to %s ..." % mc_blob_path)
            mc_blob_path.write_bytes(mc_blob)
            self.log("mv %s %s" % (config["mc_blob_name"], mc_blob_path))

        if not (
            (dest_path / "bin" / "conda").exists()
            or (dest_path / "condabin" / "conda.bat").exists()
        ):
            if config["system"] == "Windows":
                cmd = (
                    'start /wait "" %s /InstallationType=JustMe /RegisterPython=0 /S /D=%s'
                    % (mc_blob_path, dest_path)
                )
                with open("temp.bat", "w") as fh:
                    fh.write(cmd)
                p = Popen("temp.bat", stdout=PIPE)
                stdout, stderr = p.communicate()
                print(p.returncode)
                if p.returncode != 0:
                    self.log(str(stdout))
                    self.log(str(stderr))
                    raise ValueError("Installation failed...")
                else:
                    os.remove("temp.bat")
            else:
                cmd = "bash %s -b -f -p %s" % (mc_blob_path, dest_path)
                if self.verbose:
                    print("Running command: %s" % cmd)
                output = check_output(cmd.split())
                print(output.decode("utf8"))
            self.log(cmd)
        if config["system"] == "Windows":
            cmd = r"%s\condabin\activate" % dest_path
        else:
            cmd = "source %s/bin/activate" % dest_path
        self.log(cmd)

        self.installed_ok = True

    def update_miniconda_base(self):
        """
        Update conda post installation.
        """
        if config["system"] == "Windows":
            cmd = r"%s\condabin\conda update -y -n base -c defaults conda" \
                  % self.clean_dest_path
            if self.verbose:
                print("Running command: %s" % cmd)
            output = check_output(cmd.split(), shell=True)
        else:
            cmd = r"%s/bin/conda update -y -n base -c defaults conda" % self.clean_dest_path
            if self.verbose:
                print("Running command: %s" % cmd)
            output = check_output(cmd.split())
        self.log(cmd)
        print(output.decode("utf8"))

    def install_pip(
        self,
        dependencies: Optional[List[str]] = None,
        dependencies_path: Optional[str] = None,
        index_url: Optional[str] = None,
        extra_index_url: Optional[List[str]] = None
    ):
        """Pip-install dependencies.

        Dependencies can be specified in a list of package names or
        a dependencies file.

        :param dependencies: A list of dependency names.
        :param dependencies_path: A file path with one dependency name per line.
        :param index_url: URL for package index.
        :param extra_index_url: Additional URL for package index.
        """
        dep_path = dependencies_path
        dest_path = self.clean_dest_path
        pip_cmd = "pip install"
        if index_url:
            pip_cmd = r"%s --index-url %s" % (pip_cmd, index_url)
        if extra_index_url:
            extra_index_urls = extra_index_url.split(",")
            print(str(extra_index_urls))
            for url in extra_index_urls:
                pip_cmd = r"%s --extra-index-url %s" % (pip_cmd, url)

        for dep in dependencies or []:
            # This will give output earlier when installed individually.
            if config["system"] == "Windows":
                cmd = r"%s\condabin\activate && %s %s" % (
                    dest_path,
                    pip_cmd,
                    dep,
                )
                output = check_output(cmd.split(), shell=True)
            else:
                cmd = "%s/bin/%s %s" % (dest_path, pip_cmd, dep)
                output = check_output(cmd.split())
            if self.verbose:
                print("Running command: %s" % cmd)
            self.log(cmd)
            print(output.decode("utf8"))

        if dependencies_path:
            if config["system"] == "Windows":
                cmd = r"%s\condabin\activate && %s -r %s" % (
                    dest_path,
                    pip_cmd,
                    dep_path,
                )
                output = check_output(cmd.split(), shell=True)
            else:
                cmd = "%s/bin/%s -r %s" % (dest_path, pip_cmd, dep_path)
                output = check_output(cmd.split())
            if self.verbose:
                print("Running command: %s" % cmd)
            self.log(cmd)
            print(output.decode("utf8"))

    def install_conda(
        self,
        channel: str = "conda-forge",
        dependencies: Optional[List[str]] = None,
        dependencies_path: Optional[str] = None,
        environment_path: Optional[str] = None,
    ):
        """Conda-install dependencies.

        Dependencies can be specified in a list of package names or
        a dependencies file or a conda environment file (which will
        create a new environment).

        :param channel: The conda channel to fetch the packages from.
        :param dependencies: A list of dependency names.
        :param dependencies_path: A file path with one dependency name per line.
        :param environment_path: A file path for a conda environment file.
        """
        dep_path = dependencies_path
        env_path = environment_path
        dest_path = self.clean_dest_path

        for dep in dependencies or []:
            # This will give output earlier when installed individually.
            if config["system"] == "Windows":
                cmd = r"%s\condabin\conda install -y %s" % (dest_path, dep)
                output = check_output(cmd.split(), shell=True)
            else:
                cmd = "%s/bin/conda install -y -c %s %s" % (
                    dest_path,
                    channel,
                    dep,
                )
                output = check_output(cmd.split())
            if self.verbose:
                print("Running command: %s" % cmd)
            self.log(cmd)
            print(output.decode("utf8"))

        if dependencies_path:
            if config["system"] == "Windows":
                cmd = r"%s\condabin\conda install -y --file %s" % (
                    dest_path,
                    dep_path,
                )
                output = check_output(cmd.split(), shell=True)
            else:
                cmd = "%s/bin/conda install -y --file %s" % (
                    dest_path,
                    dep_path,
                )
                output = check_output(cmd.split())
            if self.verbose:
                print("Running command: cmd" % cmd)
            self.log(cmd)
            print(output.decode("utf8"))

        if environment_path:
            if config["system"] == "Windows":
                cmd = r"%s\condabin\conda env create --file %s" % (
                    dest_path,
                    env_path,
                )
                output = check_output(cmd.split(), shell=True)
            else:
                cmd = "%s/bin/conda env create --file %s" % (
                    dest_path,
                    env_path,
                )
                output = check_output(cmd.split())
            if self.verbose:
                print("Running command: %s" % cmd)
            self.log(cmd)
            print(output.decode("utf8"))


def main():
    """Main function called when used on the command-line.
    """
    systems = ", ".join(known_systems)
    desc = "Quick-install/provision a fresh Miniconda for %s." % systems
    p = argparse.ArgumentParser(description=desc)

    p.add_argument(
        "path",
        metavar="DEST_DIR",
        help="The destination directory (will be created if needed).",
    )
    p.add_argument(
        "--verbose", action="store_true", help="Output additional information."
    )
    p.add_argument(
        "--pip-dependencies",
        metavar="LIST",
        default="",
        help="Comma-separated list of pip requirements.",
    )
    p.add_argument(
        "--pip-dependencies-path",
        metavar="PATH",
        help="Path of a pip requirements file, usually named requirements.txt.",
    )
    p.add_argument(
        "--pip-index-url",
        metavar="URL",
        help="Base URL of the Python Package Index",
    )
    p.add_argument(
        "--pip-extra-index-url",
        metavar="URL",
        help="Extra URLs of package indexes to use in addition to --pip-index-url",
    )
    p.add_argument(
        "--conda-dependencies",
        metavar="LIST",
        default="",
        help="Comma-separated list of conda requirements.",
    )
    p.add_argument(
        "--conda-dependencies-path",
        metavar="PATH",
        help=(
            "Path of a conda dependencies file, usually named requirements.txt. "
            "(This is not for creating a conda environment "
            "with something like environment.yml!)"
        ),
    )
    p.add_argument(
        "--conda-environment-path",
        metavar="PATH",
        help="Path of a conda environment file, usually named environment.yml.",
    )

    if config["system"] not in known_systems:
        msg = (
            """Don't know how to handle operating system %s'. Want to provide a patch?"""
            % config["system"]
        )
        print(msg)
        sys.exit(0)

    args = p.parse_args()

    if args.path:
        inst = MinicondaInstaller(dest_path=args.path, verbose=args.verbose)
        inst.download()
        inst.install_miniconda()
        inst.update_miniconda_base()
        if args.pip_dependencies or args.pip_dependencies_path:
            inst.install_pip(
                dependencies=args.pip_dependencies.split(",")
                if args.pip_dependencies
                else None,
                dependencies_path=args.pip_dependencies_path,
                index_url=args.pip_index_url,
                extra_index_url=args.pip_extra_index_url
            )
        if (
            args.conda_dependencies
            or args.conda_dependencies_path
            or args.conda_environment_path
        ):
            inst.install_conda(
                dependencies=args.conda_dependencies.split(",")
                if args.conda_dependencies
                else None,
                dependencies_path=args.conda_dependencies_path,
                environment_path=args.conda_environment_path,
            )


if __name__ == "__main__":
    main()
