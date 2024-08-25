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
import aiohttp

from web import websocket, Session


async def make_websocket_request():
    """
    Test the websocket feature of the web package.
    """
    # create the websocket connection
    ws = await websocket('wss://echo.websocket.org')

    # if the connection was not closed
    if not ws.closed:
        # send a message as a string
        msg = 'hello world'
        print(f'sending message: {msg}')
        await ws.send_str(msg)

        # listen for messages
        while not ws.closed:

            # receive message
            wsr = await ws.receive()

            # if the message type is text
            if wsr.type == aiohttp.WSMsgType.text:

                # print the message
                print(f'receiving message: {wsr.data}')
                break

    # close the session
    await Session.close()

asyncio.run(make_websocket_request())
