"""Типы кнопок, представляющие сущности приложения"""

from abc import abstractmethod
from typing import Self

from beanie import PydanticObjectId
from flet import Button, Colors, Icons, Page
from flet.core.control_event import ControlEvent
from flet.core.tooltip import TooltipValue


class CustomButton(Button):
    """Button, с асихнронной инициализацией async_init и вспомогательным статик методом go_on_click для навигации по странице"""

    @staticmethod
    async def go_on_click(page: Page, path: str):
        """Возвращает асинхронную функцию для перехода страницы page по пути path"""

        async def go(_: ControlEvent):
            page.go(path)

        return go

    @classmethod
    @abstractmethod
    async def async_init(cls, text: str, tooltip: TooltipValue = None) -> Self:
        """Реализация метода должна устанавливать Button.text, Button.tooltip, Button.on_click и возвращать объет класса"""
        custom_button = cls()
        custom_button.text = text
        custom_button.tooltip = tooltip


class ContestButton(CustomButton):
    """Button, представляющий контест"""

    def __init__(self):
        super().__init__()
        self.width = 555
        self.height = 555
        self.icon = Icons.random()  # ! ROFL

    @classmethod
    async def async_init(
        cls, text: str, tooltip: TooltipValue = None, *, page: Page, contest_id: str
    ) -> Self:
        self = cls()
        self.text = text
        self.tooltip = tooltip

        self.on_click = await cls.go_on_click(page, f"/contests/{contest_id}")
        return self


class ProjectButton(CustomButton):
    """Button, представляющий проект"""

    place_colors = {1: "#C9B037", 2: "#D7D7D7", 3: "#6A3805"}

    def __init__(self):
        super().__init__()
        self.width = 333
        self.height = 333
        self.icon = "WORKSPACE_PREMIUM_ROUNDED"

    @classmethod
    async def async_init(
        cls,
        text: str,
        tooltip: TooltipValue = None,
        *,
        page: Page,
        project_id: PydanticObjectId,
        place: int,
    ) -> Self:
        self = cls()
        self.text = text
        self.tooltip = tooltip
        self.icon_color = cls.place_colors.get(place) or Colors.PRIMARY

        self.on_click = await cls.go_on_click(
            page, f"{page.route}/projects/{project_id}"
        )
        return self
