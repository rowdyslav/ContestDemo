from aiohttp import ClientSession
from env import API_URL
from flet import (
    Button,
    Colors,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextAlign,
    TextThemeStyle,
)
from misc.tools import click_go


async def click_boost_project(project_id, user):
    async def _(e):
        async with ClientSession() as client:
            return await client.put(f"{API_URL}/projects/boost/{project_id}", json=user)

    return _


async def contests_row(page: Page) -> Row:
    async with ClientSession() as client:
        responce = await client.get(f"{API_URL}/contests/list/")
    contests = await responce.json()
    return Row(
        [
            Button(
                contest["title"],
                width=500,
                height=500,
                on_click=await click_go(page, f"/contests/{contest['title']}"),
            )
            for contest in contests
        ],
        alignment=MainAxisAlignment.CENTER,
    )


async def projects_top_rows(page: Page, contest_title: str) -> list[Row]:
    colors = {1: "#C9B037", 2: "#D7D7D7", 3: "#6A3805"}

    async with ClientSession() as client:
        projects_responce = await client.get(f"{API_URL}/projects/list/boosts")
        contests_responce = await client.get(f"{API_URL}/contests/list")
    contest = next(
        contest
        for contest in await contests_responce.json()
        if contest["title"] == contest_title
    )
    contest_projects = [
        project
        for project in await projects_responce.json()
        if project["_id"]
        in [project_link["id"] for project_link in contest["projects"]]
    ]

    if not contest_projects:
        return [
            Row(
                [
                    Text(
                        "Топа проектов пока что нет...",
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
                Button(
                    text=project["title"],
                    tooltip=f"Бустов {project["boosts"]}",
                    on_click=await click_go(
                        page, f"{page.route}/projects/{project['title']}"
                    ),
                    icon="WORKSPACE_PREMIUM_ROUNDED",
                    icon_color=colors.get(index),
                    height=250,
                    width=250,
                )
                for index, project in enumerate(contest_projects[:3], start=1)
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(
            [
                Button(
                    text=project["title"],
                    tooltip=f"Бустов {project["boosts"]}",
                    on_click=await click_go(
                        page, f"{page.route}/projects/{project['title']}"
                    ),
                    icon="WORKSPACE_PREMIUM_ROUNDED",
                    icon_color=Colors.PRIMARY,
                    height=250,
                    width=250,
                )
                for project in contest_projects[3:]
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
    ]
