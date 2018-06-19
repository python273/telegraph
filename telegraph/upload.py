import mimetypes
import requests

from .exceptions import TelegraphException


def check_file(file):
    if hasattr(file, 'read'):
        f = file
        if hasattr(file, 'name'):
            filename = file.name
        else:
            filename = ''
    else:
        f = open(file, 'rb')
        filename = file

    mime = mimetypes.MimeTypes().guess_type(filename)[0]
    if mime is None:
        f.close()
        raise TypeError('File doesn\'t have name or extension')

    return f, mime


def upload(file):
    f, mime = check_file(file)
    response = requests.post(
        'http://telegra.ph/upload',
        files={'file': ('file', f, mime)}
    ).json()[0]
    f.close()
    if response.get('error'):
        raise TelegraphException(response.get('error'))

    return response['src']
