# Telegraph
[![Build Status](https://travis-ci.org/python273/telegraph.svg?branch=master)](https://travis-ci.org/python273/telegraph)

Python Telegraph API wrapper

python2 and python3 are supported

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
