from flet import (
    AppView,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    RouteChangeEvent,
    TemplateRoute,
    View,
    ViewPopEvent,
    app,
)

from views import Contest, Home, Project


async def main(page: Page):
    page.title = "ContestDemo"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    async def route_change(_: RouteChangeEvent):
        page.views.clear()

        troute = TemplateRoute(page.route)
        if troute.match("/"):
            view = View(
                "/",
                [await Home.view(page)],
            )
        elif troute.match("/contests/:contest_id"):
            view = View(controls=[await Contest.view(page, troute.contest_id)])  # type: ignore
        elif troute.match("/contests/:contest_id/projects/:project_id"):
            user = {
                "id": "66fe78b733afdb2c5807406c",
                "username": "rowdyslav",
                "email": "rowdyslav@gmail.com",
                "name": "Sergey",
                "surname": "Goretov",
            }  # TODO Авторизация, чтобы хранить объект пользователя
            view = View(controls=[await Project.view(troute.project_id, user)])  # type: ignore
        page.views.append(view)
        page.update()

    async def view_pop(_: ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        assert top_view.route
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


app(main, view=AppView.WEB_BROWSER)
