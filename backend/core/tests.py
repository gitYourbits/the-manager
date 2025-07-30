from django.test import TestCase
from unittest.mock import patch
from core.services.agent import agent

class AgenticRAGTests(TestCase):
    def test_intent_classification_keyword(self):
        self.assertEqual(agent.classify_intent("What should I do next week?"), "personal")
        self.assertEqual(agent.classify_intent("What are the latest industry trends?"), "global")
        self.assertEqual(agent.classify_intent("Given my uploads and industry, what’s best?"), "hybrid")
        self.assertEqual(agent.classify_intent("How do I succeed?"), "hybrid")

    @patch('core.services.agent.agent.llm_rerank')
    def test_retrieve_context_includes_global(self, mock_rerank):
        # Mock embedding and search_vectors for deterministic output
        with patch('core.services.agent.embed_text', return_value=[[0.1]*384]), \
             patch('core.services.agent.search_vectors') as mock_search:
            # Simulate Qdrant returning chunks
            mock_search.side_effect = [
                {'result': [{'payload': {'chunk': 'Industry advice 1'}}, {'payload': {'chunk': 'Industry advice 2'}}]},
                {'result': [{'payload': {'chunk': 'My show 1', 'user_id': 1}}, {'payload': {'chunk': 'My show 2', 'user_id': 1}}]}
            ]
            mock_rerank.side_effect = lambda query, chunks: list(reversed(chunks))
            context = agent.retrieve_context("What should I do next week?", user_id=1, intent="personal", use_llm_rerank=True)
            self.assertIn("global", context)
            self.assertIn("personal", context)
            self.assertEqual(context["global"], ['Industry advice 2', 'Industry advice 1'])
            self.assertEqual(context["personal"], ['My show 2', 'My show 1'])

    def test_prompt_construction(self):
        context = {
            "personal": ["You played at Venue X."],
            "global": ["Artists benefit from social media."]
        }
        prompt = agent.build_prompt(context, "What should I focus on?")
        self.assertIn("Personal Knowledge", prompt)
        self.assertIn("Global Knowledge", prompt)
        self.assertIn("What should I focus on?", prompt)

    # Add more tests for chatbot memory/follow-up as needed
