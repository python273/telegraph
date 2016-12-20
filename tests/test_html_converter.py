from unittest import TestCase

from telegraph.utils import html_to_nodes, nodes_to_html


HTML_TEST_STR = """
<p>Hello, world!</p>
<p><a href="https://telegra.ph/">Test link&lt;/a&gt;</a></p>
""".replace('\n', '')

NODES_TEST_LIST = [
    {'tag': 'p', 'children': ['Hello, world!']},
    {'tag': 'p', 'children': [{
        'tag': 'a',
        'attrs': {'href': 'https://telegra.ph/'},
        'children': ['Test link', '<', '/a', '>']
        }]
     }
]


class TestHTMLConverter(TestCase):
    def test_html_to_nodes(self):

        self.assertEqual(
            html_to_nodes(HTML_TEST_STR),
            NODES_TEST_LIST
        )

    def test_nodes_to_html(self):
        self.assertEqual(
            nodes_to_html(NODES_TEST_LIST),
            HTML_TEST_STR
        )

    def test_nodes_to_html_blank(self):
        self.assertEqual(
            nodes_to_html([]),
            ''
        )
