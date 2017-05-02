# Telegraph
[![Build Status](https://travis-ci.org/python273/telegraph.svg?branch=master)](https://travis-ci.org/python273/telegraph)
[![PyPI](https://img.shields.io/pypi/v/telegraph.svg)](https://pypi.python.org/pypi/telegraph)
![Python Versions](https://img.shields.io/pypi/pyversions/telegraph.svg)
![License](https://img.shields.io/github/license/python273/telegraph.svg)

Python Telegraph API wrapper

# Example
```python
from telegraph import Telegraph

telegraph = Telegraph()

telegraph.create_account(short_name='1337')

response = telegraph.create_page(
    'Hey',
    html_content='<p>Hello, world!</p>'
)

print('http://telegra.ph/{}'.format(response['path']))
```

# Installation

```bash
$ pip install telegraph
```
