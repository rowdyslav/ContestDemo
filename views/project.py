from flet import Button, Column, Text

from misc.clicks import click_boost_project

from . import AsyncContainer


class Project(AsyncContainer):
    @classmethod
    async def view(cls, project_id: str, user: dict):
        contest = cls()
        contest.content = Column(
            [
                Text("тут типо юзеры будут"),
                Button(
                    "Забустить!", on_click=await click_boost_project(project_id, user)
                ),
            ]
        )
        return contest
