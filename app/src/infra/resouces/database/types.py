from pydantic import BaseModel
from typing import TypeVar, Type

from infra.resouces.database.models import Base


# Type model that inherit from Base, Every model in database inherit from Base
MODEL = TypeVar("MODEL", bound=Base)

# Type model class(for typing)
TYPE_MODEL = Type[MODEL]

PYDANTIC_MODEL = TypeVar("PYDANTIC_MODEL", bound=BaseModel)
