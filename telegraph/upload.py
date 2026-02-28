from .api import TelegraphApi


def upload_file(f):
    """Deprecated, use Telegraph.upload_file"""
    import warnings

    warnings.warn(
        "telegraph.upload_file is deprecated, use Telegraph.upload_file",
        DeprecationWarning,
    )

    r = TelegraphApi().upload_file(f)
    return [i["src"] for i in r]
