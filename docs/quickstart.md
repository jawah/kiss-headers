
### Using `parse_it`

The most common thing you'd do is to parse raw headers and turn them to objects.

`parse_it()` method takes `bytes`, `str`, `fp`, `dict`, `email.Message`, `requests.Response` and `httpx._models.Response` itself and returns a `Headers` object.

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

### ManySquashedIntoOne

There is an edge case (__Not only Set-Cookie__) where one header content could contain multiple entries (usually) separated by a comma.
Take the `Accept` header for instance. 

```
Accept: text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8
```

The library will split this entry into five entries/headers/objects.

```python
from kiss_headers import parse_it

headers = parse_it("Accept: text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8")

len(headers)  # output: 5
headers.has_many("accept")  # output: True
len(headers.accept)  # output: 5 

repr(headers.accept[0])  # output: 'Accept: text/html'
repr(headers.accept[3])  # output: 'Accept: application/xml;q=0.9'

# What if we want to verify that text/html is available in Accept ?
"text/html" in headers.accept  # output: True
"text/htm" in headers.accept  # output: False

# How to extract the qualifier ?
headers.accept[0].has("q")  # output: False
"q" in headers.accept[0]  # output: False

headers.accept[3].has("q")  # output: True
"q" in headers.accept[3]  # output: True

headers.accept[3]["q"]  # output: 0.9
```

This behavior is global to all headers.

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

### Lock the output type entropy

You might not like that some functions/methods in `Header` and `Headers` classes return type-hint is `Union[Header, List[Header]]`.
There is a quick way to enforce the return type to `List[Header]` only.

```python
from kiss_headers import lock_output_type

lock_output_type(True)
```
