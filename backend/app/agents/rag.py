import json
import math
import re
from typing import List, Dict, Any, Tuple
from backend.app.config import OPENAI_API_KEY

class RetrievalAgent:
    def __init__(self, schemes: List[Dict[str, Any]]):
        self.schemes = schemes
        self.api_key = OPENAI_API_KEY
        # Precompute terms for BM25-like search
        self.documents = []
        self._build_index()

    def _build_index(self):
        """
        Builds a flat list of FAQ objects and Scheme summaries for text searching.
        """
        for scheme in self.schemes:
            # 1. Add FAQs as individual searchable units
            for faq in scheme.get("faqs", []):
                self.documents.append({
                    "type": "faq",
                    "scheme_id": scheme["scheme_id"],
                    "scheme_name": scheme["scheme_name"],
                    "title": faq["question"],
                    "content": faq["answer"],
                    "official_link": scheme["official_link"]
                })
            
            # 2. Add Scheme overview
            benefits_str = " ".join(scheme.get("benefits", []))
            self.documents.append({
                "type": "scheme_overview",
                "scheme_id": scheme["scheme_id"],
                "scheme_name": scheme["scheme_name"],
                "title": scheme["scheme_name"],
                "content": f"{scheme['ministry']} - State: {scheme['state']}. Benefits: {benefits_str}",
                "official_link": scheme["official_link"]
            })

    def _tokenize(self, text: str) -> List[str]:
        """
        Simple tokenizer removing punctuation and converting to lowercase.
        """
        return re.findall(r"\w+", text.lower())

    def _calculate_overlap(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        """
        Calculates simple Jaccard-like overlap coefficient.
        """
        if not doc_tokens or not query_tokens:
            return 0.0
        
        q_set = set(query_tokens)
        d_set = set(doc_tokens)
        
        intersection = q_set.intersection(d_set)
        if not intersection:
            return 0.0
            
        # Give higher weight to matches of important keywords
        score = sum(2.0 if len(token) > 4 else 1.0 for token in intersection)
        return score / (math.log(len(d_set) + 1) + 1.0)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the FAQ & Scheme Index.
        Supports OpenAI Semantic search if key is active, otherwise falls back to token matching.
        """
        if self.api_key:
            try:
                return self._search_with_openai(query, top_k)
            except Exception as e:
                # Log error and fallback
                pass

        # Local Fallback
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return self.documents[:top_k]

        scored_docs = []
        for doc in self.documents:
            title_tokens = self._tokenize(doc["title"])
            content_tokens = self._tokenize(doc["content"])
            
            # Match query against both title and content
            title_score = self._calculate_overlap(query_tokens, title_tokens) * 2.0  # weight title higher
            content_score = self._calculate_overlap(query_tokens, content_tokens)
            
            total_score = title_score + content_score
            if total_score > 0:
                scored_docs.append((total_score, doc))
        
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored_docs[:top_k]]
        
        # If nothing matches, return first few documents as default reference
        if not results:
            results = self.documents[:top_k]
            
        return results

    def _search_with_openai(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """
        Mocks or performs vector cosine-similarity using OpenAI embeddings if implemented.
        For simplicity, if OpenAI is configured, we use standard ChatCompletion to find the most relevant FAQ.
        This fits the agentic pattern perfectly and does not require a heavy vector database setup locally.
        """
        import openai
        client = openai.OpenAI(api_key=self.api_key)
        
        # Format candidate documents for LLM context matching
        candidates = []
        for idx, doc in enumerate(self.documents):
            candidates.append({
                "idx": idx,
                "title": doc["title"],
                "content": doc["content"]
            })
            
        prompt = f"""
        You are a government welfare retrieval assistant. Given a user query and a list of scheme FAQs/descriptions, select the top 3 most relevant items.
        
        User Query: "{query}"
        
        Candidates:
        {json.dumps(candidates, ensure_ascii=False)[:4000]}
        
        Return ONLY a JSON list of the top 3 indices in order of relevance. Format: [idx1, idx2, idx3]
        No explanation or markdown formatting.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        res_text = response.choices[0].message.content.strip()
        indices = json.loads(res_text)
        
        results = []
        for idx in indices:
            if 0 <= idx < len(self.documents):
                results.append(self.documents[idx])
                
        return results
