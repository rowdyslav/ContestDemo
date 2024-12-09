from flet import (
    AppBar,
    Colors,
    Column,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    Text,
)

from misc.controls import contests_row

from . import AsyncContainer


class Home(AsyncContainer):
    @classmethod
    async def view(cls, page: Page):
        home = cls()
        home.content = Column(
            [
                Text(
                    "Текущие контесты",
                    size=33,
                ),
                await contests_row(page),
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        return home
