import datetime as dt
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from config import settings


class CreatedAtMixin:
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.now(tz=settings.time_zone), nullable=False
    )
