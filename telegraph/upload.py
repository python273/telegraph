import mimetypes
import requests

from .exceptions import TelegraphException


def check_file(f):
    if hasattr(f, 'read'):
        if hasattr(f, 'name'):
            filename = f.name
        else:
            filename = ''
        opened = False
    else:
        f = open(f, 'rb')
        filename = f.name
        opened = True

    mime = mimetypes.MimeTypes().guess_type(filename)[0]
    return f, mime, opened


def upload_file(f):
    f, mime, opened = check_file(f)
    response = requests.post(
        'http://telegra.ph/upload',
        files={'file': ('file', f, mime)}
    ).json()

    if opened:
        f.close()

    try:
        error = response.get('error')
    except AttributeError:
        error = response[0].get('error')
    if error:
        raise TelegraphException(error)

    return response[0]['src']
