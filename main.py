import flet as ft
from aiohttp import ClientSession
from flet import CupertinoIcons, FilledButton, Icons, Page, Row
from icecream import ic

URL = "http://127.0.0.1:8000"


async def main(page: Page):
    page.title = "ContestDemo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    async with ClientSession() as client:
        responce = await client.get(f"{URL}/projects/list/boosts")
        projects = await responce.json()
    ic(projects)
    page.add(
        Row(
            [
                FilledButton(
                    text=project["name"],
                    tooltip=project["description"],
                    url=f"/project/{project['name']}",
                    icon=CupertinoIcons.PROJECTIVE,
                    height=250,
                    width=250,
                )
                for index, project in enumerate(projects)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(main)
