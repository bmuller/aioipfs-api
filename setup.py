#!/usr/bin/env python
from setuptools import setup, find_packages
import aioipfs_api

# read the contents of the README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aioipfs-api",
    version=aioipfs_api.__version__,
    description="Python 3 async client for interacting with the IPFS HTTP API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/aioipfs-api",
    packages=find_packages(),
    install_requires=["aiohttp>=3.4.0", "yarl>=1.2.6"]
)
