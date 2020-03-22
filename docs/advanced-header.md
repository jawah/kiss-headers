### Setup

Consider this :

```python
from kiss_headers import parse_it
from requests import get

headers = parse_it(get('https://www.python.org'))
```

### Existence of an attribute in header

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

### Remove attribute

If attribute exist multiple time, it would remove all entries.

```python
del headers.content_type.charset
# OR
del headers.content_type['charset']
```

### Create attribute on the fly

```python
headers.content_type.charset = 'utf-8'
# OR
headers.content_type['charset'] = 'utf-8'
```

