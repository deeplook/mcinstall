#! /usr/bin/env python3

"""
A script to quickly make/provision a fresh Miniconda installation from scratch.

This will download a Miniconda binary from https://repo.continuum.io/miniconda/
like https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh,
unpack and install it locally. It was tested on macOS and Linux ok, but will
fail on Windows (patches welcome).

For additional information please read the README! ;)
"""

import sys
import pathlib
import platform
import argparse
import subprocess
from urllib import request
from typing import Optional, List


__version__ = '0.2.4'
__license__ = 'MIT'


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
known_systems = ["MacOSX", "Linux"]
if config["system"] in known_systems:
    config["mc_blob_name"] = (
         f"{config['mc_name']}-{config['mc_version']}-"
         f"{config['system']}-{config['machine']}.sh"
    )


class MinicondaInstaller:
    """A tiny installer to bring you up to Python/Pip/Conda speed in seconds.

    This is mainly meant to install a fresh Miniconda distribution. To add
    some convenience it also allows to provision the installation with some
    specified packages to be installed via pip or conda.

    N.B.:

    - Dependencies specified via conda environment files will not be available
      together with dependencies specified separately via pip!
    """

    def __init__(self, dest_path: str, verbose: bool = False):
        self.dest_path = dest_path
        self.verbose = verbose
        self.installed_ok = False

    def __del__(self):
        if self.verbose and self.installed_ok:
            clean_dest_path = pathlib.PosixPath(self.dest_path).expanduser().absolute()
            cmd = f"source {clean_dest_path}/bin/activate"  # not yet for Windows...
            print(f'Run this to start using your fresh Miniconda: "{cmd}".')

    def log(self, command: str):
        log_path = pathlib.PosixPath(config['log_path']).expanduser().absolute()
        with log_path.open("a") as f:
            f.write(f"{command}\n")

    def download(self, dest_path: str, verbose: bool = False):
        """
        Download Miniconda locally at desired destination.
        """
        clean_dest_path = pathlib.PosixPath(dest_path).expanduser().absolute()
        if not clean_dest_path.exists():
            if verbose:
                print(f"Making directory {clean_dest_path}.")
            clean_dest_path.mkdir(parents=True)

        download_path = (
            pathlib.PosixPath(config["downloads_dir"]).expanduser().absolute()
        )
        if not download_path.exists():
            if verbose:
                print(f"Making directory {download_path}.")
            download_path.mkdir()

    def install_miniconda(self, dest_path: str, verbose: bool = False):
        """
        Install Miniconda locally at desired destination.
        """
        clean_dest_path = pathlib.PosixPath(dest_path).expanduser().absolute()
        download_path = (
            pathlib.PosixPath(config["downloads_dir"]).expanduser().absolute()
        )

        mc_blob_path = download_path / config["mc_blob_name"]
        if not mc_blob_path.exists():
            url = f"{config['mc_base_url']}{config['mc_blob_name']}"
            if verbose:
                print(f"Downloading {url} ...")
            resp = request.urlopen(url)
            self.log(f'wget {url}')
            if resp.status >= 400:
                msg = f"Cannot download {url}. Verify URL components!"
                raise ValueError(msg)
            mc_blob = resp.read()
            if verbose:
                print(f"Copying to {mc_blob_path} ...")
            mc_blob_path.write_bytes(mc_blob)
            self.log(f"mv {config['mc_blob_name']} {mc_blob_path}")
        if not (clean_dest_path / "bin" / "conda").exists():
            exec_cmd = f"bash {mc_blob_path} -b -f -p {clean_dest_path}"  # Windows?
            if verbose:
                print(f"Running command: {exec_cmd}")
            output = subprocess.check_output(exec_cmd.split())
            self.log(exec_cmd)
            print(output.decode("utf8"))
    
        source_cmd = f"source {clean_dest_path}/bin/activate"  # not yet for Windows...
        self.log(source_cmd)

        self.installed_ok = True

    def install_pip(
        self,
        dependencies: Optional[List[str]] = None,
        dependencies_path: Optional[str] = None,
        verbose: bool = False,
    ):
        """
        Pip-install dependencies.

        Dependencies can be specified in a list of package names or a dependencies file.
        """
        clean_dest_path = pathlib.PosixPath(self.dest_path).expanduser().absolute()
        if dependencies:
            for dep in dependencies:
                # This will give output earlier when installed individually.
                install_cmd = f"{clean_dest_path}/bin/pip install {dep}"
                if verbose:
                    print(f"Running command: {install_cmd}")
                output = subprocess.check_output(install_cmd.split())
                self.log(install_cmd)
                print(output.decode("utf8"))
        if dependencies_path:
            install_cmd = f"{clean_dest_path}/bin/pip install -r {dependencies_path}"
            if verbose:
                print(f"Running command: {install_cmd}")
            output = subprocess.check_output(install_cmd.split())
            self.log(install_cmd)
            print(output.decode("utf8"))

    def install_conda(
        self,
        dependencies: Optional[List[str]] = None,
        dependencies_path: Optional[str] = None,
        environment_path: Optional[str] = None,
        verbose: bool = False,
    ):
        """
        Conda-install dependencies.

        Dependencies can be specified in a list of package names or a dependencies file
        or a conda environment file (which will create a new environment).
        """
        clean_dest_path = pathlib.PosixPath(self.dest_path).expanduser().absolute()
        if dependencies:
            for dep in dependencies:
                # This will give output earlier when installed individually.
                install_cmd = f"{clean_dest_path}/bin/conda install -y {dep}"
                if verbose:
                    print(f"Running command: {install_cmd}")
                output = subprocess.check_output(install_cmd.split())
                self.log(install_cmd)
                print(output.decode("utf8"))
        if dependencies_path:
            install_cmd = (
                f"{clean_dest_path}/bin/conda install -y --file {dependencies_path}"
            )
            if verbose:
                print(f"Running command: {install_cmd}")
            output = subprocess.check_output(install_cmd.split())
            self.log(install_cmd)
            print(output.decode("utf8"))
        if environment_path:
            install_cmd = (
                f"{clean_dest_path}/bin/conda env create --file {environment_path}"
            )
            if verbose:
                print(f"Running command: {install_cmd}")
            output = subprocess.check_output(install_cmd.split())
            self.log(install_cmd)
            print(output.decode("utf8"))


