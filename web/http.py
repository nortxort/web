# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2020 Nortxort

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
try:
    import aiofiles
except ImportError:
    aiofiles = None

from . import agent
from .session import Session


log = logging.getLogger(__name__)


def headers(header: dict = None, rua: bool = False) -> dict:
    """
    Construct a basic header.

    :param header: A user provided header.
    :param rua: Use a random user agent string.
    :return: A header dictionary.
    """
    if isinstance(header, OrderedDict):
        return header

    if isinstance(header, dict):
        if header.get('User-Agent') is not None and rua:
            header['User-Agent'] = agent.random_agent()

        return header
    else:
        ua = agent.DEFAULT_AGENT
        if rua:
            ua = agent.random_agent()

        h = {
            'User-Agent': ua
        }

        return h


async def request(method: str, url: str, **kwargs):
    """
    aiohttp wrapper for HTTP requests.

    :param method: The request method.
    :param url: The url for the request.
    :param kwargs: Keywords, see
    https://github.com/aio-libs/aiohttp/blob/581e97654410aa4b372b93e69434f6de79feeef4/aiohttp/client.py#L953
    :return: A aiohttp.ClientResponse object or None on error.
    :rtype: aiohttp.ClientResponse | None
    """
    error = None
    response = None

    header = kwargs.get('headers')
    kwargs['headers'] = headers(header, kwargs.pop('rua', False))

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
            log.error(error)

        return response


async def download_file(url: str, destination: str, chunk_size: int = 1024, **kwargs):
    """
    Download file.

    :param url: The url of the file to download.
    :param destination: The destination path and file name to save.
    :param chunk_size: The size of the chunks to read/write.
    :return: The destination of the downloaded file.
    :rtype: str | None
    """
    if aiofiles is None:
        log.error('aiofiles not installed -- cannot download files!')
        return

    response = await request('GET', url=url, **kwargs)
    if response is not None:

        log.debug(f'downloading {url} to {destination}')

        async with aiofiles.open(destination, mode='wb') as f:
            async for data in response.content.iter_chunked(chunk_size):
                await f.write(data)

        return destination

    return None


async def websocket(url: str, **kwargs):
    """
    websocket request.

    :param url: The url of the resource.
    :return: A aiohttp.ClientWebSocketResponse or None.
    :rtype: aiohttp.ClientWebSocketResponse | None
    """
    return await request(method='websocket', url=url, **kwargs)


async def get(url: str, **kwargs):
    """
    GET request.

    :param url: The url of the resource.
    :return: A aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='GET', url=url, **kwargs)


async def post(url: str, **kwargs):
    """
    POST request.

    :param url: The url of the resource.
    :return: A aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='POST', url=url, **kwargs)


async def delete(url: str, **kwargs):
    """
    DELETE request.
    TODO: Test

    :param url: The url of the resource.
    :return: A aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='DELETE', url=url, **kwargs)


async def patch(url: str, **kwargs):
    """
    PATCH request.
    TODO: Test

    :param url: The url of the resource.
    :return: A aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='PATCH', url=url, **kwargs)


async def put(url: str, **kwargs):
    """
    PUT request.
    TODO: Test

    :param url: The url of the resource.
    :return: A aiohttp.ClientResponse or None.
    :rtype: aiohttp.ClientResponse | None
    """
    return await request(method='PUT', url=url, **kwargs)
