from aiohttp import ClientSession
from flet import Page
from flet.core.control_event import ControlEvent

from env import API_URL


async def click_go(page: Page, path: str):
    async def go(_: ControlEvent):
        page.go(path)

    return go


async def click_boost_project(project_id, user):
    async def boost_project(_: ControlEvent):
        async with ClientSession() as client:
            return await client.put(f"{API_URL}/projects/boost/{project_id}", json=user)

    return boost_project
