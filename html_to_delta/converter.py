from bs4 import BeautifulSoup, NavigableString, Tag
import json

class CustomDelta:
    def __init__(self):
        self.ops = []

    def insert(self, text, attributes=None):
        if attributes:
            self.ops.append({'insert': text, 'attributes': attributes})
        else:
            self.ops.append({'insert': text})

    def to_dict(self):
        return {'ops': self.ops}

def parse_element(element, delta, inherited_attributes=None):
    if inherited_attributes is None:
        inherited_attributes = {}
    
    try:
        if isinstance(element, NavigableString):
            delta.insert(str(element), inherited_attributes)
        elif isinstance(element, Tag):
            # Handle class-based indentation in any tag
            attributes = inherited_attributes.copy()
            class_list = element.get('class', [])
            for class_name in class_list:
                if class_name.startswith('ql-indent-'):
                    indent_level = int(class_name.split('ql-indent-')[1])
                    attributes['indent'] = indent_level
            
            if element.name == 'p':
                parse_children(element, delta, attributes)
                delta.insert('\n', {**attributes, 'block': 'paragraph'})
            elif element.name in ['strong', 'b']:
                parse_children(element, delta, {**attributes, 'bold': True})
            elif element.name == 'em':
                parse_children(element, delta, {**attributes, 'italic': True})
            elif element.name == 'u':
                parse_children(element, delta, {**attributes, 'underline': True})
            elif element.name == 'a':
                href = element.get('href', '')
                parse_children(element, delta, {**attributes, 'link': href})
            elif element.name == 'h1':
                parse_children(element, delta, attributes)
                delta.insert('\n', {'header': 1})
            elif element.name == 'h2':
                parse_children(element, delta, attributes)
                delta.insert('\n', {'header': 2})
            elif element.name == 'h3':
                parse_children(element, delta, attributes)
                delta.insert('\n', {'header': 3})
            elif element.name == 'ol':
                parse_children(element, delta)
                delta.insert('\n', {'list': 'ordered'})
            elif element.name == 'ul':
                parse_children(element, delta)
                delta.insert('\n', {'list': 'bullet'})
            elif element.name == 'li':
                parse_children(element, delta, attributes)
                delta.insert('\n', {'list-item': True})
            elif element.name == 'br':
                delta.insert('\n')
            elif element.name == 'img':
                src = element.get('src', '')
                delta.insert({'image': src}, attributes)
            elif element.name == 'iframe':
                src = element.get('src', '')
                delta.insert({'iframe': src}, attributes)
            elif element.name == 'table':
                parse_table(element, delta, attributes)
            elif element.name == 'blockquote':
                parse_children(element, delta, attributes)
                delta.insert('\n', {'blockquote': True})
            elif element.name == 'div':
                parse_children(element, delta, attributes)
            elif element.name == 'span':
                parse_children(element, delta, attributes)
            elif element.name == 'code':
                parse_children(element, delta, {**attributes, 'code': True})
            elif element.name == 'pre':
                parse_children(element, delta, {**attributes, 'code-block': True})
            elif element.name == 'sup':
                parse_children(element, delta, {**attributes, 'script': 'super'})
            elif element.name == 'sub':
                parse_children(element, delta, {**attributes, 'script': 'sub'})
            else:
                parse_children(element, delta, attributes)
    except Exception as e:
        print(f"Error parsing element: {e}")

def parse_children(element, delta, attributes=None):
    try:
        for child in element.children:
            parse_element(child, delta, attributes)
    except Exception as e:
        print(f"Error parsing children: {e}")

def parse_table(table, delta, attributes=None):
    try:
        table_content = []
        for row in table.find_all('tr'):
            row_content = []
            for cell in row.find_all(['td', 'th']):
                cell_text = ''.join(cell.stripped_strings)
                row_content.append(cell_text)
            table_content.append(row_content)
        delta.insert({'table': table_content}, attributes)
    except Exception as e:
        print(f"Error parsing table: {e}")

def html_to_delta(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check if body tag is present, otherwise wrap content in a div
        if not soup.body:
            body = soup.new_tag('body')
            soup.insert(0, body)
            body.append(BeautifulSoup(html, 'html.parser'))
        
        delta = CustomDelta()
        for element in soup.body.children:
            parse_element(element, delta)
        return json.dumps(delta.to_dict(), indent=2)
    except Exception as e:
        print(f"Error converting HTML to Delta: {e}")

# Example usage:
html_content = """
<p>This is <strong>bold</strong>, <em>italic</em>, and <u>underlined</u> text.</p>
"""

delta_format = html_to_delta(html_content)
print(delta_format)
