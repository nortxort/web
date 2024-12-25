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

import logging
from collections import OrderedDict

import aiohttp
import aiofile

from . import agent
from .session import Session


log = logging.getLogger(__name__)


def default_headers(headers: dict = None, rua: bool = False) -> dict:
    """
    Construct a basic header.

    :param headers: user provided header.
    :param rua: use random user agent string.
    :return: header dictionary.
    """
    if isinstance(headers, (dict, OrderedDict)):
        return headers

    bh = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': agent.DEFAULT_AGENT
    }

    if rua:
        bh['User-Agent'] = agent.random_agent()

    return bh


async def request(method: str, url: str, **kwargs):
    """
    aiohttp wrapper for HTTP requests.

    :param method: request method.
    :param url: url for the request.
    :param kwargs: keywords, see
    https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request
    :return: aiohttp.ClientResponse or None on error.
    :rtype: aiohttp.ClientResponse | None
    """
    error = None
    response = None

    header = kwargs.get('headers')
    kwargs['headers'] = default_headers(header, kwargs.pop('rua', False))

    if Session.session is None:
        session = Session.create()
    else:
        session = Session.session

    log.debug(f'{method} {url} {kwargs}')

    try:
        if method == 'websocket':
            response = await session.ws_connect(url=url, **kwargs)
        else:
            response = await session.request(method=method, url=url, **kwargs)

    except aiohttp.ClientError as e:
        error = f'web error: {e}'

    finally:
        if error is not None:
            log.error(error, exc_info=True)

        return response


async def download_file(url: str, path: str,
                        chunk_size: int = 4096, **kwargs) -> tuple:
    """
    Download file.

    :param url: url of the file to download.
    :param path: path and file name of the file to save.
    :param chunk_size: chunk size to read from the response.
    :return: path, size and header content length of file.
    """
    response = await request('GET', url=url, **kwargs)

    if response is not None:

        cl = int(response.headers.get('Content-Length', 0))
        log.debug(f'downloading {url} to {path}')

        async with aiofile.async_open(path, 'wb') as f:

            size = 0
            while True:

                data = await response.content.read(chunk_size)
                if not data:
                    log.debug(f'downloaded {size} bytes from {url}')
                    break
                await f.write(data)
                size += len(data)

        return path, size, cl

    return '', 0, 0


async def websocket(url: str, **kwargs):
    """
    websocket request.

    :param url: url of the resource.
    :return: aiohttp.ClientWebSocketResponse or None.
    :rtype: aiohttp.ClientWebSocketResponse | None
    """
    return await request(method='websocket', url=url, **kwargs)


async def get(url: str, **kwargs):
    """
    GET request.

    :param url: url of the resource.
    :return: aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='GET', url=url, **kwargs)


async def post(url: str, **kwargs):
    """
    POST request.

    :param url: url of the resource.
    :return: aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='POST', url=url, **kwargs)


async def delete(url: str, **kwargs):
    """
    DELETE request.
    TODO: Test

    :param url: url of the resource.
    :return: aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='DELETE', url=url, **kwargs)


async def patch(url: str, **kwargs):
    """
    PATCH request.
    TODO: Test

    :param url: url of the resource.
    :return: aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='PATCH', url=url, **kwargs)


async def put(url: str, **kwargs):
    """
    PUT request.
    TODO: Test

    :param url: url of the resource.
    :return: aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='PUT', url=url, **kwargs)
