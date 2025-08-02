import logging
import logging.config
import openai
from typing import List, Dict, Optional, Literal
from .qdrant_client import search_vectors
from .ingestion import embed_text

# Load logging configuration if not already loaded
import os
LOGGING_CONF_PATH = os.path.join(os.path.dirname(__file__), '../../logging.conf')
if os.path.exists(LOGGING_CONF_PATH):
    logging.config.fileConfig(LOGGING_CONF_PATH, disable_existing_loggers=False)
logger = logging.getLogger('ai_manager')

class QueryIntent:
    PERSONAL = "personal"
    GLOBAL = "global"
    HYBRID = "hybrid"

class Agent:
    """
    Agentic orchestration for intent classification, retriever selection, and prompt construction.
    """
    def classify_intent(self, query: str) -> Literal["personal", "global", "hybrid"]:
        """
        Classify query intent using LLM-based intent detection.
        """
        logger.info(f"Classifying intent for query: {query}")
        try:
            prompt = (
                "You are an expert assistant. Classify the user query as 'personal', 'global', or 'hybrid'. "
                "Return the classification as a string.\n\n"
                f"User Query: {query}"
            )
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.0
            )
            classification = response.choices[0].message.content.strip().lower()
            # Extract only 'personal', 'global', or 'hybrid' from the output
            if "personal" in classification:
                classification = "personal"
            elif "global" in classification:
                classification = "global"
            elif "hybrid" in classification:
                classification = "hybrid"
            else:
                logger.warning(f"LLM intent classification output unrecognized: {classification}. Using fallback.")
                raise ValueError('Unrecognized intent')
            logger.info(f"Intent classified as {classification}.")
            return classification
        except Exception as e:
            logger.error(f"Error in LLM-based intent classification: {e}")
            # Fallback to keyword-based classification
            personal_keywords = ["my", "me", "mine", "personal", "myself", "upload", "show", "schedule"]
            global_keywords = ["industry", "trend", "market", "best practice", "professional", "general"]
            query_lower = query.lower()
            has_personal = any(word in query_lower for word in personal_keywords)
            has_global = any(word in query_lower for word in global_keywords)
            if has_personal:
                if has_global:
                    logger.info("Intent classified as HYBRID.")
                    return QueryIntent.HYBRID
                logger.info("Intent classified as PERSONAL.")
                return QueryIntent.PERSONAL
            if has_global:
                logger.info("Intent classified as GLOBAL.")
                return QueryIntent.GLOBAL
            logger.info("Intent classified as HYBRID (default).")
            return QueryIntent.HYBRID  # Default to hybrid for ambiguous queries


    def retrieve_context(self, query: str, user_id: Optional[int] = None, intent: Optional[str] = None, top_k: int = 3) -> Dict[str, List[str]]:
        """
        Retrieve context for a query. Global KB is always included for managerial insights.
        Always use LLM-based re-ranking.
        Returns a dict with 'personal' and 'global' keys.
        """
        logger.info(f"Retrieving context for query: {query}, user_id: {user_id}, intent: {intent}, top_k: {top_k}")
        context = {}
        try:
            # For now, only use OpenAI embedding for retrieval (future-proof for hybrid)
            query_embeddings = embed_text([query])
            if len(query_embeddings[0]) >= 1:
                query_embedding_openai = query_embeddings[0][0]
            else:
                raise RuntimeError('Failed to generate OpenAI query embedding.')
        except Exception as e:
            logger.error(f"Error embedding query: {e}")
            return context
        # Modular retrieval: try each KB independently, log and continue on error
        # Global KB retrieval
        try:
            # Only use OpenAI embedding for search (future: add hybrid search here)
            global_results = search_vectors(query_embedding_openai, collection='global_kb', top=top_k)
            context['global'] = [r['payload']['chunk'] for r in global_results.get('result', []) if 'payload' in r and 'chunk' in r['payload']]
            logger.info(f"Retrieved {len(context['global'])} global KB chunks.")
        except Exception as e:
            logger.warning(f"Global KB retrieval failed: {e}")
        # Personal KB retrieval
        if intent and user_id and intent.lower() in (QueryIntent.PERSONAL, QueryIntent.HYBRID):
            try:
                # Only use OpenAI embedding for search (future: add hybrid search here)
                personal_results = search_vectors(query_embedding_openai, collection='personal_kb', top=top_k)
                filtered = [r for r in personal_results.get('result', []) if r['payload'].get('user_id') == user_id]
                context['personal'] = [r['payload']['chunk'] for r in filtered if 'payload' in r and 'chunk' in r['payload']]
                logger.info(f"Retrieved {len(context['personal'])} personal KB chunks.")
            except Exception as e:
                logger.warning(f"Personal KB retrieval failed: {e}")
        # LLM-based re-ranking
        if context.get('global') or context.get('personal'):
            logger.info("Re-ranking context chunks using LLM.")
            chunks = context.get('global', []) + context.get('personal', [])
            ranked_chunks = self.llm_rerank(query, chunks)
            context['global'] = [chunk for chunk in ranked_chunks if chunk in context.get('global', [])]
            context['personal'] = [chunk for chunk in ranked_chunks if chunk in context.get('personal', [])]
        return context

    def merge_results(self, result1, result2, result3):
        merged = result1.get('result', []) + result2.get('result', []) + result3.get('result', [])
        merged = list({r['id']: r for r in merged}.values())
        return {'result': merged}

    def build_prompt(self, context: Dict[str, List[str]], query: str) -> str:
        """
        Construct a prompt with clear context source separation.
        """
        logger.info(f"Building prompt for query: {query}")
        prompt = []
        # Persona and anti-generic instructions (always prepend)
        persona_header = (
            "You are not a generic AI. You are the user's dedicated personal manager for their music artist career. "
            "Act as a comprehensive music manager for artists, overseeing all aspects of their careers. Provide strategic guidance on branding, marketing, release schedules, touring, collaborations, and fan engagement. Develop and critique business plans, assist with contract interpretation, plan music releases and promotional campaigns, and advise on financial planning for sustainability. Support day-to-day operations such as managing a team (e.g., publicists, producers, stylists), scheduling, and digital presence. "
            "Never act as a generic AI. Always tailor your advice to the user's goals, context, and artist career. "
            "If you lack information, ask clarifying questions as a manager would. "
            "If you must rely on general knowledge, relate it to the music industry and the user's career.\n"
        )
        prompt.append(persona_header)
        if context.get('global'):
            prompt.append("Global Knowledge (industry best practices):\n" + "\n---\n".join(context['global']))
        if context.get('personal'):
            prompt.append("Personal Knowledge (your data):\n" + "\n---\n".join(context['personal']))
        if not (context.get('global') or context.get('personal')):
            prompt.append("No specific context available. Relate your answer to the user's music career and goals.")
        prompt.append(f"\nUser Query: {query}")
        final_prompt = "\n\n".join(prompt)
        logger.info(f"Final constructed prompt: {final_prompt[:200]}... (truncated)")
        logger.debug(f"Full prompt sent to LLM: {final_prompt}")
        return final_prompt

    def llm_rerank(self, query: str, chunks: list) -> list:
        """
        Use LLM to re-rank chunks by relevance to the query. Returns sorted list of chunks.
        """
        import openai
        logger.info(f"LLM re-ranking {len(chunks)} chunks for query: {query}")
        try:
            prompt = (
                "You are an expert assistant. Given the user query and a list of context passages, "
                "rank the passages by their relevance to the query. "
                "Return ONLY a valid Python list of the most relevant passages (full text, not indexes), in order. "
                "Do NOT include any explanation, summary, or text before or after the list. "
                "The response MUST start with [ and end with ].\n\n"
                f"User Query: {query}\n\n"
                f"Passages:\n" + "\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(chunks)]) +
                "\n\nReturn ONLY the Python list."
            )
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.0
            )
            # Extract the Python list from the response
            import ast
            import re
            llm_output = response.choices[0].message.content.strip()
            # Try to extract a Python list from code block or raw text
            if '```' in llm_output:
                try:
                    llm_output = re.search(r'```(?:python)?(.*?)```', llm_output, re.DOTALL).group(1).strip()
                except Exception as e:
                    logger.error(f"Error extracting code block from LLM output: {e}\nLLM output was: {llm_output}")
                    return chunks
            try:
                match = re.search(r'\[.*?\]', llm_output, re.DOTALL)
                if match:
                    ranked_list = ast.literal_eval(match.group(0))
                    if not isinstance(ranked_list, list):
                        raise ValueError('LLM did not return a list')
                    if not all(isinstance(item, str) for item in ranked_list):
                        logger.warning(f"LLM reranker returned non-string items: {ranked_list}. Falling back to original order.")
                        return chunks
                    logger.info(f"LLM re-ranked chunks: {ranked_list}")
                    return ranked_list
                else:
                    logger.warning(f"LLM response did not contain a valid Python list. LLM output was: {llm_output!r}. Returning original order.")
                    return chunks
            except Exception as e:
                logger.error(f"Error in LLM re-ranking: {e}\nLLM output was: {llm_output}")
                return chunks
        except Exception as e:
            logger.error(f"Error in LLM rerank outer block: {e}")
            return chunks

# Global instance
agent = Agent()
