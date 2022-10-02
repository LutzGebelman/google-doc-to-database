import aiohttp
from google_api_is_sheet import _internal
from google_api_is_sheet import settings
from json import loads
class ApiAuth(_internal.RequestHandel):
    def _get_token(self):
        token = None
        try:
            with open("token.json", "r") as file:
                return loads(file.read())["token"]

        except Exception as e: 
            print(f"Could not open 'token.json' file. Error is: '{e}'")
            return None

    
    async def _authenticate(self, session: aiohttp.ClientSession) -> int:
        what = _internal.What.STATUS
        method = _internal.Method.GET
        response = await self.make_request(session=session, what=what, method=method, domain=settings.AUTH_DOMAINE, params={
            'key': self._get_token()
        })
        return response