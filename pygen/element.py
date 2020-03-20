# -*- coding: utf-8 -*-

from __future__ import print_function

import os

class PyGenElement():
    """
    Base level PyGenElement class.
    Provides low-level functionality inherited by all higher classes
    
    """

    def __init__(self, **kwargs):
        """ 
        Initialize the element with some basic information

        kwargs:
            name - Local name of the element
            path - Logical file path of the current element
            data - Data structure (dictionary) loaded from source .yaml file
        
        """

        self.name = kwargs.get("name", "")
        self.path = kwargs.get("path", "")
        self.data = kwargs.get("data", {})

    @property
    def abspath(self):
        """ Return the absolute filepath of this element """
        return os.path.abspath(self.path)

    @property
    def namespace(self):
        """ Return the 'namespace' (basedir) of this element """
        return os.path.dirname(self.path)