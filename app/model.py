from datetime import datetime
import uuid

from sqlalchemy import String, UUID, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from core.base_model import Base


class Todos(Base):
    __tablename__ = "todos"  # noqa

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    done: Mapped[datetime] = mapped_column(DateTime)
