# -*- coding: utf-8 -*-

try:  # python 3.x
    from html.parser import HTMLParser
    from html.entities import name2codepoint
    from html import escape

    basestring = str

except ImportError:  # python 2.x
    from HTMLParser import HTMLParser
    from htmlentitydefs import name2codepoint
    from cgi import escape

    chr = unichr

from .exceptions import NotAllowedTag, InvalidHTML


ALLOWED_TAGS = [
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure',
    'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's',
    'strong', 'u', 'ul', 'video'
]

VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen',
    'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr'
}


class HtmlToNodesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.nodes = []

        self.current_nodes = self.nodes
        self.parent_nodes = []

    def add_str_node(self, s):
        if not s:
            return

        if self.current_nodes and isinstance(self.current_nodes[-1], basestring):
            self.current_nodes[-1] += s
        else:
            self.current_nodes.append(s)

    def handle_starttag(self, tag, attrs_list):
        if tag not in ALLOWED_TAGS:
            raise NotAllowedTag('%s tag is not allowed', tag)

        node = {'tag': tag, 'children': []}

        if attrs_list:
            attrs = {}

            for attr, value in attrs_list:
                attrs[attr] = value

            node['attrs'] = attrs

        self.current_nodes.append(node)
        self.parent_nodes.append(self.current_nodes)

        self.current_nodes = node['children']

    def handle_endtag(self, tag):
        self.current_nodes = self.parent_nodes.pop()

        last_node = self.current_nodes[-1]

        if last_node['tag'] != tag:
            raise InvalidHTML

        if not last_node['children']:
            last_node.pop('children')

    def handle_data(self, data):
        self.add_str_node(data.strip())

    def handle_entityref(self, name):
        self.add_str_node(chr(name2codepoint[name]))

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))

        self.add_str_node(c)


def html_to_nodes(html_content):
    parser = HtmlToNodesParser()
    parser.feed(html_content)

    return parser.nodes


def nodes_to_html(nodes):
    html_content = []

    stack = []
    tags_stack = []
    current_nodes = nodes[:]

    while True:
        if current_nodes:
            node = current_nodes.pop(0)

            if type(node) is dict:
                tags_stack.append(node['tag'])

                attrs = node.get('attrs')

                if attrs:
                    attrs_str = ['']

                    for attr, value in attrs.items():
                        attrs_str.append('{}="{}"'.format(attr, escape(value)))
                else:
                    attrs_str = []

                html_content.append('<{}{}>'.format(
                    node['tag'],
                    ' '.join(attrs_str)
                ))

                children = node.get('children', [])
                stack.append(current_nodes)
                current_nodes = children
            else:
                html_content.append(escape(node))

        if not current_nodes:
            if tags_stack:
                closed_tag = tags_stack.pop()

                last_el = html_content[-1]

                if closed_tag in VOID_ELEMENTS and \
                   last_el.startswith('<{}'.format(closed_tag)) and \
                   not last_el.endswith('/>'):

                    html_content[-1] = last_el[:-1] + '/>'
                else:
                    html_content.append('</{}>'.format(closed_tag))

            if stack:
                current_nodes = stack.pop()
            else:
                break

    return ''.join(html_content)
