#!/usr/bin/env python

import asyncio
import math
import os
import random
import socket

import tornado.ioloop
import tornado.web

PORT = int(os.environ.get("TORNADO_PORT", 8777))


DESCRIPTION = f"""
welcome to the virtual beer brewing webservice. 🍺🍺🍺
------------------------------------------------------

this service simulates the brewing process of beer and applies a machine learning
based on many personal experiments of your tutor team to rate the quality of the result.

The result is a score between 0 and 10.

the webservice takes four parameters to control the process:

    - malt: ratio malt to water (reasonable values are between 0.1 and 0.2)
    - hops: ratio hops to water (reasonable values are between 0.01 and 0.02)
    - yeast: yeast to water (reasonable values are between 0.001 and 0.005)
    - temperature (reasonable values are between 40 and 60C)

example:

    http://{socket.gethostname()}:{PORT}?malt=.01&hops=.005&yeast=.005&temperature=50

"""

best_malt, best_hops, best_yeast, best_temperature = (0.11, 0.015, 0.001, 45)


def beer_quality(malt, hops, yeast, temperature):

    if not 0.1 <= malt <= 0.2:
        return 0.0

    if not 0.01 <= hops <= 0.02:
        return 0.0

    if not 0.001 <= yeast <= 0.005:
        return 0.0

    if not 40 <= temperature <= 60:
        return 0.0

    diff_malt = (malt - best_malt) / 0.4
    diff_hops = (hops - best_hops) / 0.03
    diff_yeast = (yeast - best_yeast) / 0.001
    diff_temperature = (temperature - best_temperature) / 120

    deviation = (
        diff_malt ** 2 + diff_hops ** 2 + diff_yeast ** 2 + diff_temperature ** 2
    )


    # introduce local minima to avoid gradient search, this modification
    # is based on manual numerical experiments and not justified by any sound
    # mathematical concept:
    deviation = deviation + 0.1 * math.sin(deviation ** 0.5 * 10) ** 2

    # restrict devation to rage 0..1
    deviation = max(0, min(1, deviation))

    return 10 * (1 - deviation)


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        malt = self.request.arguments.get("malt")
        hops = self.request.arguments.get("hops")
        yeast = self.request.arguments.get("yeast")
        temperature = self.request.arguments.get("temperature")

        try:
            malt, hops, yeast, temperature = map(
                float, (malt[0], hops[0], yeast[0], temperature[0])
            )
        except (ValueError, TypeError) as e:
            print(e)
            self.write(DESCRIPTION)
            return

        score = beer_quality(malt, hops, yeast, temperature)

        # wait up to 500 msec randomly
        await asyncio.sleep(0.1 + 0.4 * random.random())
        self.write(f"{score:.2f}")


def make_app():
    return tornado.web.Application([(r"/", MainHandler)])


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    print("listen on port", PORT)
    tornado.ioloop.IOLoop.current().start()
