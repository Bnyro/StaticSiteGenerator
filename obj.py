from dataclasses import dataclass

@dataclass
class Page:
    title: str
    location: str
    content: dict | None = None
    children: list | None = None

    def __lt__(self, other):
        return self.title < other.title
