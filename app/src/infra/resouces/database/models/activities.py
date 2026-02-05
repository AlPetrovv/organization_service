from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, SmallInteger, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from infra.resouces.database.models import Base

from infra.resouces.database.models.mixins import IDPKINTMixin

if TYPE_CHECKING:
    from infra.resouces.database.models import Organization


class Activity(IDPKINTMixin, Base):
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("activity.id"), index=True)
    parent: Mapped[Optional["Activity"]] = relationship(
        "Activity", remote_side="Activity.id", back_populates="children", lazy="joined", join_depth=3
    )
    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary="organization_activity_association",
        back_populates="activities",
        lazy="selectin",
    )
    depth: Mapped[int] = mapped_column(SmallInteger, default=1)

    __table_args__ = (
        CheckConstraint(
            "depth BETWEEN 1 AND 3",
            name="activity_depth_check",
        ),
    )
