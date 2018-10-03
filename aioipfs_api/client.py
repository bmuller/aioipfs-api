import asyncio
import logging
from distutils.version import LooseVersion

import aiohttp
import glob
import os
from io import BytesIO
from yarl import URL

from aioipfs_api.exceptions import VersionMismatch
from aioipfs_api.autoapi import IPFSInterface

log = logging.getLogger(__name__)

MIN_VERSION = LooseVersion('0.4.3')
MAX_VERSION = LooseVersion('0.5.0')


class HTTPClient:
    def __init__(self, host, port, version):
        path = "/api/%s/" % version
        self.url = URL.build(scheme='http', host=host, port=port, path=path)

    async def connect(self):
        self.client = aiohttp.ClientSession(raise_for_status=True)

    def get(self, path, args, kwargs):
        url = self.url.join(URL(path))
        params = [('arg', v) for v in args]
        params += [(k, v) for k, v in kwargs.items()]        
        return self.client.get(url, params=params)

    async def get_parsed(self, path, args, kwargs):
        url = self.url.join(URL(path))
        params = []
        file = None
        for argval, argtype in args:
            if argtype == 'file':
                file = argval
            else:
                params.append(('arg', argval))
        params += [(k, v) for k, v in kwargs.items()]

        if file:
            file = os.path.normpath(file)
            dirfile = os.path.dirname(file)
            files = aiohttp.FormData()
            for path in glob.glob(os.path.join(file, "**"), recursive=True):
                relpath = os.path.relpath(path, dirfile)
                if os.path.isdir(path):
                    files.add_field('files', BytesIO(), filename=relpath, content_type='application/x-directory')
                else:
                    files.add_field('files', open(path, 'rb'), filename=relpath)
            async with self.client.get(url, params=params, data=files) as resp:
                return await resp.read()
        
        async with self.client.get(url, params=params) as resp:
            if resp.content_type == 'application/json':
                return await resp.json()
            return await resp.text()        

    async def close(self):
        await self.client.close()


class Client(IPFSInterface):
    def __init__(self, host='localhost', port=5001, version='v0'):
        self.client = HTTPClient(host, port, version)

    async def connect(self):
        await self.client.connect()
        fversion = await self.version()
        version = LooseVersion(fversion['Version'])
        if version < MIN_VERSION or version >= MAX_VERSION:
            raise VersionMismatch(version, MIN_VERSION, MAX_VERSION)
        msg = "Library compiled for version %s, interacting with version %s"
        log.debug(msg, IPFSInterface.VERSION, version)

    async def close(self):
        await self.client.close()
    
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
