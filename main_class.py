from ast import literal_eval
import aiohttp
import asyncio
from google_api_is_sheet.authentication import ApiAuth
from google_api_is_sheet.get_from_sheet import GetFormSheet
from database_manip import Database_update, Create_Table
import psycopg2

class Google_Api_Base(ApiAuth, GetFormSheet):
    def __init__(self, table_id: str):
        '''
        Getting required variables

        table_id: ID of a google spreed sheet
        '''
        self.table_id = table_id
        token_temp = self._get_token()
        self.token = token_temp if token_temp else None
        
        self.conn = psycopg2.connect("dbname=test_task user=postgres password=66106610")
        Create_Table(self.conn)
   
    async def main_loop(self):
        self.cur = self.conn.cursor()
        while(True):
        
            self.cur.execute("SELECT id, order_id, price_in_usd, due_to FROM MAIN_TABLE ORDER BY ID::integer;")
            fetch_result = str(self.cur.fetchall())
            old_hash_sum = fetch_result.__hash__()

            async with aiohttp.ClientSession() as session:    
                resp_code = await self._authenticate(session)
                print(resp_code)
                ans = (await self.get_range(session, "A:D")) if resp_code == 200 else print(resp_code)
                if not ans:
                    return
                
                ans = f"[{str(literal_eval(ans)['values'][1:]).replace('[', '(').replace(']', ')')[1:-1]}]"

                new_hash = ans.__hash__()

                print(f"{old_hash_sum}\n{new_hash}")
                if new_hash != old_hash_sum:
                    print("updating")
                    Database_update(self.conn, ans)
                else:
                    print("Not updating")
            await asyncio.sleep(1.0)

    def __del__(self):
        self.conn.close()

def start(doc_id):
    sheet = Google_Api_Base(doc_id)
    loop = asyncio.get_event_loop()
    loop.create_task(sheet.main_loop())
    loop.run_forever()

