import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression, func

from app.sql_app.database import Base
from app.sql_app.professional.professional_status import ProfessionalStatus

if TYPE_CHECKING:
    from app.sql_app import City, JobApplication


class Professional(Base):
    """
    Represents a professional in the job matching application.

    Attributes:
        id (UUID): Unique identifier for the professional.
        sub (str, optional): Unique identifier for the professional in the authentication system.
        city_id (UUID): Foreign key referencing the city where the professional is located.
        username (str): Unique username for the professional.
        password (str): Password for the professional.
        description (str): Description of the professional.
        email (str): Unique email address of the professional.
        photo (bytes, optional): Photo of the professional.
        status (ProfessionalStatus): Current status of the professional.
        active_application_count (int): Number of active job applications by the professional.
        first_name (str): First name of the professional.
        last_name (str): Last name of the professional.

    Relationships:
        city (City): Relationship to the City model.
        job_applications (List[JobApplication]): Relationship to the JobApplication model.
    """

    __tablename__ = "professional"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    sub: Mapped[str] = mapped_column(String, nullable=True)
    city_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("city.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=True,
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    photo: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    cv: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    status: Mapped[ProfessionalStatus] = mapped_column(
        Enum(ProfessionalStatus, native_enum=True),
        nullable=False,
        server_default=expression.literal(ProfessionalStatus.ACTIVE.name),
    )
    active_application_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=expression.text("0")
    )
    has_private_matches: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    city: Mapped["City"] = relationship("City", back_populates="professionals")
    job_applications: Mapped[list["JobApplication"]] = relationship(
        "JobApplication",
        back_populates="professional",
        uselist=True,
        collection_class=list,
    )

    __table_args__ = (Index("unique_sub", "sub", postgresql_where=(sub.isnot(None))),)
