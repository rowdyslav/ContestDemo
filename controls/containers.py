from abc import abstractmethod
from typing import Self

from aiohttp import ClientSession
from beanie import PydanticObjectId
from flet import (
    Button,
    Column,
    Container,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextThemeStyle,
)
from flet.core import alignment
from flet.core.control_event import ControlEvent
from pydantic import EmailStr

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
        home_container = cls()
        home_container.content = Column(
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
        return home_container


class ContestContainer(CustomContainer):
    @classmethod
    async def ainit(cls, page: Page, contest_id: PydanticObjectId):
        contest_container = cls()
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
            content = Container(
                Text(
                    "Проектов в этом контесте пока что нет...",
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                ),
                alignment=alignment.center,
            )
        contest_container.content = content
        return contest_container


class ProjectContainer(CustomContainer):
    User = dict[str, str | PydanticObjectId | EmailStr]

    @staticmethod
    async def click_boost_project(project_id: PydanticObjectId, user: User):
        async def boost_project(_: ControlEvent):
            async with ClientSession() as client:
                return await client.put(
                    f"{API_URL}/projects/boost/{project_id}", json=user
                )

        return boost_project

    @classmethod
    async def ainit(cls, project_id: PydanticObjectId, user: User):
        project_container = cls()
        project_container.content = Column(
            [
                Text("тут типо юзеры будут"),
                Button(
                    "Забустить!",
                    on_click=await cls.click_boost_project(project_id, user),
                ),
            ]
        )
        return project_container
