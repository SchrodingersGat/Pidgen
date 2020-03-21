# -*- coding: utf-8 -*-

import setuptools

from pygen.version import PYGEN_VERSION

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="PyGen",
    scripts=["pygen.py"],
    version=PYGEN_VERSION,
    author="Oliver Walters",
    author_email="oliver.henry.walters@gmail.com",
    description="Protocol Generation Tool",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/SchrodingersGat/PyGen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
