from asyncio import run

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
    app_async,
)
from flet.core.control_event import ControlEvent

from controls import ContestContainer, HomeContainer, ProjectContainer


async def main(page: Page):
    page.title = "ContestDemo"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    async def route_change(_: RouteChangeEvent | ControlEvent):
        page.views.clear()

        troute = TemplateRoute(page.route)
        if troute.match("/"):
            container_type, args = HomeContainer, {"page": page}
        elif troute.match("/contests/:contest_id"):
            container_type, args = ContestContainer, {"page": page, "contest_id": troute.contest_id}  # type: ignore
        elif troute.match("/contests/:contest_id/projects/:project_id"):
            user = ...  # TODO Авторизация, чтобы хранить объект пользователя
            container_type, args = ProjectContainer, {"project_id": troute.project_id, "user": user}  # type: ignore
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
                    await container_type.async_init(**args),  # type: ignore
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
    page.on_connect = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


async def app():
    await app_async(main, view=AppView.WEB_BROWSER)


run(app())
