from abc import abstractmethod
from typing import Self

from aiohttp import ClientSession
from flet import (
    Button,
    Column,
    Container,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextAlign,
    TextThemeStyle,
)
from flet.core.control_event import ControlEvent

from env import API_URL

from .rows import contests, projects_top


class CustomContainer(Container):
    @classmethod
    @abstractmethod
    async def ainit(cls, page: Page, **context) -> Self:
        """Реализация метода должна устанавливать Container.content и возвращать объет класса"""
        pass


class HomeContainer(CustomContainer):
    @classmethod
    async def ainit(cls, page: Page):
        home = cls()
        home.content = Column(
            [
                Text(
                    "Текущие контесты",
                    size=33,
                ),
                Row(
                    await contests(page),
                    alignment=MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        return home


class ContestContainer(CustomContainer):
    @classmethod
    async def ainit(cls, page: Page, contest_id: str):
        contest = cls()
        projects = await projects_top(page, contest_id)
        if projects:
            content = Column(
                (
                    Row(projects[:3], alignment=MainAxisAlignment.CENTER),
                    Row(projects[3:], alignment=MainAxisAlignment.CENTER),
                ),
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        else:
            content = Row(
                (
                    Text(
                        "Проектов в этом контесте пока что нет...",
                        theme_style=TextThemeStyle.HEADLINE_LARGE,
                    ),
                ),
                MainAxisAlignment.CENTER,
            )
        contest.content = content
        return contest


class ProjectContainer(CustomContainer):
    @staticmethod
    async def click_boost_project(project_id, user):
        async def boost_project(_: ControlEvent):
            async with ClientSession() as client:
                return await client.put(
                    f"{API_URL}/projects/boost/{project_id}", json=user
                )

        return boost_project

    @classmethod
    async def ainit(cls, project_id: str, user: dict):
        contest = cls()
        contest.content = Column(
            [
                Text("тут типо юзеры будут"),
                Button(
                    "Забустить!",
                    on_click=await cls.click_boost_project(project_id, user),
                ),
            ]
        )
        return contest
