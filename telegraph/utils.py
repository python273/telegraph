# -*- coding: utf-8 -*-
import re

from .exceptions import NotAllowedTag, InvalidHTML

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

    def add_str_node(self, s):
        if not s:
            return

        if self.current_nodes and isinstance(self.current_nodes[-1], basestring):
            self.current_nodes[-1] += s
        else:
            self.current_nodes.append(s)

    def handle_starttag(self, tag, attrs_list):
        if tag not in ALLOWED_TAGS:
            raise NotAllowedTag('%s tag is not allowed' % tag)

        node = {'tag': tag}

        if attrs_list:
            attrs = {}

            for attr, value in attrs_list:
                attrs[attr] = value

            node['attrs'] = attrs

        self.current_nodes.append(node)

        if tag not in VOID_ELEMENTS:
            self.parent_nodes.append(self.current_nodes)
            self.current_nodes = node['children'] = []

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            return

        if not len(self.parent_nodes):
            raise InvalidHTML('"{}" missing start tag'.format(
                tag
            ))

        self.current_nodes = self.parent_nodes.pop()

        last_node = self.current_nodes[-1]

        if last_node['tag'] != tag:
            raise InvalidHTML('"{}" tag closed instead of "{}"'.format(
                tag, last_node['tag']
            ))

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
            raise InvalidHTML('"{}" tag is not closed'.format(not_closed_tag))

        return self.nodes


def clear_whitespace_nodes(nodes, last_text_node=None):
    """

    :param nodes:
    :type nodes: list
    :param last_text_node:
    :type last_text_node: basestring
    :return: list
    """
    # TODO: probably possible to move to html parser

    stack = []
    current_nodes = nodes[:]

    new_nodes = []
    new_children = new_nodes

    while True:
        if current_nodes:
            node = current_nodes.pop(0)

            if type(node) is dict:
                is_block_element = node['tag'] in BLOCK_ELEMENTS
                if is_block_element:
                    last_text_node = None

                new_children.append(node)

                node_children = node.get('children')

                if node_children:
                    stack.append((current_nodes, new_children))
                    current_nodes = node_children
                    new_children = []
                    node['children'] = new_children
            else:
                node = RE_WHITESPACE.sub(' ', node)

                if last_text_node is None or last_text_node.endswith(' '):
                    node = node.lstrip(' ')

                if node:
                    last_text_node = node
                    new_children.append(node)
                else:
                    last_text_node = None

        if not current_nodes:
            if stack:
                current_nodes, new_children = stack.pop()
            else:
                break

    return new_nodes, last_text_node


def html_to_nodes(html_content):
    parser = HtmlToNodesParser()
    parser.feed(html_content)

    nodes = parser.get_nodes()
    nodes, _ = clear_whitespace_nodes(nodes)
    return nodes


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
