
### Using `parse_it` for the first time

`parse_it()` method takes `bytes`, `str`, `fp`, `dict` or even `requests.Response` itself and returns a `Headers` object.

```python
from requests import get
from kiss_headers import parse_it

response = get('https://www.google.fr')
headers = parse_it(response)

headers.content_type.charset  # output: ISO-8859-1
```

### OneToOne, OneToMany

Do not forget that headers are not 1 to 1. One header can be repeated multiple times and attributes can have multiple values within the same header.

```python
from kiss_headers import parse_it

my_cookies = """set-cookie: 1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT; path=/; domain=.google.fr; Secure; SameSite=none
set-cookie: CONSENT=WP.284b10; expires=Fri, 01-Jan-2038 00:00:00 GMT; path=/; domain=.google.fr"""

headers = parse_it(my_cookies)

type(headers.set_cookie)  # output: list
headers.set_cookie[0].expires # output Wed, 15-Apr-2020 21:27:31 GMT
```

### Using protected keyword

Just a note: Accessing a header that has the same name as a reserved keyword must be done this way :
```python
from kiss_headers import parse_it
headers = parse_it('From: Ousret; origin=www.github.com\nIS: 1\nWhile: Not-True')

# this flavour
headers.from_ # to access From, just add a single underscore to it
# or..
headers['from']
```
