
from uuid import (
    uuid4,
)

from sqlalchemy import (
    UUID,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_'

    id: Mapped[str] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )


class File(Base):
    __tablename__ = 'file'

    uuid: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_.id'),
    )
    file_path: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
