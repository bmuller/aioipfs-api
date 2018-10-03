import logging
from distutils.version import LooseVersion

from aioipfs_api.exceptions import VersionMismatch
from aioipfs_api.autoapi import IPFSInterface
from aioipfs_api.http import HTTPClient

log = logging.getLogger(__name__)

MIN_VERSION = LooseVersion('0.4.3')
MAX_VERSION = LooseVersion('0.5.0')


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
