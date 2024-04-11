import asyncio
import logging
import sys
import threading
from routines.removing_tokens import Tokens
from routines.removing_users import Users

UPDATE_SETTINGS_PER_SECONDS = 10

logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def tks():
    tokens = Tokens(UPDATE_SETTINGS_PER_SECONDS)
    while True:
        await tokens.execute()
        logging.debug('Tokens. number of current threads is ', threading.active_count())

async def usrs():
    users = Users(UPDATE_SETTINGS_PER_SECONDS)
    while True:
        await users.execute()
        logging.debug('Users. number of current threads is ', threading.active_count())

async def main():
    task1 = asyncio.create_task(tks())
    task2 = asyncio.create_task(usrs())

    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())