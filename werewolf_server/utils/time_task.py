import asyncio

async def start_timer_task(seconds: int, callback, *args, **kwargs):
    asyncio.create_task(timer_task(seconds, callback, *args, **kwargs))

async def timer_task(seconds: int, callback, *args, **kwargs):
    await asyncio.sleep(seconds)
    if asyncio.iscoroutinefunction(callback):
        await callback(*args, **kwargs)
    else:
        callback(*args, **kwargs)