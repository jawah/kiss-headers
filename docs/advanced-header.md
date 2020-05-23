# Header Class

This class is used to represent a single header as an object. An Header can be casted to `str`, `bytes` and `dict`.
Given this :

```python
from kiss_headers import Header

header = Header("Content-Type", "text/html; charset=UTF-8")

str(header)  # output: 'text/html; charset=UTF-8'
repr(header)  # output: 'Content-Type: text/html; charset=UTF-8'
bytes(header)  # output: b'Content-Type: text/html; charset=UTF-8'
dict(header)  # output: {'text/html': None, 'charset': 'UTF-8'}
```

### Setup

If you wish to run bellow examples, first do :

```python
from kiss_headers import parse_it
from requests import get

headers = parse_it(get('https://www.python.org'))
```

### Check existence of an attribute in header

Choose any flavour you like when checking for an attribute like `charset=utf-8`.

```python
'charset' in headers.content_type
# OR
hasattr(headers.content_type, 'charset')
# OR
headers.content_type.has('charset')
```

### Accessing an attribute

```python
headers.content_type.charset
# OR
headers.content_type['charset']
# OR
headers.content_type.get('charset')
```

### Remove an attribute

If attribute exists multiple times, this removes all entries.

```python
del headers.content_type.charset
# OR
del headers.content_type['charset']
```

### Remove a member from it

If adjective/member exists multiple times, this removes all entries.

```python
headers.content_type -= 'text/html'
```

### Create an attribute on the fly

```python
headers.content_type.charset = 'utf-8'
# OR
headers.content_type['charset'] = 'utf-8'
```

