#!/usr/bin/env python

from setuptools import setup

setup(name='mcinstall',
      version='0.1.0',
      description='Install and provision a fresh Miniconda distribution from scratch.',
      author='Dinu Gherman',
      url='https://github.com/deeplook/mcinstall',
      py_modules=['mcinstall'],
      entry_points={
        'console_scripts': ['mcinstall=mcinstall:main']})
