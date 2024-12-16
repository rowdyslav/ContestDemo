from abc import abstractmethod
from typing import Self

from flet import Button, Colors, Page
from flet.core.control_event import ControlEvent
from flet.core.tooltip import TooltipValue


class CustomButton(Button):
    """Button, с асихнронной инициализацией async_init и вспомогательным статик методом click_go для навигации по странице"""

    @staticmethod
    async def click_go(page: Page, path: str):
        """Возвращает асинхронную функцию для перехода страницы page по пути path"""

        async def go(_: ControlEvent):
            page.go(path)

        return go

    @classmethod
    @abstractmethod
    async def async_init(cls, text: str, tooltip: TooltipValue) -> Self:
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

    @classmethod
    async def async_init(
        cls, text: str, tooltip: TooltipValue = None, *, page: Page, contest_id: str
    ) -> Self:
        contest_button = cls()
        contest_button.text = text
        contest_button.tooltip = tooltip

        contest_button.on_click = await cls.click_go(page, f"/contests/{contest_id}")
        return contest_button


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
        project_id: str,
        place: int,
    ) -> Self:
        project_button = cls()
        project_button.text = text
        project_button.tooltip = tooltip
        project_button.icon_color = cls.place_colors.get(place) or Colors.PRIMARY

        project_button.on_click = await cls.click_go(
            page, f"{page.route}/projects/{project_id}"
        )
        return project_button
