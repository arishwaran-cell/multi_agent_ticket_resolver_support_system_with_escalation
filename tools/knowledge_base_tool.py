import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class KnowledgeBaseTool:
    def __init__(self, kb_path="data/knowledge_base.json"):
        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load knowledge base
        with open(kb_path, "r") as f:
            self.data = json.load(f)

        # Extract fields
        self.texts = [item["problem"] for item in self.data]
        self.solutions = [item["solution"] for item in self.data]
        self.categories = [item.get("category", "General") for item in self.data]

        # Create embeddings (normalized for cosine similarity)
        self.embeddings = self.model.encode(self.texts, normalize_embeddings=True)

        # FAISS index (cosine similarity)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(np.array(self.embeddings))

    def search(self, query: str, category: str = None, k: int = 5) -> str:
        query_embedding = self.model.encode([query], normalize_embeddings=True)

        D, I = self.index.search(np.array(query_embedding), k)

        results = []

        for rank, idx in enumerate(I[0]):
            score = float(D[0][rank])

            # Soft category filter
            if category:
                if category.lower() not in self.categories[idx].lower():
                    continue

            results.append({
                "score": score,
                "category": self.categories[idx],
                "problem": self.texts[idx],
                "solution": self.solutions[idx]
            })

        # 🔥 fallback if nothing matched category
        if not results:
            for rank, idx in enumerate(I[0]):
                results.append({
                    "score": float(D[0][rank]),
                    "category": self.categories[idx],
                    "problem": self.texts[idx],
                    "solution": self.solutions[idx]
                })

        # Sort by best similarity
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        best = results[0]

        return (
            f"Category: {best['category']}\n"
            f"Problem: {best['problem']}\n"
            f"Solution: {best['solution']}"
        )


# Singleton
kb_tool = KnowledgeBaseTool()


def search_similar_solution(query: str, category: str = None) -> str:
    return kb_tool.search(query, category)