import logging
from io import BytesIO
import os
from aiohttp import ClientSession, FormData
from glob import glob
import json

from yarl import URL

log = logging.getLogger(__name__)

async def _parse_json_response(resp):
    """
    Not super robust now since it's not incremental...
    but handle parsing a json type response that is chunked.
    """
    if resp.headers.get('X-Chunked-Output') != '1':
        return await resp.json()
    text = await resp.read()
    parts = text.split(b"\n")
    return [json.loads(p) for p in parts if p]


class HTTPClient:
    def __init__(self, host, port, version):
        path = "/api/%s/" % version
        self.url = URL.build(scheme='http', host=host, port=port, path=path)

    async def connect(self):
        self.client = ClientSession(raise_for_status=True)

    def get(self, path, args, kwargs):
        url = self.url.join(URL(path))
        params = [('arg', v) for v in args]
        params += [(k, v) for k, v in kwargs.items()]        
        return self.client.get(url, params=params)

    def _build_form(self, source, kwargs):
        source = os.path.abspath(source)
        sourcedir = os.path.dirname(source)
        flist = [source]
        if os.path.isdir(source):
            flist = glob(os.path.join(source, "**"), recursive=True)
        form = FormData()
        for path in flist:
            relpath = os.path.relpath(path, sourcedir)
            if os.path.isdir(path):
                form.add_field('files', BytesIO(), filename=relpath, content_type='application/x-directory')
            else:
                form.add_field('files', open(path, 'rb'), filename=relpath)
        return form

    async def get_parsed(self, path, args, kwargs):
        url = self.url.join(URL(path))
        # build params, ignoring type of file, adding kwargs
        params = [('arg', val) for val, type in args if type != 'file']
        params += [(k, v) for k, v in kwargs.items()]

        # build data param if a file param type is given
        fparams = [val for val, type in args if type == 'file']
        data = self._build_form(fparams[0], kwargs) if fparams else None

        async with self.client.get(url, params=params, data=data) as resp:
            if resp.content_type == 'application/json':
                return await _parse_json_response(resp)
            return await resp.text()        

    async def close(self):
        await self.client.close()
