import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.sql_app.database import Base
from app.sql_app.job_application.job_application import JobApplication

if TYPE_CHECKING:
    from app.sql_app import JobAd


class Skill(Base):
    """
    Represents a skill entity in the database.

    Attributes:
        id (uuid.UUID): Unique identifier for the skill.
        category_id (uuid.UUID): Foreign key referencing the category this skill belongs to.
        name (str): Name of the skill.
        job_ads (list[JobAd]): List of job advertisements associated with this skill.
        job_applications (list[JobApplication]): List of job applications associated with this skill.
    """

    __tablename__ = "skill"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("category.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    job_ads: Mapped[list["JobAd"]] = relationship(
        "JobAd",
        secondary="job_ad_skill",
        back_populates="skills",
        uselist=True,
        collection_class=list,
    )
    job_applications: Mapped[list["JobApplication"]] = relationship(
        "JobApplication",
        secondary="job_application_skill",
        back_populates="skills",
        uselist=True,
        collection_class=list,
    )
