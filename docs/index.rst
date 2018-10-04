aioipfs-api
=======================================

Asynchronous Python library for interacting with the IPFS HTTP API.

Library Installation
====================

.. code-block:: bash

   $ pip install aiohttp

Getting Started
===============

Client example::

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

Source code
===========

The project is hosted on `GitHub <https://github.com/bmuller/aioipfs-api>`_.

Please feel free to file an issue on the `bug tracker
<https://github.com/bmuller/aioipfs-api/issues>`_ if you have found a bug
or have some suggestion in order to improve the library.

The library uses `Travis <https://travis-ci.com/bmuller/aioipfs-api>`_ for
Continuous Integration.

Table Of Contents
=================

.. toctree::
   :name: mastertoc
   :maxdepth: 2
   :caption: Contents:

   client

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
