import asyncio
import threading
from routines.removing_tokens import Tokens
from routines.removing_users import Users


UPDATE_SETTINGS_PER_SECONDS = 10

async def tks():
    tokens = Tokens(UPDATE_SETTINGS_PER_SECONDS)
    while True:
        await tokens.execute()
        print('Tokens. number of current threads is ', threading.active_count())

async def usrs():
    users = Users(UPDATE_SETTINGS_PER_SECONDS)
    while True:
        await users.execute()
        print('Users. number of current threads is ', threading.active_count())

async def main():
    task1 = asyncio.create_task(tks())
    task2 = asyncio.create_task(usrs())

    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())