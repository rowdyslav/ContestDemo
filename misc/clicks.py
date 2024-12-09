from aiohttp import ClientSession
from env import API_URL
from flet import Page


async def click_go(page: Page, path: str):
    async def _(e):
        page.go(path)

    return _


async def click_boost_project(project_id, user):
    async def _(e):
        async with ClientSession() as client:
            return await client.put(f"{API_URL}/projects/boost/{project_id}", json=user)

    return _
