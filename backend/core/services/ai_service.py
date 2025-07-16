import openai
import os
from typing import List, Dict, Optional
from .qdrant_client import search_vectors
from .ingestion import embed_text

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

class AIService:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.max_context_length = 4000  # tokens
        
    def generate_response(self, user_message: str, conversation_history: List[str], user_id: int = None) -> str:
        """
        Generate AI response using RAG (Retrieval-Augmented Generation)
        
        Args:
            user_message: Current user message
            conversation_history: List of previous messages for context
            user_id: User ID for personal knowledgebase search
            
        Returns:
            AI generated response
        """
        try:
            # Step 1: Retrieve relevant context from knowledgebases
            relevant_context = self._retrieve_context(user_message, user_id)
            
            # Step 2: Build the prompt with context and conversation history
            system_prompt = self._build_system_prompt(relevant_context)
            
            # Step 3: Create messages for OpenAI API
            messages = self._build_messages(system_prompt, conversation_history, user_message)
            
            # Step 4: Generate response
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
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
        base_prompt = """You are an AI assistant specifically designed to help music artists with their career development, creative process, and business strategies. You have access to both global music industry knowledge and the artist's personal documents and information.

Your role is to:
1. Provide informed advice based on music industry best practices
2. Help artists understand their personal data and documents
3. Offer strategic guidance for career development
4. Answer questions about music production, marketing, and business
5. Be encouraging and supportive while remaining professional

When responding:
- Use the provided context to give relevant, specific advice
- If the context doesn't contain relevant information, rely on your general knowledge
- Be concise but thorough
- Focus on actionable advice
- Maintain a professional yet encouraging tone

Available Context Information:
"""
        
        if context:
            return base_prompt + f"\n{context}\n\nUse this context to provide relevant, personalized advice."
        else:
            return base_prompt + "\nNo specific context available. Rely on your general knowledge of the music industry."
    
    def _build_messages(self, system_prompt: str, conversation_history: List[str], user_message: str) -> List[Dict]:
        """Build messages array for OpenAI API"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (alternating user/assistant)
        for i, message in enumerate(conversation_history[-6:]):  # Keep last 6 messages for context
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": message})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Fallback response when AI generation fails"""
        return f"I apologize, but I'm having trouble processing your request right now. You said: '{user_message}'. Please try again in a moment, or feel free to ask a different question about your music career or creative process."

# Global instance
ai_service = AIService() 