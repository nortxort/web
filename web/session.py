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

import asyncio
import logging

import aiohttp


log = logging.getLogger(__name__)


class Session:
    """
    Session class maintaining cookies across requests.
    """
    session = None
    connector = None
    _cookie_to_delete = None

    @classmethod
    def create(cls, cookies: dict = None, connector=None):
        """
        Create a new aiohttp.ClientSession object.

        :param cookies: User provided cookies for session.
        :param connector:
        :return: aiohttp.ClientSession object.
        """
        if connector is not None:
            # try, except?
            cls.connector = connector

        cls.session = aiohttp.ClientSession(cookies=cookies, connector=cls.connector)
        log.debug(f'creating session: `{cls.session}`, connector: `{cls.connector}`')

        return cls.session

    @classmethod
    async def close(cls, delay: float = 0.250) -> None:
        """
        Close the session object.

        :param delay: A small delay to let connections close gracefully.
        :type delay: float
        """
        if cls.session is not None:
            log.debug(f'closing session, type: `{type(cls.session)}`')
            await cls.session.close()
            # wait for connections to close
            await asyncio.sleep(delay)
            cls.session = None

    @classmethod
    async def close_connector(cls):
        if cls.connector is not None:
            log.debug(f'closing connector, type: `{type(cls.connector)}`')
            await cls.connector.close()
            cls.connector = None

    @classmethod
    async def reset(cls):
        """ Reset the session and connector to their initial state(None). """
        log.debug(f'reset, session={cls.session}, connector={cls.connector}')
        await cls.close()
        await cls.close_connector()

    @classmethod
    def cookie_jar(cls):
        """ All the cookies for the session. """
        if cls.session is not None:
            return cls.session.cookie_jar

    @classmethod
    def cookies(cls, domain: str, name: str = None):
        """
        Get cookie(s) for a specific domain.

        If only domain is given, all cookies for the domain
        will be returned as a list of Morsels.

        If a name is also provided, then the cookie will be
        returned as Morsel.

        None will be returned if no cookies for the domain exists,
        or if there is no cookie with that name.
        """
        domain_cookies = []
        if cls.session is not None:

            for cookie in cls.session.cookie_jar:
                if cookie['domain'] == domain:
                    domain_cookies.append(cookie)

            if len(domain_cookies) > 0:
                if name is None:
                    log.debug(f'cookies lookup for: `{domain}`')
                    return domain_cookies
                else:
                    log.debug(f'cookie lookup for: `{domain}`, cookie name: `{name}`')
                    for cookie in domain_cookies:
                        if cookie.key == name:
                            return cookie

    @classmethod
    def filter_cookies(cls, request_url: str):
        """
        Filter cookies by request url.

        :param request_url: The request url to filter for.
        :type request_url: str
        :return: a dictionary-like object whose keys are
        strings and whose values are Morsel instances.
        """
        if cls.session is not None:
            log.debug(f'filtering cookies for: `{request_url}`')
            return cls.session.cookie_jar.filter_cookies(request_url)

    @classmethod
    def delete_all_cookies(cls) -> None:
        """ Delete all session cookies. """
        if cls.session is not None:
            log.debug(f'deleting `{len(cls.session.cookie_jar)}` session cookies')
            cls.session.cookie_jar.clear(None)

    @classmethod
    def delete_cookies_by_domain(cls, domain) -> None:
        """
        Delete all cookies for domain and subdomains.

        :param domain: The domain to delete cookies for.
        :type domain: str
        """
        if cls.session is not None:
            log.debug(f'deleting cookies for domain: `{domain}`')
            cls.session.cookie_jar.clear_domain(domain)

    @classmethod
    def delete_cookie_by_name(cls, domain: str, name: str) -> None:
        """
        Delete cookie by name.

        :param domain: The domain the cookie belongs to.
        :type domain: str
        :param name: The name of the cookie to delete.
        :type name: str
        """
        cookie = cls.cookies(domain, name)
        if cookie is not None:
            cls._cookie_to_delete = cookie
            cls.session.cookie_jar.clear(cls._has_cookie_to_delete)

    @classmethod
    def _has_cookie_to_delete(cls, morsel):
        if (morsel.key == cls._cookie_to_delete.key and
                morsel['domain'] == cls._cookie_to_delete['domain']):
            log.debug(f'deleting morsel: `{morsel}`')
            return True
        return False
