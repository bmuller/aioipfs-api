import asyncio
import logging
from distutils.version import LooseVersion

import aiohttp
from yarl import URL

from exceptions import VersionMismatch

log = logging.getLogger(__name__)

MIN_VERSION = LooseVersion('0.4.3')
MAX_VERSION = LooseVersion('0.5.0')


class HTTPClient:
    def __init__(self, host, port, version):
        path = "/api/%s/" % version
        self.url = URL.build(scheme='http', host=host, port=port, path=path)

    async def connect(self):
        self.client = aiohttp.ClientSession(raise_for_status=True)

    async def get(self, *parts, **kwargs):
        parts = "/".join(parts)
        url = self.url.join(URL(parts))
        async with self.client.get(url, params=kwargs) as resp:
            return resp

    async def get_parsed(self, *parts, **kwargs):
        parts = "/".join(parts)
        url = self.url.join(URL(parts))
        async with self.client.get(url, params=kwargs) as resp:
            if resp.content_type == 'application/json':
                return await resp.json()
            return await resp.text()        

    async def close(self):
        await self.client.close()


def get_parsed_method(path):
    async def method(obj, *args, **kwargs):
        return await obj.client.get_parsed(path, *args, **kwargs)
    return method


class Client:
    def __init__(self, host='localhost', port=5001, version='v0'):
        self.client = HTTPClient(host, port, version)

    async def connect(self):
        await self.client.connect()
        fversion = await self.version()
        version = LooseVersion(fversion['Version'])
        log.debug("Checking version %s for compatability" % version)
        if version < MIN_VERSION or version > MAX_VERSION:
            raise VersionMismatch(version, MIN_VERSION, MAX_VERSION)

    async def close(self):
        await self.client.close()
    
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    version = get_parsed_method('version')
    id = get_parsed_method('id')
    ls = get_parsed_method('ls')
        
    async def cat(self, multihash):
        return await self.client.get('cat', multihash)

    async def object_data(self, multihash):
        data = await self.client.get('object', 'data', multihash)
        return await data.read()



if __name__ == "__main__":
    log = logging.getLogger('client')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

    async def main():
        async with Client() as c:
            print(await c.version())
            #print(await c.cat('QmZLRFWaz9Kypt2ACNMDzA5uzACDRiCqwdkNSP1UZsu56D'))
            print(await c.id())        
            print(await c.ls('QmQsvfkjXXFAR4buzGRiVRTSP7DDbkNPoBhG8xiin9dmKj'))
            #print(await c.object_data('QmNW36HjE2cmJN8xCuJPggRsJrvMsH1Uxz2uHhn2CUSy2F'))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
