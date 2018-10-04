# Async IPFS API Client
[![Build Status](https://secure.travis-ci.org/bmuller/aioipfs-api.png?branch=master)](https://travis-ci.org/bmuller/aioipfs-api)
[![Docs Status](https://readthedocs.org/projects/kademlia/badge/?version=latest)](https://aioipfs-api.readthedocs.io)
[![Codecov Status](https://codecov.io/gh/bmuller/aioipfs-api/branch/master/graph/badge.svg)](https://codecov.io/gh/bmuller/aioipfs-api/)

**Documentation can be found at [aioipfs-api.readthedocs.org](https://aioipfs-api.readthedocs.io).**

## Installation

```
pip install aioipfs-api
```

## Usage
*This assumes you have a working familiarity with [asyncio](https://docs.python.org/3/library/asyncio.html).*

```python
import asyncio
from aioipfs_api.client import Client

async def main():
    async with Client() as client:
        # print the readme
        async with client.cat("QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme") as f:
            print(await f.text())

        # add a directory
        print(await client.add('/some/dir/path'))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Logging
This library uses the standard [Python logging library](https://docs.python.org/3/library/logging.html).  To see debut output printed to STDOUT, for instance, use:

```python
import logging

log = logging.getLogger('aioipfs_api')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
```

## Running Tests
To run tests:

```
pip install -r dev-requirements.txt
python -m unittest
```
