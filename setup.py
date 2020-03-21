# -*- coding: utf-8 -*-

import setuptools

from PyGen.version import PYGEN_VERSION

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="PyGen",
    
    version=PYGEN_VERSION,
    
    author="Oliver Walters",
    
    author_email="oliver.henry.walters@gmail.com",
    
    description="Protocol Generation Tool",
    
    long_description_content_type="text/markdown",
    
    long_description=long_description,

    keywords="protocol, generation, embedded",
    
    url="https://github.com/SchrodingersGat/PyGen",

    license="MIT",
    
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'pyyaml',
        'colorama',
        'flake8'
    ]


)
