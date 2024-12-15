from abc import abstractmethod
from typing import Self

from flet import Button, Colors, Page
from flet.core.control_event import ControlEvent
from flet.core.tooltip import TooltipValue


class CustomButton(Button):
    @staticmethod
    async def click_go(page: Page, path: str):
        async def go(_: ControlEvent):
            page.go(path)

        return go

    @classmethod
    @abstractmethod
    async def ainit(cls, text: str, tooltip: TooltipValue) -> Self:
        """Реализация метода должна устанавливать Button.text, Button.on_click, опционально Button.tooltip и возвращать объет класса"""
        custom_button = cls()
        custom_button.text = text
        custom_button.tooltip = tooltip


class ContestButton(CustomButton):
    """Button, представляющая карточку контеста"""

    def __init__(self):
        super().__init__()
        self.width = 500
        self.height = 500

    @classmethod
    async def ainit(cls, text: str, page: Page, *, contest_id: str) -> Self:
        contest_button = cls()
        contest_button.text = text

        contest_button.on_click = await cls.click_go(page, f"/contests/{contest_id}")
        return contest_button


class ProjectButton(CustomButton):
    """Button, представляющая карточку проекта"""

    place_colors = {1: "#C9B037", 2: "#D7D7D7", 3: "#6A3805"}

    def __init__(self):
        super().__init__()
        self.width = 333
        self.height = 333
        self.icon = "WORKSPACE_PREMIUM_ROUNDED"

    @classmethod
    async def ainit(
        cls,
        text: str,
        tooltip: TooltipValue,
        *,
        place: int,
        page: Page,
        project_id: str,
    ) -> Self:
        project_button = cls()
        project_button.text = text
        project_button.tooltip = tooltip
        project_button.icon_color = cls.place_colors.get(place) or Colors.PRIMARY

        project_button.on_click = await cls.click_go(
            page, f"{page.route}/projects/{project_id}"
        )
        return project_button
