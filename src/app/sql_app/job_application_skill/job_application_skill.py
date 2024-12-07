import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.sql_app.database import Base


class JobApplicationSkill(Base):
    """
    Represents a skill associated with a Job application.

    Attributes:
        job_application_id (UUID): Foerign key referencing the related Job application.
        skill_id (UUID): Foerign key referencing the related Skill.
    """

    __tablename__ = "job_application_skill"

    job_application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_application.id"),
        nullable=False,
        primary_key=True,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skill.id"), primary_key=True
    )
