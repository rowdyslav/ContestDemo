from aiohttp import ClientSession
from flet import MainAxisAlignment, Page, Row, Text, TextAlign, TextThemeStyle

from controls.buttons import ProjectButton
from env import API_URL

from .buttons import ContestButton


async def contests(page: Page) -> Row:
    async with ClientSession() as client:
        return Row(
            [
                await ContestButton.ainit(contest["title"], page, contest["_id"])
                for contest in await (
                    await client.get(f"{API_URL}/contests/list")
                ).json()
            ],
            alignment=MainAxisAlignment.CENTER,
        )


async def projects_top(page: Page, contest_id: str) -> list[Row]:
    async with ClientSession() as client:
        projects_responce = await client.get(f"{API_URL}/projects/list/boosts")
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

    if not contest_projects:
        return [
            Row(
                [
                    Text(
                        "Проектов в этом контесте пока что нет...",
                        theme_style=TextThemeStyle.HEADLINE_LARGE,
                        text_align=TextAlign.CENTER,
                    )
                ],
                alignment=MainAxisAlignment.CENTER,
            )
        ]
    return [
        Row(
            [
                await ProjectButton.ainit(
                    project["title"],
                    f"Бустов {project["boosts"]}",
                    page,
                    project["_id"],
                    place,
                )
                for place, project in enumerate(contest_projects[:3], start=1)
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(
            [
                await ProjectButton.ainit(
                    project["title"],
                    f"Бустов {project["boosts"]}",
                    page,
                    project["_id"],
                )
                for project in contest_projects[3:]
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
    ]
