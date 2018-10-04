import logging
# pylint: disable=no-name-in-module,import-error
from distutils.version import LooseVersion

from aioipfs_api.exceptions import VersionMismatchError
from aioipfs_api.autoapi import IPFSInterface
from aioipfs_api.http import HTTPClient

log = logging.getLogger(__name__)

MIN_VERSION = LooseVersion('0.4.3')
MAX_VERSION = LooseVersion('0.5.0')


class Client(IPFSInterface):
    def __init__(self, host='localhost', port=5001, version='v0'):
        client = HTTPClient(host, port, version)
        super().__init__(client)

    async def connect(self):
        """
        Start a HTTP connection and check API version for mismatch.
        """
        await self.client.connect()
        fversion = await self.version()
        version = LooseVersion(fversion['Version'])
        if version < MIN_VERSION or version >= MAX_VERSION:
            msg = "Version %s outside of supported %s - %s range"
            msg = msg % (version, MIN_VERSION, MAX_VERSION)
            raise VersionMismatchError(msg)
        msg = "Library compiled for version %s, interacting with version %s"
        log.debug(msg, IPFSInterface.VERSION, version)

    async def close(self):
        """
        Close any open HTTP connections.
        """
        await self.client.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
