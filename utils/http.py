import aiohttp
from config.public import USER_AGENT


async def request(url, *, headers=None, **kwargs):
    """Simple get request"""

    if headers is None:
        headers = {'User-agent': USER_AGENT}
    else:
        headers['User-agent'] = USER_AGENT

    async with aiohttp.ClientSession() as session:
        return await session.get(url, headers=headers, **kwargs)