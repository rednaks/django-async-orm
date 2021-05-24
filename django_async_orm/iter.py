import asyncio


class AsyncIter:
    def __init__(self, iterable):
        self._iter = iter(iterable)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            element = next(self._iter)
        except StopIteration:
            raise StopAsyncIteration
        await asyncio.sleep(0)
        return element
