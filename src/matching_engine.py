from src.candidate_matcher import create_candidate_embedding
from src.job_index import build_job_index


def find_matching_jobs(
    candidate_profile,
    candidate_preferences,
    job_file_path: str,
    top_k: int = 5
):

    jobs, matcher = build_job_index(
        job_file_path
    )

    candidate_embedding = create_candidate_embedding(
        candidate_profile,
        candidate_preferences
    )

    distances, job_ids = matcher.search(
        candidate_embedding,
        top_k
    )

    matched_jobs = []

    for distance, job_id in zip(
        distances,
        job_ids
    ):

        job = next(
            job
            for job in jobs
            if job.id == job_id
        )

        matched_jobs.append(
            {
                "job": job,
                "distance": float(distance)
            }
        )

    return matched_jobs