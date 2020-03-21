# -*- coding: utf-8 -*-

import setuptools

from pidgen.version import PIDGEN_VERSION

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="pidgen",
    
    version=PIDGEN_VERSION,
    
    author="Oliver Walters",
    
    author_email="oliver.henry.walters@gmail.com",
    
    description="Python-based Protocol Generation Tool",
    
    long_description=long_description,
    
    long_description_content_type="text/markdown",

    keywords="protocol, generation, embedded",
    
    url="https://github.com/SchrodingersGat/pidgen",

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
    ],

    python_requires=">=2.7"
)
