import ujson
from aiohttp.web_response import json_response as aiohttp_json_response


def json_response(*args, **kwargs):
    try:
        data = kwargs.pop('data')
        kwargs['text'] = ujson.dumps(data, ensure_ascii=False)
    except KeyError:
        pass
    return aiohttp_json_response(*args, **kwargs)
