#!/usr/bin/env python
# encoding: utf-8
"""
IPython.

IPython is a set of tools for interactive and exploratory computing in Python.
"""
#-----------------------------------------------------------------------------
#  Copyright (C) 2008-2009  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import absolute_import

import os
import sys

#-----------------------------------------------------------------------------
# Setup everything
#-----------------------------------------------------------------------------

if sys.version[0:3] < '2.5':
    raise ImportError('Python Version 2.5 or above is required for IPython.')


# Make it easy to import extensions - they are always directly on pythonpath.
# Therefore, non-IPython modules can be added to extensions directory.
# This should probably be in ipapp.py.
sys.path.append(os.path.join(os.path.dirname(__file__), "extensions"))

#-----------------------------------------------------------------------------
# Setup the top level names
#-----------------------------------------------------------------------------

from .config.loader import Config
from .core import release
from .core.application import Application
from .core.ipapp import IPythonApp
from .core.embed import embed
from .core.error import TryNext
from .core.iplib import InteractiveShell
from .testing import test

from .lib import (
    enable_wx, disable_wx,
    enable_gtk, disable_gtk,
    enable_qt4, disable_qt4,
    enable_tk, disable_tk,
    set_inputhook, clear_inputhook,
    current_gui, spin,
    appstart_qt4, appstart_wx,
    appstart_gtk, appstart_tk
)

# Release data
__author__ = ''
for author, email in release.authors.values():
    __author__ += author + ' <' + email + '>\n'
__license__  = release.license
__version__  = release.version
__revision__ = release.revision
