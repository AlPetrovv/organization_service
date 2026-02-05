from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from config import settings
from infra.resouces.database.utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    This class is inherited by all SQLAlchemy models defined in the application.
    It provides a common base class for all models and includes a common
    `__tablename__` method to automatically generate table names based on the
    class name.

    All models inherit from this class and are automatically registered with
    SQLAlchemy's metadata.

    Attributes:
        __abstract__ (bool): Indicates that this class is abstract and should
            not be mapped to the database.
        metadata (MetaData): The metadata object that SQLAlchemy uses to
            manage the database.

    """

    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls):
        return f"{camel_case_to_snake_case(cls.__name__)}"

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.__class__.__name__}"
