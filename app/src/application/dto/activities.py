from dataclasses import dataclass, field
from typing import Optional

from application.dto.base import DTO


@dataclass(kw_only=True, slots=True, frozen=True)
class ActivityDTO(DTO):
    name: str
    parent_id: Optional[int] = None
    parent: Optional["ActivityDTO"] = None
    depth: int = 0
    children: list["ActivityDTO"] = field(default_factory=list)
