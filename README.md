# Telegraph
[![PyPI](https://img.shields.io/pypi/v/telegraph.svg)](https://pypi.python.org/pypi/telegraph)
![Python Versions](https://img.shields.io/pypi/pyversions/telegraph.svg)
![License](https://img.shields.io/github/license/python273/telegraph.svg)

Python Telegraph API wrapper

- [Documentation](https://python-telegraph.readthedocs.io/en/latest/)

```bash
$ python3 -m pip install telegraph
```

### Example
```python
from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='1337')

response = telegraph.create_page(
    'Hey',
    html_content='<p>Hello, world!</p>'
)
print(response['url'])

telegraph.close()
```

#### Or with context manager
```python

with Telegraph() as telegraph:
    telegraph.create_account(short_name='1337')
    response = telegraph.create_page(
        'Hey',
        html_content='<p>Hello, world!</p>'
    )
    print(response['url'])
```

### Async Example
```python
import asyncio
from telegraph.aio import Telegraph

async def main():
    telegraph = Telegraph()
    print(await telegraph.create_account(short_name='1337'))

    response = await telegraph.create_page(
        'Hey',
        html_content='<p>Hello, world!</p>',
    )
    print(response['url'])

    await telegraph.aclose()


asyncio.run(main())
```

#### Or with context manager
```python
import asyncio
from telegraph.aio import Telegraph

async def main():
    async with Telegraph() as telegraph:
        print(await telegraph.create_account(short_name='1337'))

        response = await telegraph.create_page(
            'Hey',
            html_content='<p>Hello, world!</p>',
        )
        print(response['url'])

asyncio.run(main())
```
