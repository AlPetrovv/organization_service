from dataclasses import dataclass, field
from typing import Optional, Self

from domain.entities.base import Entity


@dataclass(kw_only=True, slots=True)
class ActivityEntity(Entity[int]):
    name: str
    parent_id: Optional[int] = field(default=None)
    parent: Optional[Self] = field(default=None)
    children: list[Self] = field(default_factory=list, compare=False)
    depth: int = field(default=0)

    MAX_DEPTH: int = 3

    def __post_init__(self) -> None:
        if self.parent is not None:
            if self.parent.id is None:
                raise ValueError("parent should have id")

            self.parent_id = self.parent.id

            new_depth = self.parent.depth + 1
            if new_depth > self.MAX_DEPTH:
                raise ValueError(
                    f"Can not more then {self.MAX_DEPTH} " f" ({self.MAX_DEPTH}). Parent depth: {self.parent.depth}"
                )

            self.depth = new_depth

        else:
            self.depth = 0
            self.parent_id = None
