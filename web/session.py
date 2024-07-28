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
from typing import Any

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
        """ All cookies in the cookie_jar. """
        if cls.session is not None:
            return cls.session.cookie_jar

        return None

    @classmethod
    def cookies(cls, domain: str, name: str = None):
        """
        Get cookie(s) for a specific domain.

        If only domain is given, all cookies for the domain
        will be returned as SimpleCookie.

        If a name is also provided, then the cookie will be
        returned as Morsel.

        None will be returned if no cookies for the domain exists,
        or if there is no cookie with that name.

        :param domain: The domain for which the cookie(s) belongs.
        :param name: The name of the cookie.
        :return: SimpleCookie, Morsel or None.
        """
        if cls.session is not None:

            domain_cookies = cls.session.cookie_jar.filter_cookies(domain)
            # domain_cookies = cls.cookie_jar().filter_cookies(domain)

            if name is None:
                if len(domain_cookies) == 0:
                    return None

                return domain_cookies

            cookie = domain_cookies.get(name)
            if cookie is not None:
                return cookie

        return None

    @classmethod
    def clear_cookies(cls, predicate=None):
        """
        Clear(delete) cookie(s).

        If predicate is None, all session cookies will be deleted
        """
        cls.session.cookie_jar.clear(predicate)
        # cls.cookie_jar().clear(predicate)

    @classmethod
    def clear_domain_cookies(cls, domain):
        """ Clear(delete) all cookies from domain. """
        log.debug(f'clearing cookies for domain: `{domain}')
        cls.session.cookie_jar.clear_domain(domain)
        # cls.cookie_jar().clear_domain(domain)

    @classmethod
    def get_cookie_by_name(cls, name):
        """ Get a cookie Morsel by name. """
        if cls.session is not None:
            for cookie in cls.session.cookie_jar:
                if cookie.key == name:
                    return cookie
        return None

    @classmethod
    async def close_connector(cls):
        # if type(cls.connector) in connector.types:
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
