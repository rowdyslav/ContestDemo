from abc import abstractmethod
from typing import Self

from flet import Column, Container, Row


class AsyncContainer(Container):
    def __init__(self):
        super().__init__()
        self.content: Column | Row

    @classmethod
    @abstractmethod
    async def view(cls, page, **context) -> Self:
        pass


from .contest import Contest
from .home import Home
from .project import Project
