import mimetypes
import requests

from .exceptions import TelegraphException


def check_file(paths):
    files = []
    mimes = []
    opened_files = []
    for f in paths:
        if hasattr(f, 'read'):
            if hasattr(f, 'name'):
                filename = f.name
            else:
                filename = ''
        else:
            f = open(f, 'rb')
            filename = f.name
            opened_files.append(f)

        mimes.append(mimetypes.MimeTypes().guess_type(filename)[0])
        files.append(f)
    return files, mimes, opened_files


def upload_file(f):
    """ Upload file to Telegra.ph's servers. Returns {"file<number>": "<link>"}.
        Allowed only .jpg, .jpeg, .png, .gif and .mp4 files.

        :param f: Filename or file-like object.
        :type f: file, str or list
    """
    files, mimes, opened_files = check_file(f)
    files_req = {}

    for x, f in enumerate(files):
        files_req[f'file{x}'] = (f'file{x}', f, mimes[x])

    response = requests.post(
        'http://telegra.ph/upload',
        files=files_req
    ).json()

    for f in opened_files:
        f.close()

    try:
        error = response.get('error')
    except AttributeError:
        error = response[0].get('error')
    if error:
        raise TelegraphException(error)

    res = {}
    for x, src in enumerate(response):
        src = f['src']
        res[f'file{x}'] = (f'{src}')

    return res
