from typing import TYPE_CHECKING

from geoalchemy2 import WKBElement, Geometry
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins import IDPKBIGINTMixin

if TYPE_CHECKING:
    from .organizations import Organization

WGS84 = 4326


class Building(IDPKBIGINTMixin, Base):
    address: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    location: Mapped[WKBElement] = mapped_column(Geometry(geometry_type="POINT", srid=WGS84, nullable=False))
    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        back_populates="building",
        lazy="joined",
    )

    def __str__(self):
        return f"{self.address}"
