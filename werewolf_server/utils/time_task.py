import asyncio

async def start_timer_task(seconds: int, callback, *args, **kwargs):
    asyncio.create_task(timer_task(seconds, callback, *args, **kwargs))

async def timer_task(seconds: int, callback, current_seconds=None, *args, **kwargs):
    if current_seconds is None:
        current_seconds = [10]
    while seconds > 0:
        await asyncio.sleep(1)
        seconds -= 1
        current_seconds[0] = seconds
    if asyncio.iscoroutinefunction(callback):
        await callback(*args, **kwargs)
    else:
        callback(*args, **kwargs)