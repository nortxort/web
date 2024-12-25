# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2024 Nortxort

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from .agent import DEFAULT_AGENT, COMMON_AGENTS, random_agent
from .session import Session
from .http import request, get, post, websocket, \
     download_file, default_headers, put, patch, delete

<<<<<<< Updated upstream
__version__ = '2.1.0'  # 2.1.0 29/9/2024
=======
__version__ = '2.3.0'  # 2.3.0 25/12/2024
>>>>>>> Stashed changes

__all__ = [
    '__version__',
    'DEFAULT_AGENT',
    'COMMON_AGENTS',
    'random_agent',
    'Session',
    'request',
    'get',
    'post',
    'websocket',
    'download_file',
    'default_headers',
    'put',
    'patch',
    'delete'
]
