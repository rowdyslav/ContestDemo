from flet import Page
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()


async def click_go(page: Page, path: str):
    async def _(e):
        page.go(path)

    return _
