#!/usr/bin/env python

import sys
from os.path import abspath, dirname, join

from setuptools import setup

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []
this_directory = abspath(dirname(__file__))
with open(join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mcinstall",
    version="0.3.0",
    description=(
        "Quick-install/provision a fresh Miniconda distribution from scratch."
    ),
    long_description_content_type="text/x-rst",
    long_description=long_description,
    author="Dinu Gherman",
    url="https://github.com/deeplook/mcinstall",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Installation/Setup",
    ],
    setup_requires=[] + pytest_runner,
    tests_require=["pytest"],
    py_modules=["mcinstall"],
    entry_points={"console_scripts": ["mcinstall=mcinstall:main"]},
)
