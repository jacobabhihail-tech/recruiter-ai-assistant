import json

from src.job_schema import Job


def load_jobs(file_path: str) -> list[Job]:

    with open(file_path, "r", encoding="utf-8") as file:

        jobs_data = json.load(file)

    jobs = [
        Job(**job)
        for job in jobs_data
    ]

    return jobs