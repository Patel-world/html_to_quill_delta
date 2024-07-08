import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from html_to_delta import html_to_delta

class TestHtmlToDelta(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        pass
    
    def test_plain_text(self):
        html_content = "<p>This is plain text.</p>"
        expected_output = {
            "ops": [
                {"insert": "This is plain text."},
                {"insert": "\n", "attributes": {"block": "paragraph"}}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)
    
    def test_bold_text(self):
        html_content = "<p>This is <strong>bold</strong> text.</p>"
        expected_output = {
            "ops": [
                {"insert": "This is "},
                {"insert": "bold", "attributes": {"bold": True}},
                {"insert": " text."},
                {"insert": "\n", "attributes": {"block": "paragraph"}}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)
    
    def test_link_text(self):
        html_content = '<p>This is a <a href="https://example.com">link</a>.</p>'
        expected_output = {
            "ops": [
                {"insert": "This is a "},
                {"insert": "link", "attributes": {"link": "https://example.com"}},
                {"insert": "."},
                {"insert": "\n", "attributes": {"block": "paragraph"}}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)
    
    def test_blockquote(self):
        html_content = "<blockquote>This is a blockquote.</blockquote>"
        expected_output = {
            "ops": [
                {"insert": "This is a blockquote."},
                {"insert": "\n", "attributes": {"blockquote": True}}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)
    
    def test_table(self):
        html_content = """
        <table>
            <tr><th>Header 1</th><th>Header 2</th></tr>
            <tr><td>Row 1, Cell 1</td><td>Row 1, Cell 2</td></tr>
            <tr><td>Row 2, Cell 1</td><td>Row 2, Cell 2</td></tr>
        </table>
        """
        expected_output = {
            "ops": [
                {"insert": "\n"},
                {"insert": {"table": [
                    ["Header 1", "Header 2"],
                    ["Row 1, Cell 1", "Row 1, Cell 2"],
                    ["Row 2, Cell 1", "Row 2, Cell 2"]
                ]}},
                {"insert": "\n"}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)
    
    def test_div(self):
        html_content = """
        <div>This is a div.</div>
        """
        expected_output = {
            "ops": [
                {"insert": "\n"},
                {"insert": "This is a div."},
                {"insert": "\n"}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)

    
    def test_image(self):
        html_content = '<p>This is an <img src="https://example.com/image.jpg"> image.</p>'
        expected_output = {
            "ops": [
                {"insert": "This is an "},
                {"insert": {"image": "https://example.com/image.jpg"}},
                {"insert": " image."},
                {"insert": "\n", "attributes": {"block": "paragraph"}}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)
    
    def test_nested_elements(self):
        html_content = """
        <p>This is a <strong>bold <em>and italic</em></strong> text.</p>
        """
        expected_output = {
            "ops": [
                {"insert": "\n"},
                {"insert": "This is a "},
                {"insert": "bold ", "attributes": {"bold": True}},
                {"insert": "and italic", "attributes": {"bold": True, "italic": True}},
                {"insert": " text."},
                {"insert": "\n", "attributes": {"block": "paragraph"}},
                {"insert": "\n"}
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)
    
    def tearDown(self):
        pass

    def test_combined_formatting(self):
        html_content = """<p>This is <strong>bold</strong>, <em>italic</em>, and <u>underlined</u> text.</p>"""
        expected_output = {
            "ops": [
                
                {
                    "insert": "This is "
                },
                {
                    "insert": "bold",
                    "attributes": {
                        "bold": True
                    }
                },
                {
                    "insert": ", "
                },
                {
                    "insert": "italic",
                    "attributes": {
                        "italic": True
                    }
                },
                {
                    "insert": ", and "
                },
                {
                    "insert": "underlined",
                    "attributes": {
                        "underline": True
                    }
                },
                {
                    "insert": " text."
                },
                {
                    "insert": "\n",
                    "attributes": {
                        "block": "paragraph"
                    }
                },
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)

    
    def test_indentation(self):
        html_content = """
        <p class="ql-indent-2">This is indented text.</p>
        """
        expected_output = {
            "ops": [
                {"insert": "\n"},
                {"insert": "This is indented text.", "attributes": {"indent": 2}},
                {"insert": "\n", "attributes": {"indent": 2, "block": "paragraph"}},
                {"insert": "\n"},
            ]
        }
        result = html_to_delta(html_content)
        self.assertEqual(json.loads(result), expected_output)

if __name__ == '__main__':
    unittest.main()
