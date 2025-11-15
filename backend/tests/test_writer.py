# backend/tests/test_writer.py
import unittest
from unittest.mock import patch, MagicMock, mock_open

from backend.agents.writer_agent import write_article

class TestWriterAgent(unittest.TestCase):

    def setUp(self):
        self.spec = {
            "topic": "Binary Search in Python",
            "goal": "Explain the binary search algorithm",
            "audience": "Beginners",
            "word_count": 1000,
            "language": "Python",
            "selected_examples": ["Find element in sorted array"]
        }
        self.mock_article_content = """
# Binary Search Explained

## Introduction
This is an introduction.

## Concept Explanation
Here is the concept.

## Example Problems
```python
def binary_search(arr, x):
    pass
```

## Complexity Analysis
The complexity is...

## FAQ
- Q1? A1.
- Q2? A2.
- Q3? A3.

## Conclusion
In conclusion...
"""

    @patch('backend.agents.writer_agent.os.makedirs')
    @patch('backend.agents.writer_agent.open', new_callable=mock_open)
    @patch('backend.agents.writer_agent.OpenAI')
    def test_write_article_returns_string(self, MockOpenAI, mock_file, mock_makedirs):
        # Arrange
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mock_article_content
        mock_client.chat.completions.create.return_value = mock_response

        # Act
        result = write_article(self.spec)

        # Assert
        self.assertIsInstance(result, str)

    @patch('backend.agents.writer_agent.os.makedirs')
    @patch('backend.agents.writer_agent.open', new_callable=mock_open)
    @patch('backend.agents.writer_agent.OpenAI')
    def test_write_article_contains_h1_and_h2_headers(self, MockOpenAI, mock_file, mock_makedirs):
        # Arrange
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mock_article_content
        mock_client.chat.completions.create.return_value = mock_response

        # Act
        result = write_article(self.spec)

        # Assert
        self.assertIn("# ", result)
        self.assertGreaterEqual(result.count("## "), 2)

    @patch('backend.agents.writer_agent.os.makedirs')
    @patch('backend.agents.writer_agent.open', new_callable=mock_open)
    @patch('backend.agents.writer_agent.OpenAI')
    def test_write_article_contains_code_block(self, MockOpenAI, mock_file, mock_makedirs):
        # Arrange
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mock_article_content
        mock_client.chat.completions.create.return_value = mock_response

        # Act
        result = write_article(self.spec)

        # Assert
        self.assertIn("```python", result)
        self.assertIn("```", result)

    def test_write_article_raises_value_error_for_missing_keys(self):
        # Arrange
        incomplete_spec = {"topic": "Binary Search"}

        # Act & Assert
        with self.assertRaises(ValueError):
            write_article(incomplete_spec)

if __name__ == '__main__':
    unittest.main()
