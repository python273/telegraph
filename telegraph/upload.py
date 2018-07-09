import mimetypes

import requests

from .exceptions import TelegraphException


def upload_file(f, fn=None):
    """ Upload file to Telegra.ph's servers. Returns a list of links.
        Allowed only .jpg, .jpeg, .png, .gif and .mp4 files.

        :param f: filename or file-like object.
        :type f: file, str or list

        :param fn: filename. Required if can't get filename
        :type fn: str or list
    """

    with FilesOpener(f, fn) as files:
        response = requests.post(
            'http://telegra.ph/upload',
            files=files
        ).json()

    if isinstance(response, list):
        error = response[0].get('error')
    else:
        error = response.get('error')

    if error:
        raise TelegraphException(error)

    return [i['src'] for i in response]


class FilesOpener(object):
    def __init__(self, paths, fn, key_format='file{}'):
        if not isinstance(paths, list):
            paths = [paths]

        if not isinstance(fn, list):
            fn = [fn]

        self.paths = paths
        self.fn = fn
        self.key_format = key_format
        self.opened_files = []

    def __enter__(self):
        return self.open_files()

    def __exit__(self, type, value, traceback):
        self.close_files()

    def open_files(self):
        self.close_files()

        files = []

        for x, file_or_name in enumerate(self.paths):
            if hasattr(file_or_name, 'read'):
                f = file_or_name

                if hasattr(f, 'name'):
                    filename = f.name
                else:
                    filename = self.fn[x]
            else:
                filename = file_or_name
                f = open(filename, 'rb')
                self.opened_files.append(f)

            mimetype = mimetypes.MimeTypes().guess_type(filename)[0]

            files.append(
                (self.key_format.format(x), ('file{}'.format(x), f, mimetype))
            )

        return files

    def close_files(self):
        for f in self.opened_files:
            f.close()

        self.opened_files = []
