# backend/tests/test_clarifier.py
import unittest
from unittest.mock import patch, MagicMock
import json
import pytest

from backend.agents.clarifier import clarify

class TestClarifierAgent(unittest.TestCase):

    def setUp(self):
        self.job_json = {
            "topic": "Recursion in Python",
            "level": "Beginner",
            "language": "Python",
            "examples": ["Factorial", "Fibonacci sequence"]
        }
        self.mock_response_content = {
            "audience": "Beginner DSA learners",
            "goal": "Explain the concept of recursion clearly",
            "word_count": 1200,
            "selected_examples": ["Factorial calculation", "Fibonacci sequence generation"],
            "angles": ["Explaining the call stack", "Visualizing recursion with diagrams"]
        }

    @patch('backend.agents.clarifier.OpenAI')
    def test_clarify_returns_dict(self, MockOpenAI):
        # Arrange
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps(self.mock_response_content)
        mock_client.chat.completions.create.return_value = mock_response

        # Act
        result = clarify(self.job_json)

        # Assert
        self.assertIsInstance(result, dict)

    @patch('backend.agents.clarifier.OpenAI')
    def test_clarify_returns_expected_keys(self, MockOpenAI):
        # Arrange
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps(self.mock_response_content)
        mock_client.chat.completions.create.return_value = mock_response

        # Act
        result = clarify(self.job_json)

        # Assert
        expected_keys = ["audience", "goal", "word_count", "selected_examples", "angles"]
        for key in expected_keys:
            self.assertIn(key, result)

    def test_clarify_raises_value_error_for_missing_keys(self):
        # Arrange
        incomplete_job_json = {"topic": "Recursion"}

        # Act & Assert
        with self.assertRaises(ValueError):
            clarify(incomplete_job_json)

    @patch('backend.agents.clarifier.OpenAI')
    def test_clarify_handles_invalid_json_response(self, MockOpenAI):
        # Arrange
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is not valid JSON"
        mock_client.chat.completions.create.return_value = mock_response

        # Act & Assert
        with self.assertRaises(json.JSONDecodeError):
            clarify(self.job_json)

if __name__ == '__main__':
    unittest.main()
