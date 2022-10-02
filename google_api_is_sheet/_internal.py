from pickle import GET
import aiohttp
from enum import Enum

def make_url(json: dict) -> str:
    ans = "?"
    for key, value in json.items():
        ans += f"{key}={value}&"
    return ans

class Method(Enum):
    GET = 0
    POST = 1
    PUT = 2
    HEAD = 3

class What(Enum):
    TEXT = 0
    STATUS = 1
    HEADERS = 2

class RequestHandel:
    async def make_request(self, session: aiohttp.ClientSession, domain: str = "", path: str = "", params: dict = {}, method: Method = Method.GET, what: What = What.TEXT) -> str:
        url = f"{domain}/{path}{make_url(params)}"
        
        request = None
        match method:
            case Method.GET:
                request = session.get
            case Method.POST:
                request = session.post
            case Method.PUT:
                request = session.put
            case Method.HEAD:
                request = session.head

        async with request(url) as resp:
            match what:
                case What.TEXT:
                    return await resp.text()
                case What.STATUS:
                    return resp.status
                case What.HEADERS:
                    return await resp.headers()