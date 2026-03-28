import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class KnowledgeBaseTool:
    def __init__(self, kb_path="data/knowledge_base.json"):
        # Load embedding model (local)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load knowledge base
        with open(kb_path, "r") as f:
            self.data = json.load(f)

        # Extract fields
        self.texts = [item["problem"] for item in self.data]
        self.solutions = [item["solution"] for item in self.data]
        self.categories = [item.get("category", "General") for item in self.data]

        # Create embeddings
        self.embeddings = self.model.encode(self.texts)

        # Build FAISS index
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

    def search(self, query: str, category: str = None, k: int = 3) -> str:
        query_embedding = self.model.encode([query])

        D, I = self.index.search(np.array(query_embedding), k)

        results = []
        for idx in I[0]:
            if category and self.categories[idx] != category:
                continue

            results.append(
                f"\nResult:\n"
                f"Category: {self.categories[idx]}\n"
                f"Problem: {self.texts[idx]}\n"
                f"Solution: {self.solutions[idx]}\n"
            )

        if not results:
            return "No matching solutions found."

        return "\n".join(results)


# Create singleton instance
kb_tool = KnowledgeBaseTool()


# Function used by agent
def search_similar_solution(query: str, category: str = None) -> str:
    return kb_tool.search(query, category)