def main():
    """Main function called when used on the command-line.
    """
    systems = ", ".join(known_systems)
    desc = f'Quick-install a fresh Miniconda from {config["mc_base_url"]} for {systems}.'
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
        help="Comma-separated list of pip requirements.",
    )
    p.add_argument(
        "--pip-dependencies-path",
        metavar="PATH",
        help="Path of a pip requirements file, usually named requirements.txt.",
    )
    p.add_argument(
        "--conda-dependencies",
        metavar="LIST",
        help="Comma-separated list of conda requirements.",
    )
    p.add_argument(
        "--conda-dependencies-path",
        metavar="PATH",
        help=(
            "Path of a conda dependencies file, usually named requirements.txt. "
            "(This is not for creating a conda environment with something like environment.yml!)"
        ),
    )
    p.add_argument(
        "--conda-environment-path",
        metavar="PATH",
        help="Path of a conda environment file, usually named environment.yml.",
    )

    if config["system"] not in known_systems:
        msg = (
            f"""Don't know how to handle operating system '{config["system"]}'. """
            "Want to provide a patch?"
        )
        print(msg)
        sys.exit(0)

    args = p.parse_args()

    if args.path:
        inst = MinicondaInstaller(dest_path=args.path, verbose=args.verbose)
        inst.download(dest_path=args.path, verbose=args.verbose)
        inst.install_miniconda(dest_path=args.path, verbose=args.verbose)
        if args.pip_dependencies or args.pip_dependencies_path:
            inst.install_pip(
                dependencies=args.pip_dependencies.split(","),
                dependencies_path=args.pip_dependencies_path,
                verbose=args.verbose,
            )
        if (
            args.conda_dependencies
            or args.conda_dependencies_path
            or args.conda_environment_path
        ):
            inst.install_conda(
                dependencies=args.conda_dependencies.split(","),
                dependencies_path=args.conda_dependencies_path,
                environment_path=args.conda_environment_path,
                verbose=args.verbose,
            )


if __name__ == "__main__":
    main()
