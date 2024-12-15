from aiohttp import ClientSession
from beanie import PydanticObjectId
from flet import Page

from env import API_URL

from .buttons import ContestButton, ProjectButton


async def contests(page: Page) -> list[ContestButton]:
    async with ClientSession() as client:
        return [
            await ContestButton.ainit(
                contest["title"], page=page, contest_id=contest["_id"]
            )
            for contest in await (await client.get(f"{API_URL}/contests/list/")).json()
        ]


async def projects_top(page: Page, contest_id: PydanticObjectId) -> list[ProjectButton]:
    async with ClientSession() as client:
        projects_responce = await client.get(f"{API_URL}/projects/list/boosts/")
        contest_responce = await client.get(f"{API_URL}/contests/get/{contest_id}")
    contest_projects = [
        project
        for project in await projects_responce.json()
        if project["_id"]
        in [
            project_link["id"]
            for project_link in (await contest_responce.json())["projects"]
        ]
    ]

    return [
        await ProjectButton.ainit(
            project["title"],
            f"Бустов {project["boosts"]}",
            page=page,
            project_id=project["_id"],
            place=place,
        )
        for place, project in enumerate(contest_projects, start=1)
    ]
