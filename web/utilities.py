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

# useful functions when doing web related tasks.


def url_parse(url: str,
              scheme: str = '',
              allow_fragments: bool = True) -> tuple:
    """
    Parse an url in to different parts.

    :param url: The url to parse.
    :type url: str
    :param scheme: URL scheme specifier.
    :type scheme: str
    :param allow_fragments: If false, fragment identifiers are not recognized.
    :type allow_fragments: bool
    :return: A named tuple.
    :rtype: tuple
    """
    return urllib.parse.urlparse(url,
                                 scheme=scheme,
                                 allow_fragments=allow_fragments)


def url_encode(input_str: str,
               safe: str = '/',
               encoding='utf-8',
               errors='strict') -> str:
    """
    Url encode a str.

    Replace special characters in string using the %xx escape.

    :param input_str: The string to encode.
    :type input_str: str
    :param safe: Do not encode these ASCII characters.
    :type safe: str
    :param encoding: Specify how to deal with non-ASCII characters.
    :type encoding: str
    :param errors:
    :type errors:
    :return: Url encoded string.
    """
    return urllib.parse.quote_plus(input_str,
                                   safe=safe,
                                   encoding=encoding,
                                   errors=errors)


def url_decode(input_str: str,
               encoding: str = 'utf-8',
               errors: str = 'replace') -> str:
    """
    Url decode a string.

    Replace %xx escapes with their single-character equivalent

    :param input_str: The input string to decode.
    :type input_str: str | bytes
    :param encoding:
    :type encoding:
    :param errors:
    :type errors:
    :return:
    """
    return urllib.parse.unquote_plus(input_str,
                                     encoding=encoding,
                                     errors=errors)
