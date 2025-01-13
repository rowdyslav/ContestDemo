from aiohttp import ClientSession
from beanie import PydanticObjectId
from flet import CircleAvatar, Page, Colors

from env import API_URL

from .buttons import ContestButton, ProjectButton


async def contests(page: Page) -> list[ContestButton]:
    """Возвращает контесты в виде списка ContestButton"""

    async with ClientSession() as client:
        return [
            await ContestButton.async_init(
                contest["title"], page=page, contest_id=contest["_id"]
            )
            for contest in await (await client.get(f"{API_URL}/contests/list/")).json()
        ]


async def projects_top(page: Page, contest_id: PydanticObjectId) -> list[ProjectButton]:
    """Возвращает топ проектов по бустам в виде списка ProjectButton"""

    async with ClientSession() as client:
        projects_top_responce = await client.get(f"{API_URL}/projects/list/boosts/")
        contest_responce = await client.get(f"{API_URL}/contests/get/{contest_id}")
    contest_projects_top = [
        project
        for project in await projects_top_responce.json()
        if project["_id"]
        in [
            project_link["id"]
            for project_link in (await contest_responce.json())["projects"]
        ]
    ]

    return [
        await ProjectButton.async_init(
            project["title"],
            f"Бустов {project["boosts"]}",
            page=page,
            project_id=project["_id"],
            place=place,
        )
        for place, project in enumerate(contest_projects_top, start=1)
    ]


async def project_users(project_id: PydanticObjectId) -> list[CircleAvatar]:
    """Возвращает аватарки пользователей проекта"""

    async with ClientSession() as client:
        project_responce = await client.get(f"{API_URL}/projects/get/{project_id}")
        users = [
            await (await client.get(f"{API_URL}/users/get/{user_link['id']}")).json()
            for user_link in (await project_responce.json())["users"]
        ]
    return [
        CircleAvatar(
            width=333,
            height=333,
            foreground_image_src=user["avatar"],
            background_image_src=user["avatar"],
            tooltip=user["username"],
            bgcolor=Colors.TRANSPARENT,
        )
        for user in users
    ]
