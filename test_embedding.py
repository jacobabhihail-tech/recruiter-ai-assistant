from src.embedding_engine import create_embedding


text = """
Python Backend Developer.
Skills: Python, FastAPI, Django, PostgreSQL, Docker.
Location: Bangalore.
Experience: 3+ years.
"""


embedding = create_embedding(text)


print("Embedding type:", type(embedding))
print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])