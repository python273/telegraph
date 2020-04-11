# -*- coding: utf-8 -*-
import json

import requests

from .exceptions import TelegraphException
from .utils import html_to_nodes, nodes_to_html


class TelegraphApi(object):
    """ Telegraph API Client

    :param access_token: access_token
    :type access_token: str
    """

    __slots__ = ('access_token', 'session')

    def __init__(self, access_token=None):
        self.access_token = access_token
        self.session = requests.Session()

    def method(self, method, values=None, path=''):
        values = values.copy() if values is not None else {}

        if 'access_token' not in values and self.access_token:
            values['access_token'] = self.access_token

        response = self.session.post(
            'https://api.telegra.ph/{}/{}'.format(method, path),
            values
        ).json()

        if response.get('ok'):
            return response['result']

        raise TelegraphException(response.get('error'))


class Telegraph(object):
    """ Telegraph API client helper

    :param access_token: Telegraph access token
    """

    __slots__ = ('_telegraph',)

    def __init__(self, access_token=None):
        self._telegraph = TelegraphApi(access_token)

    def get_access_token(self):
        """ Return current access_token
        """

        return self._telegraph.access_token

    def create_account(self, short_name, author_name=None, author_url=None,
                       replace_token=True):
        """ Create a new Telegraph account

        :param short_name: Account name, helps users with several
                           accounts remember which they are currently using.
                           Displayed to the user above the "Edit/Publish"
                           button on Telegra.ph, other users don't see this name

        :param author_name: Default author name used when creating new articles

        :param author_url: Default profile link, opened when users click on the
                           author's name below the title. Can be any link,
                           not necessarily to a Telegram profile or channels

        :param replace_token: Replaces current token to a new user's token
        """

        response = self._telegraph.method('createAccount', values={
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        })

        if replace_token:
            self._telegraph.access_token = response.get('access_token')

        return response

    def edit_account_info(self, short_name=None, author_name=None,
                          author_url=None):
        """ Update information about a Telegraph account.
            Pass only the parameters that you want to edit

        :param short_name: Account name, helps users with several
                           accounts remember which they are currently using.
                           Displayed to the user above the "Edit/Publish"
                           button on Telegra.ph, other users don't see this name

        :param author_name: Default author name used when creating new articles

        :param author_url: Default profile link, opened when users click on the
                           author's name below the title. Can be any link,
                           not necessarily to a Telegram profile or channels
        """

        return self._telegraph.method('editAccountInfo', values={
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        })

    def revoke_access_token(self):
        """ Revoke access_token and generate a new one, for example,
            if the user would like to reset all connected sessions, or
            you have reasons to believe the token was compromised.
            On success, returns dict with new access_token and auth_url fields
        """

        response = self._telegraph.method('revokeAccessToken')

        self._telegraph.access_token = response.get('access_token')

        return response

    def get_page(self, path, return_content=True, return_html=True):
        """ Get a Telegraph page

        :param path: Path to the Telegraph page (in the format Title-12-31,
                     i.e. everything that comes after https://telegra.ph/)

        :param return_content: If true, content field will be returned
        :param return_html: If true, returns HTML instead of Nodes list
        """

        response = self._telegraph.method('getPage', path=path, values={
            'return_content': return_content
        })

        if return_content and return_html:
            response['content'] = nodes_to_html(response['content'])

        return response

    def create_page(self, title, content=None, html_content=None,
                    author_name=None, author_url=None, return_content=False):
        """ Create a new Telegraph page

        :param title: Page title

        :param content: Content in nodes list format (see doc)

        :param html_content: Content in HTML format

        :param author_name: Author name, displayed below the article's title

        :param author_url: Profile link, opened when users click on
                           the author's name below the title

        :param return_content: If true, a content field will be returned
        """

        if content is None:
            content = html_to_nodes(html_content)

        content_json = json.dumps(content, ensure_ascii=False)

        return self._telegraph.method('createPage', values={
            'title': title,
            'author_name': author_name,
            'author_url': author_url,
            'content': content_json,
            'return_content': return_content
        })

    def edit_page(self, path, title, content=None, html_content=None,
                  author_name=None, author_url=None, return_content=False):
        """ Edit an existing Telegraph page

        :param path: Path to the page

        :param title: Page title

        :param content: Content in nodes list format (see doc)

        :param html_content: Content in HTML format

        :param author_name: Author name, displayed below the article's title

        :param author_url: Profile link, opened when users click on
                           the author's name below the title

        :param return_content: If true, a content field will be returned
        """

        if content is None:
            content = html_to_nodes(html_content)

        content_json = json.dumps(content, ensure_ascii=False)

        return self._telegraph.method('editPage', path=path, values={
            'title': title,
            'author_name': author_name,
            'author_url': author_url,
            'content': content_json,
            'return_content': return_content
        })

    def get_account_info(self, fields=None):
        """ Get information about a Telegraph account

        :param fields: List of account fields to return. Available fields:
                       short_name, author_name, author_url, auth_url, page_count

                       Default: [“short_name”,“author_name”,“author_url”]
        """

        return self._telegraph.method('getAccountInfo', {
            'fields': json.dumps(fields, ensure_ascii=False) if fields else None
        })

    def get_page_list(self, offset=0, limit=50):
        """ Get a list of pages belonging to a Telegraph account
            sorted by most recently created pages first

        :param offset: Sequential number of the first page to be returned
                       (default = 0)

        :param limit: Limits the number of pages to be retrieved
                      (0-200, default = 50)
        """

        return self._telegraph.method('getPageList', {
            'offset': offset,
            'limit': limit
        })

    def get_views(self, path, year=None, month=None, day=None, hour=None):
        """ Get the number of views for a Telegraph article

        :param path: Path to the Telegraph page

        :param year: Required if month is passed. If passed, the number of
                     page views for the requested year will be returned

        :param month: Required if day is passed. If passed, the number of
                      page views for the requested month will be returned

        :param day: Required if hour is passed. If passed, the number of
                    page views for the requested day will be returned

        :param hour: If passed, the number of page views for
                     the requested hour will be returned
        """

        return self._telegraph.method('getViews', path=path, values={
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        })
