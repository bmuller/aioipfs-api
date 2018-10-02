import asyncio
import logging

from aioipfs_api.client import Client

if __name__ == "__main__":
    log = logging.getLogger('aioipfs_api')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

    async def main():
        async with Client() as c:
            print(await c.add('/Users/bmuller/projects/aioipfs-api/input.txt'))
            #async with c.cat('QmZLRFWaz9Kypt2ACNMDzA5uzACDRiCqwdkNSP1UZsu56D') as f:
            #    print(await f.read())

            #print(await c.cat('QmZLRFWaz9Kypt2ACNMDzA5uzACDRiCqwdkNSP1UZsu56D').read())
            #print(await c.id())
            #print(await c.log_level('all', 'warning'))
            #print(await c.commands())
            #print(await c.ls('QmQsvfkjXXFAR4buzGRiVRTSP7DDbkNPoBhG8xiin9dmKj'))
            #print(await c.object_data('QmNW36HjE2cmJN8xCuJPggRsJrvMsH1Uxz2uHhn2CUSy2F'))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
