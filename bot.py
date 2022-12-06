from pyrogram import Client
from aiohttp import web
from plugins import web_server
from database.ia_filterdb import Media
from info import API_ID, API_HASH, BOT_TOKEN
from typing import Union, Optional, AsyncGenerator
from pyrogram import types

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="TinSonBro",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=300,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        self.username = me.username 
        self.id = me.id
        self.name = me.first_name
        self.mention = me.mention 
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        PORT = "8080"
        await web.TCPSite(app, bind_address, PORT).start()
        print(f"@{me.username}... IS STARTED ⚡️⚡️")
        

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
    
    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:       
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1


app = Bot()
app.run()
