# Telegraph
Python Telegraph API wrapper

# Example
    from telegraph import Telegraph
    
    telegraph = Telegraph()

    telegraph.create_account(short_name='1337')

    response = telegraph.create_page(
        'Python Telegraph API wrapper',
        html_content='<p>Hello, world!</p>'
    )

    print('http://telegra.ph/{}'.format(response['path']))

# Installation

    $ pip install telegraph
