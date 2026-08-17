import faiss
import numpy as np


class JobMatcher:

    def __init__(self, dimension: int):

        self.index = faiss.IndexFlatL2(dimension)

        self.job_ids = []


    def add_embeddings(
        self,
        embeddings,
        job_ids
    ):

        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        self.index.add(vectors)

        self.job_ids.extend(job_ids)


    def search(
        self,
        query_embedding,
        top_k: int = 5
    ):

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_vector,
            top_k
        )

        job_ids = [
            self.job_ids[index]
            for index in indices[0]
        ]

        return distances[0], job_ids