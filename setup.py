#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup
from re import search


def get_version():
    with open("kiss_headers/version.py") as version_file:
        return search(
            r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""", version_file.read()
        ).group("version")


# Package meta-data.
NAME = "kiss-headers"
DESCRIPTION = "Python package for object oriented headers, HTTP/1.1 style. Also parse headers."
URL = "https://github.com/ousret/kiss-headers"
EMAIL = "ahmed.tahri@cloudnursery.dev"
AUTHOR = "Ahmed TAHRI @Ousret"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = get_version()

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    project_urls={
        "Documentation": "https://www.kiss-headers.tech",
        "Source": "https://github.com/Ousret/kiss-headers",
        "Issue tracker": "https://github.com/Ousret/kiss-headers/issues",
    },
    keywords=["headers", "http", "mail", "text", "imap", "header", "https", "imap4"],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_data={"kiss_headers": ["py.typed"]},
    install_requires=[],  # We shall not require anything. This will remain the same.
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Communications :: Email",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
