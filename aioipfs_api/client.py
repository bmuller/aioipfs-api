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
        async with self.client.get(url) as resp:
            if resp.content_type == 'text/plain':
                return resp
            return await resp.json()

    async def close(self):
        await self.client.close()


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

    async def version(self):
        return await self.client.get('version')

    async def id(self):
        return await self.client.get('id')
        
    async def cat(self, multihash):
        return await self.client.get('cat', multihash)


log = logging.getLogger('client')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

async def main():
    async with Client() as c:
        print(await c.version())
        txt = await c.cat('QmZLRFWaz9Kypt2ACNMDzA5uzACDRiCqwdkNSP1UZsu56D')
        print(await txt.content.read())
        resp.close()
        print(await c.id())        
        img = await c.cat('QmcAoKXzmgkBcFQgTpWMny9dQXPjxtbwxNSR7D84g2xFHm')
        print(await img.content.read())
        
loop = asyncio.get_event_loop()
r = loop.run_until_complete(main())
