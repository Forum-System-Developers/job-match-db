import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.sql_app.category_job_application.category_job_application import (
    CategoryJobApplication,
)
from app.sql_app.database import Base
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.skill.skill import Skill

if TYPE_CHECKING:
    from app.sql_app import City, Match, Professional


class JobApplication(Base):
    """
    Represents a job application in the job matching database.

    Attributes:
        id (uuid.UUID): Unique identifier for the job application.
        name (str): Name of the job application.
        min_salary (float | None): Minimum salary for the job application.
        max_salary (float | None): Maximum salary for the job application.
        status (JobStatus): Status of the job application.
        description (str): Description of the job application.
        professional_id (uuid.UUID): Identifier for the associated professional.
        is_main (bool): Indicates if this is the main job application.
        created_at (datetime): Timestamp when the job application was created.
        updated_at (datetime): Timestamp when the job application was last updated.
        city_id (uuid.UUID): Identifier for the associated city.

    Relationships:
        professional (Professional): The professional associated with the job application.
        category_job_applications (CategoryJobApplication): The category job applications associated with the job application.
        skills (list[Skill]): The skills associated with the job application.
        matches (list[Match]): The matches associated with the job application.
        city (City): The city associated with the job application.
    """

    __tablename__ = "job_application"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    min_salary: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    max_salary: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    professional_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("professional.id"), nullable=False
    )
    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=True,
    )
    city_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("city.id"), nullable=False
    )

    professional: Mapped["Professional"] = relationship(
        "Professional", back_populates="job_applications"
    )
    category_job_applications: Mapped["CategoryJobApplication"] = relationship(
        "CategoryJobApplication", back_populates="job_application"
    )
    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        secondary="job_application_skill",
        back_populates="job_applications",
        uselist=True,
        collection_class=list,
    )
    matches: Mapped[list["Match"]] = relationship(
        "Match", back_populates="job_application", uselist=True, collection_class=list
    )
    city: Mapped["City"] = relationship("City", back_populates="job_applications")
