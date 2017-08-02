# class Telegraph(object):

## Methods defined here:
### \_\_init\_\_

- access_token (default: `None`) — Telegraph access token

### create_account
 Create a new Telegraph account
- short_name — Account name, helps users with several accounts remember which they are currently using. Displayed to the user above the "Edit/Publish" button on Telegra.ph, other users don't see this name
- author_name (default: `None`) — Default author name used when creating new articles
- author_url (default: `None`) — Default profile link, opened when users click on the author's name below the title. Can be any link, not necessarily to a Telegram profile or channels
- replace_token (default: `True`) — Replaces current token to a new user's token

### create_page
 Create a new Telegraph page
- title — Page title
- content (default: `None`) — Content in nodes list format (see doc)
- html_content (default: `None`) — Content in HTML format
- author_name (default: `None`) — Author name, displayed below the article's title
- author_url (default: `None`) — Profile link, opened when users click on the author's name below the title
- return_content (default: `False`) — If true, a content field will be returned

### edit_account_info
 Update information about a Telegraph account. Pass only the parameters that you want to edit
- short_name (default: `None`) — Account name, helps users with several accounts remember which they are currently using. Displayed to the user above the "Edit/Publish" button on Telegra.ph, other users don't see this name
- author_name (default: `None`) — Default author name used when creating new articles
- author_url (default: `None`) — Default profile link, opened when users click on the author's name below the title. Can be any link, not necessarily to a Telegram profile or channels

### edit_page
 Edit an existing Telegraph page
- path — Path to the page
- title — Page title
- content (default: `None`) — Content in nodes list format (see doc)
- html_content (default: `None`) — Content in HTML format
- author_name (default: `None`) — Author name, displayed below the article's title
- author_url (default: `None`) — Profile link, opened when users click on the author's name below the title
- return_content (default: `False`) — If true, a content field will be returned

### get_access_token
 Return current access_token

### get_account_info
 Get information about a Telegraph account
- fields (default: `None`) — List of account fields to return. Available fields: short_name, author_name, author_url, auth_url, page_count Default: [“short_name”,“author_name”,“author_url”]

### get_page
 Get a Telegraph page
- path — Path to the Telegraph page (in the format Title-12-31, i.e. everything that comes after [http://telegra.ph/](http://telegra.ph/))
- return_content (default: `True`) — If true, content field will be returned
- return_html (default: `True`) — If true, returns HTML instead of Nodes list

### get_page_list
 Get a list of pages belonging to a Telegraph account sorted by most recently created pages first
- offset (default: `0`) — Sequential number of the first page to be returned (default = 0)
- limit (default: `50`) — Limits the number of pages to be retrieved (0-200, default = 50)

### get_views
 Get the number of views for a Telegraph article
- path — Path to the Telegraph page
- year (default: `None`) — Required if month is passed. If passed, the number of page views for the requested year will be returned
- month (default: `None`) — Required if day is passed. If passed, the number of page views for the requested month will be returned
- day (default: `None`) — Required if hour is passed. If passed, the number of page views for the requested day will be returned
- hour (default: `None`) — If passed, the number of page views for the requested hour will be returned

### revoke_access_token
 Revoke access_token and generate a new one, for example, if the user would like to reset all connected sessions, or you have reasons to believe the token was compromised. On success, returns dict with new access_token and auth_url fields

