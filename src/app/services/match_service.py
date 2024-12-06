from uuid import UUID

from sqlalchemy.orm import Session

from app.schemas.match import MatchRequestAd
from app.sql_app.job_ad.job_ad import JobAd
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.match.match import Match
from app.sql_app.match.match_status import MatchStatus


def get_match_requests_for_professional(
    professional_id: UUID,
    db: Session,
) -> list[MatchRequestAd]:
    """
    Retrieve match requests for a given professional.

    This function queries the database to find all match requests for a
    professional where the job application status is active and the match
    status is requested by the job advertisement.

    Args:
        professional_id (UUID): The unique identifier of the professional.
        db (Session): The database session used for querying.

    Returns:
        list[MatchRequestAd]: A list of MatchRequestAd objects representing
        the match requests for the professional.
    """
    result = (
        db.query(Match, JobAd)
        .join(JobApplication, Match.job_application_id == JobApplication.id)
        .join(JobAd, Match.job_ad_id == JobAd.id)
        .filter(
            JobApplication.professional_id == professional_id,
            JobApplication.status == JobStatus.ACTIVE,
            Match.status == MatchStatus.REQUESTED_BY_JOB_AD,
        )
        .all()
    )

    return [
        MatchRequestAd.create_response(match=match, job_ad=ad) for (match, ad) in result
    ]
