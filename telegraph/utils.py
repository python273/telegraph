# -*- coding: utf-8 -*-
import re
from html.parser import HTMLParser
from html.entities import name2codepoint
from html import escape

from .exceptions import NotAllowedTag, InvalidHTML


RE_WHITESPACE = re.compile(r'(\s+)', re.UNICODE)


ALLOWED_TAGS = {
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure',
    'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's',
    'strong', 'u', 'ul', 'video'
}

VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen',
    'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr'
}

BLOCK_ELEMENTS = {
    'address', 'article', 'aside', 'blockquote', 'canvas', 'dd', 'div', 'dl',
    'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'li', 'main', 'nav',
    'noscript', 'ol', 'output', 'p', 'pre', 'section', 'table', 'tfoot', 'ul',
    'video'
}


class HtmlToNodesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.nodes = []

        self.current_nodes = self.nodes
        self.parent_nodes = []

        self.last_text_node = None

        self.tags_path = []

    def add_str_node(self, s):
        if not s:
            return

        if 'pre' not in self.tags_path:  # keep whitespace in <pre>
            s = RE_WHITESPACE.sub(' ', s)

            if self.last_text_node is None or self.last_text_node.endswith(' '):
                s = s.lstrip(' ')

            if not s:
                self.last_text_node = None
                return

            self.last_text_node = s

        if self.current_nodes and isinstance(self.current_nodes[-1], str):
            self.current_nodes[-1] += s
        else:
            self.current_nodes.append(s)

    def handle_starttag(self, tag, attrs_list):
        if tag not in ALLOWED_TAGS:
            raise NotAllowedTag(f'{tag!r} tag is not allowed')

        if tag in BLOCK_ELEMENTS:
            self.last_text_node = None

        node = {'tag': tag}
        self.tags_path.append(tag)
        self.current_nodes.append(node)

        if attrs_list:
            attrs = {}
            node['attrs'] = attrs

            for attr, value in attrs_list:
                attrs[attr] = value

        if tag not in VOID_ELEMENTS:
            self.parent_nodes.append(self.current_nodes)
            self.current_nodes = node['children'] = []

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            return

        if not len(self.parent_nodes):
            raise InvalidHTML(f'{tag!r} missing start tag')

        self.current_nodes = self.parent_nodes.pop()

        last_node = self.current_nodes[-1]

        if last_node['tag'] != tag:
            raise InvalidHTML(f'{tag!r} tag closed instead of {last_node["tag"]!r}')

        self.tags_path.pop()

        if not last_node['children']:
            last_node.pop('children')

    def handle_data(self, data):
        self.add_str_node(data)

    def handle_entityref(self, name):
        self.add_str_node(chr(name2codepoint[name]))

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))

        self.add_str_node(c)

    def get_nodes(self):
        if self.parent_nodes:
            not_closed_tag = self.parent_nodes[-1][-1]['tag']
            raise InvalidHTML(f'{not_closed_tag!r} tag is not closed')

        return self.nodes


def html_to_nodes(html_content):
    parser = HtmlToNodesParser()
    parser.feed(html_content)
    return parser.get_nodes()


def nodes_to_html(nodes):
    out = []
    append = out.append

    stack = []
    curr = nodes
    i = -1

    while True:
        i += 1

        if i >= len(curr):
            if not stack:
                break
            curr, i = stack.pop()
            append(f'</{curr[i]["tag"]}>')
            continue

        node = curr[i]

        if isinstance(node, str):
            append(escape(node))
            continue

        append(f'<{node["tag"]}')

        if node.get('attrs'):
            for attr, value in node['attrs'].items():
                append(f' {attr}="{escape(value)}"')

        if node.get('children'):
            append('>')
            stack.append((curr, i))
            curr, i = node['children'], -1
            continue

        if node["tag"] in VOID_ELEMENTS:
            append('/>')
        else:
            append(f'></{node["tag"]}>')

    return ''.join(out)
