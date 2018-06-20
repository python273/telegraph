import mimetypes
import requests

from .exceptions import TelegraphException

opened_files = []


def check_file(f):
    if hasattr(f, 'read'):
        if hasattr(f, 'name'):
            filename = f.name
        else:
            filename = ''
    else:
        f = open(f, 'rb')
        filename = f.name
        opened_files.append(f)

    mime = mimetypes.MimeTypes().guess_type(filename)[0]
    return f, mime


def upload_file(f):
    global opened_files
    f, mime = check_file(f)
    response = requests.post(
        'http://telegra.ph/upload',
        files={'file': ('file', f, mime)}
    ).json()

    for n in opened_files:
        n.close()
    opened_files = []

    try:
        error = response.get('error')
    except AttributeError:
        error = response[0].get('error')
    if error:
        raise TelegraphException(error)

    return response[0]['src']
