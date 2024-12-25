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

from web import get, Session


def show_cookies_jar():
    print(f'cookie items in cookie_jar: {len(Session.cookie_jar())}')

    for cookie in Session.cookie_jar():
        print(f'cookie_jar cookie> {cookie}')


async def set_cookie():
    # each url will set a cookie/value
    urls = [
        'http://httpbin.org/cookies/set/cookie1/cookie1_value',
        'http://httpbin.org/cookies/set/cookie2/cookie2_value',
        'http://httpbin.org/cookies/set/cookie3/cookie3_value'
    ]

    for url in urls:
        await get(url)


async def delete_cookie():
    # set some cookies
    await set_cookie()

    # show the cookies in the sessions cookie jar
    show_cookies_jar()

    # delete one of the cookies
    Session.delete_cookie_by_name('httpbin.org', 'cookie2')

    # show the remaining cookies
    show_cookies_jar()

    # close the session
    await Session.close()


async def get_cookies_by_domain():
    await set_cookie()

    # get all cookies for domain
    cookies = Session.cookies('httpbin.org')
    for cookie in cookies:
        print(f'cookie> {cookie}')

    await Session.close()


async def filter_cookies():
    await set_cookie()

    # filter cookies by request url
    filtered_cookies = Session.filter_cookies('http://httpbin.org')
    for cookie in filtered_cookies:
        print(filtered_cookies[cookie])

    await Session.close()


asyncio.run(filter_cookies())
