import flet as ft
from aiohttp import ClientSession
from flet import (
    AppBar,
    Button,
    Colors,
    ElevatedButton,
    Page,
    Row,
    TemplateRoute,
    Text,
    TextAlign,
    TextThemeStyle,
    View,
)

URL = "http://127.0.0.1:8000"


async def go(page: Page, path: str):
    async def _(e):
        page.go(path)

    return _


async def get_contests_row(page: Page):
    async with ClientSession() as client:
        responce = await client.get(f"{URL}/contests/list/")
    contests = await responce.json()
    return Row(
        [
            Button(
                contest["title"],
                width=500,
                height=500,
                on_click=await go(page, f"/contests/{contest['title']}"),
            )
            for contest in contests
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )


async def get_projects_top(page: Page, contest_title: str):
    colors = {1: "#C9B037", 2: "#D7D7D7", 3: "#6A3805"}

    async with ClientSession() as client:
        projects_responce = await client.get(f"{URL}/projects/list/boosts")
        contests_responce = await client.get(f"{URL}/contests/list")
    contest = next(
        contest
        for contest in await contests_responce.json()
        if contest["title"] == contest_title
    )
    contest_projects = [
        project
        for project in await projects_responce.json()
        if project["_id"] in [project["id"] for project in contest["projects"]]
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
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]

    return [
        Row(
            [
                Button(
                    text=project["title"],
                    tooltip=f"{project["boosts"]} бустов",
                    on_click=await go(
                        page, f"{page.route}/projects/{project['title']}"
                    ),
                    icon="WORKSPACE_PREMIUM_ROUNDED",
                    icon_color=colors.get(index),
                    height=250,
                    width=250,
                )
                for index, project in enumerate(contest_projects[:3], start=1)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        Row(
            [
                Button(
                    text=project["title"],
                    tooltip=f"{project["boosts"]} бустов",
                    on_click=await go(
                        page, f"{page.route}/projects/{project['title']}"
                    ),
                    icon="WORKSPACE_PREMIUM_ROUNDED",
                    icon_color=Colors.PRIMARY,
                    height=250,
                    width=250,
                )
                for project in contest_projects[3:]
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]


async def main(page: Page):
    page.title = "ContestDemo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(
                        title=Text("ContestDemo"),
                        bgcolor=Colors.SURFACE_CONTAINER_HIGHEST,
                    ),
                    await get_contests_row(page),
                ],
            )
        )

        troute = TemplateRoute(page.route)

        if troute.match("/contests/:contest_title"):
            page.views.append(
                View(
                    controls=[
                        *await get_projects_top(page, troute.contest_title),  # type: ignore
                        ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        elif troute.match("/contests/:contest_title/projects/:project_title"):
            page.views.append(View(controls=[Text("тут типо юзеры будут")]))
        page.update()

    async def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        assert top_view.route
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


ft.app(main, view=ft.AppView.WEB_BROWSER)
