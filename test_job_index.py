from src.job_index import build_job_index


jobs, matcher = build_job_index(
    "data/jobs.json"
)


print("Number of jobs:", len(jobs))

print(
    "Number of vectors in FAISS:",
    matcher.index.ntotal
)

print(
    "Stored job IDs:",
    matcher.job_ids
)