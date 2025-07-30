import openai
import os
from typing import List, Dict, Optional
from .qdrant_client import search_vectors
from .ingestion import embed_text
import logging
import logging.config

# Load logging configuration
LOGGING_CONF_PATH = os.path.join(os.path.dirname(__file__), '../../logging.conf')
if os.path.exists(LOGGING_CONF_PATH):
    logging.config.fileConfig(LOGGING_CONF_PATH, disable_existing_loggers=False)
logger = logging.getLogger('ai_manager')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

class AIService:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.max_context_length = 4000  # tokens

    def generate_response(self, user_message: str, conversation_history: List[str], user_id: int = None) -> str:
        """
        Generate AI response using agentic hybrid RAG orchestration.
        """
        try:
            from .agent import agent
            logger.info(f"Generating response for user_id={user_id} | user_message='{user_message}'")
            # 1. Classify intent
            intent = agent.classify_intent(user_message)
            logger.debug(f"Intent classified: {intent}")
            # 2. Retrieve context based on intent
            context_dict = agent.retrieve_context(user_message, user_id=user_id, intent=intent, top_k=3)
            logger.debug(f"Context retrieved: {context_dict}")
            # 3. Build prompt with clear source separation
            system_prompt = agent.build_prompt(context_dict, user_message)
            logger.debug(f"System prompt constructed: {system_prompt}")
            # 4. Build messages for OpenAI API
            messages = self._build_messages(system_prompt, conversation_history, user_message)
            logger.debug(f"Messages sent to LLM: {messages}")
            # 5. Generate response
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9
            )
            logger.info(f"LLM response received for user_id={user_id}")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.exception(f"Error generating AI response (agentic) for user_id={user_id} | user_message='{user_message}'")
            return self._get_fallback_response(user_message)

    
    def _retrieve_context(self, query: str, user_id: int = None) -> str:
        """
        Retrieve relevant context from both global and personal knowledgebases
        """
        try:
            # Get query embedding
            query_embedding = embed_text([query])[0]
            
            # Search global knowledgebase
            global_results = search_vectors(query_embedding, collection='global_kb', top=3)
            global_context = self._extract_context_from_results(global_results)
            
            # Search personal knowledgebase if user_id provided
            personal_context = ""
            if user_id:
                personal_results = search_vectors(query_embedding, collection='personal_kb', top=3)
                # Filter results for this user
                filtered_results = [r for r in personal_results.get('result', []) 
                                  if r['payload'].get('user_id') == user_id]
                personal_context = self._extract_context_from_results({'result': filtered_results})
            
            # Combine contexts
            combined_context = ""
            if global_context:
                combined_context += f"Global Knowledge:\n{global_context}\n\n"
            if personal_context:
                combined_context += f"Personal Knowledge:\n{personal_context}\n\n"
                
            return combined_context.strip()
            
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return ""
    
    def _extract_context_from_results(self, results: Dict) -> str:
        """Extract text content from search results"""
        try:
            context_parts = []
            for result in results.get('result', []):
                if 'payload' in result and 'chunk' in result['payload']:
                    context_parts.append(result['payload']['chunk'])
            return "\n".join(context_parts)
        except Exception as e:
            print(f"Error extracting context: {e}")
            return ""
    
    def _build_system_prompt(self, context: str) -> str:
        """Build the system prompt with context"""
        base_prompt = """
You are not a generic AI assistant. You are the user's dedicated personal manager for their music artist career. Your sole purpose is to help this specific artist with their career development, creative process, and business strategies. You must always:

- Act as a professional, supportive, and proactive personal manager for music artists.
- Use both global music industry knowledge and the artist's personal documents and information to provide advice.
- Never refer to yourself as an AI. Never give generic, vague, or impersonal answers.
- Always tailor your advice to the user's goals, context, and artist career. If you lack information, ask clarifying questions as a manager would.
- If you must rely on general knowledge, always relate it back to the music industry and the user's career.

Your role is to:
1. Provide informed, actionable advice based on music industry best practices
2. Help artists understand and leverage their personal data and documents
3. Offer strategic guidance for career development and business growth
4. Answer questions about music production, marketing, and business as a manager would
5. Be encouraging, supportive, and professional at all times

When responding:
- Use the provided context to give relevant, specific, and personalized advice
- If the context doesn't contain relevant information, relate your response to the user's music career and goals
- Be concise but thorough
- Focus on actionable, practical steps
- Maintain a professional, encouraging, and artist-focused tone
- Never act as a generic AI assistant. Reiterate your role as the user's personal manager for music artists if needed.

Available Context Information:
"""
        
        if context:
            return base_prompt + f"\n{context}\n\nUse this context to provide relevant, personalized advice."
        else:
            return base_prompt + "\nNo specific context available. Rely on your general knowledge of the music industry."
    
    def _build_messages(self, system_prompt: str, conversation_history: List[str], user_message: str) -> List[Dict]:
        """Build messages array for OpenAI API with dynamic context windowing and summarization."""
        import tiktoken
        encoding = tiktoken.encoding_for_model(self.model)
        max_tokens = self.max_context_length
        # Reserve tokens for system prompt and LLM output
        reserved_tokens = 1200  # 1000 for output, 200 for prompt overhead
        used_tokens = len(encoding.encode(system_prompt)) + len(encoding.encode(user_message))
        messages = [{"role": "system", "content": system_prompt}]

        # Estimate tokens for each conversation message
        history_tokens = [len(encoding.encode(m)) for m in conversation_history]
        cum_tokens = used_tokens
        selected = []
        # Add as many recent messages as possible without exceeding token budget
        for i in range(len(conversation_history)-1, -1, -1):
            if cum_tokens + history_tokens[i] + reserved_tokens > max_tokens:
                break
            selected.append((i, conversation_history[i]))
            cum_tokens += history_tokens[i]
        selected = sorted(selected)  # maintain chronological order

        # If not all history fits, summarize the omitted portion
        if len(selected) < len(conversation_history):
            omitted = conversation_history[:len(conversation_history)-len(selected)]
            summary = self._summarize_history(omitted)
            messages.append({"role": "user", "content": f"Summary of earlier conversation: {summary}"})

        # Add selected messages (alternating roles)
        for idx, message in selected:
            role = "user" if idx % 2 == 0 else "assistant"
            messages.append({"role": role, "content": message})

        # Add current user message
        messages.append({"role": "user", "content": user_message})
        return messages

    def _summarize_history(self, history: list) -> str:
        """Summarize omitted conversation history for context windowing."""
        if not history:
            return ""
        # Simple heuristic: join and truncate, or use LLM for summarization if available
        joined = " ".join(history)
        if len(joined) > 500:
            return joined[:500] + "..."
        return joined

    
    def _get_fallback_response(self, user_message: str) -> str:
        """Fallback response when AI generation fails"""
        return f"I apologize, but I'm having trouble processing your request right now. You said: '{user_message}'. Please try again in a moment, or feel free to ask a different question about your music career or creative process."

# Global instance
ai_service = AIService() 