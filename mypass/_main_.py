from mypass.database.postgresql.connection import *
import asyncio

async def mew():
    conn = Connection()
    connect = await conn.connect()
    result = await connect.fetch('SELECT * from u_users')
    await connect.close()
    return result


async def main():
    # create the coroutine
    coro = mew()
    # create and execute the task
    task = asyncio.create_task(coro)
    # wait for the task to complete and get the return value
    value = await task
    value2 = await task
    value3 = await task
    value4 = await task
    # report the return value
    print(value, value2, value3, value4)


# run the asyncio program
asyncio.run(main())
