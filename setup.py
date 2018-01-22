#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pytest-sqlalchemy',
    license='MIT',
    description='pytest plugin with sqlalchemy related fixtures',
    #long_description=read("README.rst"),
    version='0.2.0',
    author='Torsten Irländer',
    author_email='torsten.irlaender@googlemail.com',
    url='http://github.com/toirl/pytest-sqlalchemy/',
    py_modules=['pytest_sqlalchemy'],
    entry_points={'pytest11': ['sqlalchemy = pytest_sqlalchemy']},
    install_requires=['pytest>=2.0', 'sqlalchemy', 'SQLAlchemy-Utils'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ]
)
