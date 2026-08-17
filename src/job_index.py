from src.job_loader import load_jobs
from src.embedding_engine import create_embedding, job_to_text
from src.job_matcher import JobMatcher


def build_job_index(file_path: str):

    jobs = load_jobs(file_path)

    embeddings = []
    job_ids = []

    for job in jobs:

        job_text = job_to_text(job)

        embedding = create_embedding(job_text)

        embeddings.append(embedding)

        job_ids.append(job.id)

    dimension = len(embeddings[0])

    matcher = JobMatcher(dimension)

    matcher.add_embeddings(
        embeddings,
        job_ids
    )

    return jobs, matcher