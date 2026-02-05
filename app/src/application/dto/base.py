from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DTO:
    """Base DTO class"""


DtoType = TypeVar("DtoType", bound=DTO)
