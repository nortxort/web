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

import urllib.parse


def url_parse(url: str,
              scheme: str = '',
              allow_fragments: bool = True) -> tuple:
    """ Parse a url in to different parts. """

    return urllib.parse.urlparse(url,
                                 scheme=scheme,
                                 allow_fragments=allow_fragments)


def url_encode(input_str: str,
               safe: str = '',
               encoding=None,
               errors=None) -> str:
    """ Url encode a str. """

    return urllib.parse.quote_plus(input_str,
                                   safe=safe,
                                   encoding=encoding,
                                   errors=errors)


def url_decode(input_str: str,
               encoding: str = 'utf-8',
               errors: str = 'replace') -> str:
    """ Decode a url encoded str. """

    return urllib.parse.unquote_plus(input_str,
                                     encoding=encoding,
                                     errors=errors)
