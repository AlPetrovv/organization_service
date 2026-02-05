from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PhoneNumber, PhoneNumberType


from .base import Base
from .mixins import IDPKBIGINTMixin, CreatedAtMixin, UUIDPKMixin

if TYPE_CHECKING:
    from .buildings import Building
    from .activities import Activity


class Organization(UUIDPKMixin, CreatedAtMixin, Base):
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phones: Mapped[list["OrganizationPhoneNumber"]] = relationship(
        "OrganizationPhoneNumber",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary="organization_activity_association",
        back_populates="organizations",
        lazy="selectin",
    )
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id", ondelete="CASCADE"))
    building: Mapped["Building"] = relationship("Building", back_populates="organizations", lazy="selectin")


class OrganizationPhoneNumber(IDPKBIGINTMixin, CreatedAtMixin, Base):
    phone: Mapped[PhoneNumber] = mapped_column(PhoneNumberType(), unique=True, index=True)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"))
    organization: Mapped["Organization"] = relationship("Organization", back_populates="phones", lazy="joined")
