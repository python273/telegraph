from unittest import TestCase, skip

from telegraph import Telegraph


POST_HTML_CONTENT = """<p><a href="https://github.com/python273/telegraph">
Python Telegraph API Wrapper</a></p>
""".replace('\n', '')


class TestTelegraph(TestCase):
    @skip('unstable page creation, PAGE_SAVE_FAILED')
    def test_flow(self):
        telegraph = Telegraph()

        response = telegraph.create_account(
            short_name='python telegraph',
            author_name='Python Telegraph API wrapper',
            author_url='https://github.com/python273/telegraph'
        )
        self.assertTrue('access_token' in response)
        self.assertTrue('auth_url' in response)

        response = telegraph.get_account_info()
        self.assertEqual(response['short_name'], 'python telegraph')

        response = telegraph.edit_account_info(
            short_name='Python Telegraph Wrapper'
        )
        self.assertEqual(response['short_name'], 'Python Telegraph Wrapper')

        response = telegraph.create_page(
            'Python Telegraph API wrapper',
            html_content='<p>Hello, world!</p>'
        )

        telegraph.edit_page(
            response['path'],
            'Python Telegraph API Wrapper',
            html_content=POST_HTML_CONTENT
        )

        response = telegraph.get_views(response['path'])
        self.assertTrue('views' in response)

        response = telegraph.get_page_list()
        self.assertTrue(response['total_count'] > 0)

        response = telegraph.revoke_access_token()
        self.assertTrue('access_token' in response)
        self.assertTrue('auth_url' in response)

    def test_get_page_html(self):
        telegraph = Telegraph()
        response = telegraph.get_page('Hey-01-17-2')

        self.assertEqual(response['content'], '<p>Hello, world!</p>')

    def test_get_page(self):
        telegraph = Telegraph()
        response = telegraph.get_page('Hey-01-17-2', return_html=False)

        self.assertEqual(
            response['content'],
            [{'tag': 'p', 'children': ['Hello, world!']}]
        )

    def test_get_page_without_content(self):
        telegraph = Telegraph()
        response = telegraph.get_page('Hey-01-17-2', return_content=False)

        self.assertTrue('content' not in response)
