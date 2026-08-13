from src.llm import extract_candidate_profile

resume_text = """
John Doe

Python Developer

Professional Summary:
Python developer with 4 years of experience building web applications
and data processing systems.

Skills:
Python, Django, FastAPI, SQL, PostgreSQL, AWS, Docker

Experience:
Python Developer - ABC Technologies - 2022 to Present
Software Developer - XYZ Solutions - 2020 to 2022

Education:
Bachelor of Technology in Computer Science
"""

profile = extract_candidate_profile(resume_text)

print("\n Candidate Profile")
print(profile.model_dump_json(indent=4))

