from flet import (
    AppBar,
    AppView,
    Colors,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    RouteChangeEvent,
    TemplateRoute,
    TextButton,
    View,
    ViewPopEvent,
    app,
)

from controls import ContestsContainer, HomeContainer, ProjectsContainer


async def main(page: Page):
    page.title = "ContestDemo"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    async def route_change(_: RouteChangeEvent):
        page.views.clear()

        troute = TemplateRoute(page.route)
        if troute.match("/"):
            container = await HomeContainer.ainit(page)
        elif troute.match("/contests/:contest_id"):
            container = await ContestsContainer.ainit(page, troute.contest_id)  # type: ignore
        elif troute.match("/contests/:contest_id/projects/:project_id"):
            user = {
                "id": "66fe78b733afdb2c5807406c",
                "username": "rowdyslav",
                "email": "rowdyslav@gmail.com",
                "name": "Sergey",
                "surname": "Goretov",
            }  # TODO Авторизация, чтобы хранить объект пользователя
            container = await ProjectsContainer.ainit(troute.project_id, user)  # type: ignore
        page.views.append(
            View(
                controls=[
                    AppBar(
                        title=TextButton(
                            "ContestDemo",
                            on_click=lambda _: page.go("/"),
                            width=222,
                            height=222,
                        ),
                        bgcolor=Colors.SURFACE_CONTAINER_HIGHEST,
                        center_title=True,
                    ),
                    container,
                ]
            )
        )
        page.update()

    async def view_pop(_: ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        assert top_view.route
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


app(main, view=AppView.WEB_BROWSER, port=5000)
