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

import asyncio
from web import get, Session


async def make_requests_concurrently():
    """
    Make requests concurrently.

    In this case, 20 GET requests.
    """
    urls = ['https://httpbin.org/get'] * 20

    # a list of tasks to run
    tasks = []

    for url in urls:

        # foreach url create a task
        task = asyncio.create_task(get(url))
        tasks.append(task)

    # pages is a list of ClientResponses
    pages = await asyncio.gather(*tasks)

    for page in pages:
        print(await page.text())

    # close the session
    await Session.close()
    # wait for asyncio to finish
    await asyncio.sleep(1)

# asyncio.run(make_requests_concurrently())
asyncio.get_event_loop().run_until_complete(make_requests_concurrently())
