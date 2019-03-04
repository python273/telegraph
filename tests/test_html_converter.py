from unittest import TestCase

from telegraph.exceptions import NotAllowedTag, InvalidHTML
from telegraph.utils import html_to_nodes, nodes_to_html, clear_whitespace_nodes

HTML_TEST_STR = """
<p>Hello, world!<br/></p>
<p><a href="https://telegra.ph/">Test link&lt;/a&gt;</a></p>
<figure>
<img src="/file/6c2ecfdfd6881d37913fa.png"/>
<figcaption></figcaption>
</figure>
""".replace('\n', '')

NODES_TEST_LIST = [
    {'tag': 'p', 'children': ['Hello, world!', {'tag': 'br'}]},
    {'tag': 'p', 'children': [{
        'tag': 'a',
        'attrs': {'href': 'https://telegra.ph/'},
        'children': ['Test link</a>']
        }]
     },
    {'tag': 'figure', 'children': [
        {'tag': 'img', 'attrs': {'src': '/file/6c2ecfdfd6881d37913fa.png'}},
        {'tag': 'figcaption'}
    ]}
]

HTML_MULTI_LINES = """
<p>
    <b>
        Hello,

    </b>
    world!
</p>
"""

HTML_MULTI_LINES1 = """<p><b>Hello, </b>world! </p>"""

HTML_MULTI_LINES_NODES_LIST = [
    {'tag': 'p', 'children': [
        {'tag': 'b', 'children': ['Hello, ']},
        'world! '
    ]},
]

HTML_NO_STARTTAG = "</a><h1></h1>"


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

    def test_html_to_nodes_multi_line(self):
        self.assertEqual(
            html_to_nodes(HTML_MULTI_LINES),
            HTML_MULTI_LINES_NODES_LIST
        )
        self.assertEqual(
            html_to_nodes(HTML_MULTI_LINES1),
            HTML_MULTI_LINES_NODES_LIST
        )

    def test_html_to_nodes_invalid_html(self):
        with self.assertRaises(InvalidHTML):
            html_to_nodes('<p><b></p></b>')

    def test_html_to_nodes_not_allowed_tag(self):
        with self.assertRaises(NotAllowedTag):
            html_to_nodes('<script src="localhost"></script>')

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

    def test_clear_whitespace_nodes(self):
        nodes = [
            '\n',
            {'tag': 'p', 'children': [
                {'tag': 'i', 'children': ['A']},
                {'tag': 'b', 'children': [' ']},
                {'tag': 'b', 'children': [
                    'B ',
                    {'tag': 'i', 'children': ['C']},
                    {'tag': 'i', 'children': [{'tag': 'b'}]},
                    ' D '
                ]},
                ' E '
            ]},
            {'tag': 'p', 'children': [' F ']},
            '\n'
        ]
        expected = [
            {'tag': 'p', 'children': [
                {'tag': 'i', 'children': ['A']},
                {'tag': 'b', 'children': [' ']},
                {'tag': 'b', 'children': [
                    'B ',
                    {'tag': 'i', 'children': ['C']},
                    {'tag': 'i', 'children': [{'tag': 'b'}]},
                    ' D '
                ]},
                'E '
            ]},
            {'tag': 'p', 'children': ['F ']}
        ]

        self.assertEqual(clear_whitespace_nodes(nodes)[0], expected)

    def test_no_starttag_node(self):
        with self.assertRaises(InvalidHTML):
             html_to_nodes(HTML_NO_STARTTAG)
