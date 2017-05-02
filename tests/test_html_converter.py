import sys
from unittest import TestCase

from telegraph.exceptions import NotAllowedTag, InvalidHTML
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

NODES_TEST_LIST_PY35 = [
    {'tag': 'p', 'children': ['Hello, world!']},
    {'tag': 'p', 'children': [{
        'tag': 'a',
        'attrs': {'href': 'https://telegra.ph/'},
        'children': ['Test link</a>']
        }]
     }
]


class TestHTMLConverter(TestCase):
    def test_html_to_nodes(self):

        if sys.version_info.major == 3 and sys.version_info.minor >= 5:
            self.assertEqual(
                html_to_nodes(HTML_TEST_STR),
                NODES_TEST_LIST_PY35
            )
        else:
            self.assertEqual(
                html_to_nodes(HTML_TEST_STR),
                NODES_TEST_LIST
            )

    def test_html_to_nodes_invalid_html(self):
        with self.assertRaises(InvalidHTML):
            html_to_nodes('<p><b></p></b>')

    def test_html_to_nodes_not_allowed_tag(self):
        with self.assertRaises(NotAllowedTag):
            html_to_nodes('<script src="localhost"></script>')

    def test_nodes_to_html(self):
        self.assertEqual(
            nodes_to_html(NODES_TEST_LIST),
            HTML_TEST_STR
        )

    def test_nodes_to_html_nested(self):
        self.assertEqual(
            nodes_to_html([
                {'tag': 'a', 'children': [
                    {'tag': 'b', 'children': [
                        {'tag': 'c', 'children': [
                            {'tag': 'd', 'children': []}
                        ]}
                    ]}
                ]}
            ]),
            '<a><b><c><d></d></c></b></a>'
        )

    def test_nodes_to_html_blank(self):
        self.assertEqual(
            nodes_to_html([]),
            ''
        )
