from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from infra.resouces.database.models import Base
from infra.resouces.database.models.mixins import IDPKBIGINTMixin


class OrganizationActivityAssociation(IDPKBIGINTMixin, Base):
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), index=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id", ondelete="CASCADE"), index=True)
