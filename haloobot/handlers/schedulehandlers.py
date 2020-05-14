import asyncio
import schedule
from haloobot.handlers.base import Handler
from haloobot.utils import time
from haloobot.utils import fingerpori
from haloobot.utils import fokit

class ScheduleHandler(Handler):

    SCHEDULE_TIME = "10:05"
    MAX_SLEEP_TIME = 60*60

    def __init__(self, handlers, bot, tables, messages, settings):
        super().__init__(handlers, bot, tables, messages, settings)
        schedule.every().day.at(self.SCHEDULE_TIME).do(
            lambda: asyncio.get_event_loop().create_task(self.send_to_all())
            )
    
    async def schedule_loop(self):
        while True:
            schedule.run_pending()
            await asyncio.sleep(min(self.MAX_SLEEP_TIME, schedule.idle_seconds()))
    
    async def send_to_all(self):
        for result in self.tables['db'].query('SELECT DISTINCT chat_id FROM schedules'):
            await self.send_upcoming(result['chat_id'])
        await self.send_daily_fingerpori(self.settings['chat_id'])
        await self.send_daily_fokit(self.settings['chat_id'])
    
    async def send_upcoming(self, chat_id):
        ret = time.get_upcoming_events_string(self.tables['schedules'], chat_id)
        if ret:
            return await self.send_message(chat_id, ret)
        else:
            return False

    async def send_daily_fingerpori(self, chat_id):
        url = await fingerpori.get_newest_fingerpori()
        if(url != self.settings['last_fingerpori_url']):
            await self.send_image(chat_id, url)
            self.settings['last_fingerpori_url'] = url
        url = await fingerpori.get_newest_fingerpori_b()
        if(url != self.settings['last_fingerpori_b_url']):
            await self.send_image(chat_id, url) 
            self.settings['last_fingerpori_b_url'] = url

    async def send_daily_fokit(self, chat_id):
        url = await fokit.get_newest_fokit()
        if(url != self.settings['last_fokit_url']):
            await self.send_image(chat_id, url)
            self.settings['last_fokit_url'] = url
