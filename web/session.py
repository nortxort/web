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

# https://docs.python.org/3/library/http.cookies.html
# https://docs.aiohttp.org/en/stable/abc.html#aiohttp.abc.AbstractCookieJar

import asyncio
import logging

import aiohttp

# implement aiohttp-socks
# https://github.com/romis2012/aiohttp-socks
try:
    from aiohttp_socks import ProxyConnector
except ImportError:
    ProxyConnector = None

log = logging.getLogger(__name__)


class Session:
    """
    Session class maintaining cookies across requests.
    """
    session = None
    connector = None

    @classmethod
    def create(cls, cookies: dict = None, connector=None):
        """
        Create a new aiohttp.ClientSession object.

        creating a new aiohttp.ClientSession is
        basically the same as opening a browser.

        cookies will be stored for as long as the session
        is open.

        :param cookies: User provided cookies for session.
        :param connector:
        :return: aiohttp.ClientSession object.
        """
        # if proxy is not:
        #   cls.connector = ProxyConnector.from_url(proxy)

        if connector is not None:
            # try, except?
            cls.connector = connector

        cls.session = aiohttp.ClientSession(cookies=cookies, connector=cls.connector)
        log.debug(f'creating session: {cls.session}, connector: {cls.connector}')

        return cls.session

    @classmethod
    async def close(cls, delay: float = 0.250):
        """ Close the session object. """
        if cls.session is not None:
            log.debug(f'closing, `cls.session` type={type(cls.session)}')
            await cls.session.close()
            # wait for connections to close
            await asyncio.sleep(delay)
            cls.session = None

    @classmethod
    def cookie_jar(cls):
        """ All session cookies. """
        if cls.session is not None:
            return cls.session.cookie_jar

    @classmethod
    def delete_all_cookies(cls):
        # TODO: Test
        """ Clear(delete) all session cookies. """
        if cls.session is not None:
            cls.session.cookie_jar.clear(None)

    @classmethod
    def delete_cookies_by_domain(cls, domain):
        """ Clear(delete) all cookies from domain. """
        log.debug(f'deleting cookies for domain: `{domain}')
        if cls.session is not None:
            cls.session.cookie_jar.clear_domain(domain)

    @classmethod
    def delete_cookie_by_name(cls, predicate=None):
        """ This method *should* delete a cookie by name. """
        # TODO: Make this work!
        if cls.session is not None:
            cls.session.cookie_jar.clear(predicate)

    @classmethod
    def get_cookie_by_name(cls, name: str):
        """ Get a cookie as Morsel by name. """
        if cls.session is not None:
            if len(cls.session.cookie_jar) > 0:
                for cookie in cls.session.cookie_jar:
                    if cookie.key == name:
                        return cookie

    @classmethod
    def get_cookies_by_domain(cls, domain: str):
        # TODO: Test
        if cls.session is not None:
            return cls.session.cookie_jar.filter_cookies(domain)

    @classmethod
    async def close_connector(cls):
        if cls.connector is not None:
            log.debug(f'connector close `cls.connector` type={type(cls.connector)}')
            await cls.connector.close()
            cls.connector = None

    @classmethod
    async def reset(cls):
        """ Reset the session and connector to their initial state(None). """
        await cls.close()
        await cls.close_connector()

    @classmethod
    def detach(cls):
        # TODO:
        # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.detach
        if cls.session is not None:
            cls.session.detach()
