from src.job_loader import load_jobs
from src.embedding_engine import job_to_text


jobs = load_jobs("data/jobs.json")


print("Number of jobs:", len(jobs))

print("\nFirst job:")

print(jobs[0])

print("\nJob text:")

print(job_to_text(jobs[0]))