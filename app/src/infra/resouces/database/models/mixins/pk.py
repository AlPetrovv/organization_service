from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import UUID, BigInteger
import uuid


class IDPKINTMixin:
    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class IDPKBIGINTMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)


class UUIDPKMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4)
