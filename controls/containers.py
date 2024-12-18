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

from .from_api import contests, project_users, projects_top


class CustomContainer(Container):
    """Container с асихнронной инициализацией async_init, который представляет собой страницу сайта"""

    @classmethod
    @abstractmethod
    async def async_init(cls) -> Self:
        """Реализация метода должна устанавливать Container.content и возвращать объет класса"""
        custom_container = cls()
        return custom_container


class HomeContainer(CustomContainer):
    """Container для индекса сайта"""

    @classmethod
    async def async_init(cls, *, page: Page):
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
    """Container для /contests/{contest_id}"""

    @classmethod
    async def async_init(cls, *, page: Page, contest_id: PydanticObjectId):
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
    """Container для /contests/{contest_id}/projects/{project_id}
    со вспомогательным статик методом click_boost_project для буста данного проекта"""

    User = dict[str, str | PydanticObjectId | EmailStr]

    @staticmethod
    async def click_boost_project(project_id: PydanticObjectId, user: User):
        """Возвращает асинхронную функцию для буста проекта project_id юзером user"""

        async def boost_project(_: ControlEvent):
            async with ClientSession() as client:
                return await client.put(
                    f"{API_URL}/projects/boost/{project_id}", json=user
                )

        return boost_project

    @classmethod
    async def async_init(cls, *, project_id: PydanticObjectId, user: User):
        project_container = cls()
        project_container.content = Column(
            [
                Text("Участники проекта"),
                Row(await project_users(project_id)),
                Button(
                    "Забустить!",
                    on_click=await cls.click_boost_project(project_id, user),
                ),
            ]
        )
        return project_container
