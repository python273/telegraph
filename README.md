# Telegraph
[![PyPI](https://img.shields.io/pypi/v/telegraph.svg)](https://pypi.python.org/pypi/telegraph)
![Python Versions](https://img.shields.io/pypi/pyversions/telegraph.svg)
![License](https://img.shields.io/github/license/python273/telegraph.svg)

Python Telegraph API wrapper

- [Documentation](https://python-telegraph.readthedocs.io/en/latest/)

```bash
$ python3 -m pip install telegraph
```

# Example
```python
from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='1337')

response = telegraph.create_page(
    'Hey',
    html_content='<p>Hello, world!</p>'
)
print(response['url'])
```
