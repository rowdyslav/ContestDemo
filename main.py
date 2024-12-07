from flet import (
    AppBar,
    AppView,
    Button,
    Colors,
    Column,
    CrossAxisAlignment,
    ElevatedButton,
    MainAxisAlignment,
    Page,
    TemplateRoute,
    Text,
    View,
    app,
)
from misc.api_functions import click_boost_project, contests_row, projects_top_rows


async def main(page: Page):
    page.title = "ContestDemo"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    async def route_change(e):
        page.views.clear()

        troute = TemplateRoute(page.route)
        if troute.match("/"):
            view = View(
                "/",
                [
                    AppBar(
                        title=Text("ContestDemo"),
                        bgcolor=Colors.SURFACE_CONTAINER_HIGHEST,
                    ),
                    Column(
                        [
                            Text(
                                "Текущие контесты",
                                size=33,
                            ),
                            await contests_row(page),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                ],
            )
        elif troute.match("/contests/:contest_title"):
            view = View(
                controls=[
                    *await projects_top_rows(page, troute.contest_title),  # type: ignore
                    ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ],
            )
        elif troute.match("/contests/:contest_title/projects/:project_title"):
            project_id = (
                "67516811063070cda071abc9"  # TODO Пока есть только title, буст по id
            )
            user = {
                "id": "66fe78b733afdb2c5807406c",
                "username": "rowdyslav",
                "email": "rowdyslav@gmail.com",
                "name": "Sergey",
                "surname": "Goretov",
            }  # TODO Авторизация, чтобы хранить объект пользователя
            view = View(
                controls=[
                    Text("тут типо юзеры будут"),
                    Button(
                        "Забустить!",
                        on_click=await click_boost_project(project_id, user),
                    ),
                ]
            )
        page.views.append(view)
        page.update()

    async def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        assert top_view.route
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


app(main, view=AppView.WEB_BROWSER)
