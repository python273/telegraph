try:
    from html.parser import HTMLParser  # python 3.x
    from html.entities import name2codepoint
    from html import escape
except ImportError:
    chr = unichr

    from HTMLParser import HTMLParser  # python 2.x
    from htmlentitydefs import name2codepoint
    from cgi import escape

from .exceptions import NotAllowedTag, InvalidHTML


ALLOWED_TAGS = [
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure',
    'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's',
    'strong', 'u', 'ul', 'video'
]


class HtmlToNodesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.nodes = []

        self.current_node_list = self.nodes
        self.parent_node_lists = []

    def handle_starttag(self, tag, attrs_list):
        if tag not in ALLOWED_TAGS:
            raise NotAllowedTag('%s tag is not allowed', tag)

        node = {'tag': tag, 'children': []}

        if attrs_list:
            attrs = {}

            for attr, value in attrs_list:
                attrs[attr] = value

            node['attrs'] = attrs

        self.current_node_list.append(node)
        self.parent_node_lists.append(self.current_node_list)

        self.current_node_list = node['children']

    def handle_endtag(self, tag):
        self.current_node_list = self.parent_node_lists.pop(-1)

        if self.current_node_list[-1]['tag'] != tag:
            raise InvalidHTML

    def handle_data(self, data):
        self.current_node_list.append(data)

    def handle_entityref(self, name):
        self.current_node_list.append(chr(name2codepoint[name]))

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))

        self.current_node_list.append(c)


def html_to_nodes(html_content):
    parser = HtmlToNodesParser()
    parser.feed(html_content)

    return parser.nodes


def nodes_to_html(nodes):
    html_content = []

    stack = []
    tags_stack = []
    current_nodes = nodes

    while True:
        if current_nodes:
            node = current_nodes.pop(0)

            if type(node) is dict:
                tags_stack.append(node['tag'])

                attrs = node.get('attrs')

                if attrs:
                    attrs_str = ['']

                    for attr, value in attrs.items():
                        attrs_str.append('{}="{}"'.format(attr, value))
                else:
                    attrs_str = []

                html_content.append('<{}{}>'.format(
                    node['tag'],
                    ' '.join(attrs_str)
                ))

                children = node.get('children')

                if children:
                    stack.append(current_nodes)
                    current_nodes = children
            else:
                html_content.append(escape(node))

        if not current_nodes:
            if tags_stack:
                html_content.append('</{}>'.format(tags_stack.pop(-1)))

            if stack:
                current_nodes = stack.pop(-1)
            else:
                break

    return ''.join(html_content)
