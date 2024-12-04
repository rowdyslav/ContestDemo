import flet as ft
from aiohttp import ClientSession
from flet import Button, Colors, Page, Row, Text, TextAlign, TextThemeStyle

URL = "http://127.0.0.1:8000"


async def add_contests_list(page):
    async with ClientSession() as client:
        responce = await client.get(f"{URL}/contests/list/")
    contests = await responce.json()
    page.add(
        Row(
            [
                Button(text=contest["title"], height=500, width=500)
                for contest in contests
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


async def add_projects_top(page):
    colors = {1: "#C9B037", 2: "#D7D7D7", 3: "#6A3805"}

    async with ClientSession() as client:
        responce = await client.get(f"{URL}/projects/list/boosts")
    projects = await responce.json()

    page.add(
        Row(
            [
                Button(
                    text=project["title"],
                    tooltip=f"{project["boosts"]} бустов",
                    url=f"/project/{project['title']}",
                    icon="WORKSPACE_PREMIUM_ROUNDED",
                    icon_color=colors.get(index),
                    height=250,
                    width=250,
                )
                for index, project in enumerate(projects[:3], start=1)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        Row(
            [
                Button(
                    text=project["title"],
                    tooltip=f"{project["boosts"]} бустов",
                    url=f"/project/{project['title']}",
                    icon="WORKSPACE_PREMIUM_ROUNDED",
                    icon_color=Colors.PRIMARY,
                    height=250,
                    width=250,
                )
                for project in projects[3:]
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
    if not projects:
        page.add(
            Text(
                "Топа проектов пока что нет...",
                theme_style=TextThemeStyle.HEADLINE_LARGE,
                text_align=TextAlign.CENTER,
            )
        )

    page.update()


async def main(page: Page):
    page.title = "ContestDemo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def update(e=None):
        if page.controls:
            page.controls.clear()
        await add_contests_list(page)
        await add_projects_top(page)

    page.on_connect = update

    await update()


ft.app(main)
