import aiohttp
from google_api_is_sheet import settings
from google_api_is_sheet import _internal

class GetFormSheet(_internal.RequestHandel):
    async def get_range(self, session: aiohttp.ClientSession, range: str):
        params = {
            'key': self.token
        }
        return await self.make_request(session, domain=settings.SPREADSHEETS, path=f"{self.table_id}/values/{range}", params=params)