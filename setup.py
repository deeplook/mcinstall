#!/usr/bin/env python

import sys
from setuptools import setup

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

setup(
    name="mcinstall",
    version="0.3.0",
    description="Install and provision a fresh Miniconda distribution from scratch.",
    author="Dinu Gherman",
    url="https://github.com/deeplook/mcinstall",
    setup_requires=[] + pytest_runner,
    tests_require=["pytest"],
    py_modules=["mcinstall"],
    entry_points={"console_scripts": ["mcinstall=mcinstall:main"]},
)
