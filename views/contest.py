from flet import Button, Column, Page

from misc.controls import projects_top_rows

from . import AsyncContainer


class Contest(AsyncContainer):
    @classmethod
    async def view(cls, page: Page, contest_id: str):
        contest = cls()
        contest.content = Column([*await projects_top_rows(page, contest_id)])
        return contest
