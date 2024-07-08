```markdown
# HTML to Quill Delta

This library converts HTML content to Quill Delta format. It is useful for integrating rich text content from HTML into applications that use the Quill editor.

## Installation

To install the library, use pip:

```bash
pip install html_to_quill_delta
```

## Usage

To convert HTML to Quill Delta, import the library and use the `html_to_delta` function:

```python
from html_to_quill_delta import html_to_delta

html = '''
<h1 style="color:red;font-size:24px;">Header 1</h1>
<p>This is a <strong>bold</strong> paragraph with a <a href="https://example.com">link</a>.</p>
'''

delta = html_to_delta(html)
print(delta)
```

## Features

- Converts HTML headings, paragraphs, links, lists, tables, and other common elements to Quill Delta format.
- Preserves inline styles such as bold, italic, underline, and color.
- Supports nested lists and tables.

## Examples

### Converting a Simple Paragraph

```python
html = '<p>Hello, <strong>world</strong>!</p>'
delta = html_to_delta(html)
print(delta)
```

### Converting a Complex HTML Structure

```python
html = '''
<h1>Title</h1>
<p>This is a paragraph with <em>emphasis</em> and <strong>strong text</strong>.</p>
<ul>
  <li>List item 1</li>
  <li>List item 2</li>
</ul>
'''

delta = html_to_delta(html)
print(delta)
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License.
```

## Acknowledgements

Special thanks to all contributors and the open-source community for their support and collaboration.
