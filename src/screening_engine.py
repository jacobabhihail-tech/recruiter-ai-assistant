from src.screening_schema import ScreeningResult


def calculate_screening_score(
    candidate_profile,
    candidate_preferences,
    job
):

    candidate_skills = {
        skill.lower()
        for skill in candidate_profile.skills
    }

    job_skills = {
        skill.lower()
        for skill in job.skills
    }


    # --------------------------------------------------
    # SKILL MATCH
    # --------------------------------------------------

    matched_skills = (
        candidate_skills.intersection(
            job_skills
        )
    )

    missing_skills = (
        job_skills - candidate_skills
    )


    if job_skills:

        skill_score = (
            len(matched_skills)
            / len(job_skills)
        )

    else:

        skill_score = 0


    # --------------------------------------------------
    # EXPERIENCE MATCH
    # --------------------------------------------------

    candidate_experience = (
        candidate_profile.years_experience
    )

    required_experience = (
        int(
            job.experience
            .replace("+ years", "")
            .replace(" years", "")
            .replace(" year", "")
            .strip()
        )
    )


    experience_match = (
        candidate_experience
        >= required_experience
    )


    experience_score = (
        1
        if experience_match
        else 0
    )


    # --------------------------------------------------
    # LOCATION MATCH
    # --------------------------------------------------

    candidate_location = (
        candidate_preferences
        .preferred_location
        .lower()
        .strip()
    )

    job_location = (
        job.location
        .lower()
        .strip()
    )


    location_match = (
        candidate_location
        == job_location
    )


    location_score = (
        1
        if location_match
        else 0
    )


    # --------------------------------------------------
    # FINAL MATCH SCORE
    # --------------------------------------------------

    match_score = (
        skill_score * 60
        + experience_score * 25
        + location_score * 15
    )


    return ScreeningResult(

        match_score=round(
            match_score,
            2
        ),

        skill_overlap=sorted(
            matched_skills
        ),

        missing_skills=sorted(
            missing_skills
        ),

        experience_match=experience_match,

        location_match=location_match
    )