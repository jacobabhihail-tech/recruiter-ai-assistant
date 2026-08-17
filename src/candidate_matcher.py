from src.candidate_schema import CandidateProfile
from src.intake_schema import CandidatePreferences
from src.embedding_engine import create_embedding


def candidate_to_text(
    candidate_profile: CandidateProfile,
    candidate_preferences: CandidatePreferences
) -> str:

    return f"""
    Candidate Role:
    {", ".join(candidate_profile.roles)}

    Skills:
    {", ".join(candidate_profile.skills)}

    Years of Experience:
    {candidate_profile.years_experience}

    Preferred Location:
    {candidate_preferences.preferred_location}

    Interested Role:
    {candidate_preferences.interested_role}

    Work Preference:
    {candidate_preferences.work_preference}
    """


def create_candidate_embedding(
    candidate_profile: CandidateProfile,
    candidate_preferences: CandidatePreferences
):

    candidate_text = candidate_to_text(
        candidate_profile,
        candidate_preferences
    )

    return create_embedding(candidate_text)