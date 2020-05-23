# Headers Class

Object-oriented representation for Headers. Contains a list of Header with some level of abstraction.
Combine advantages of dict, CaseInsensibleDict, list, multi-dict, and native objects. Headers do not inherit the Mapping type, but it does borrow some concepts from it.
A Headers can be casted to `str`, `bytes` and `dict`.

Given this :

```python
from kiss_headers import Headers, Header

headers = Headers(Header("Content-Type", "application/json"), Header("Allow", "POST"), Header("Accept", "text/html,application/json;q=0.8"))

str(headers)  # output: 'Content-Type: application/json\r\nAllow: POST\r\nAccept: text/html,application/json;q=0.8'
repr(headers)  # output: 'Content-Type: application/json\r\nAllow: POST\r\nAccept: text/html,application/json;q=0.8'
bytes(headers)  # output: b'Content-Type: application/json\r\nAllow: POST\r\nAccept: text/html,application/json;q=0.8'
dict(headers)  # output: {'Content-Type': Content-Type: application/json, 'Allow': Allow: POST, 'Accept': Accept: text/html,application/json;q=0.8}
headers.to_dict()  # output: {'Content-Type': 'application/json', 'Allow': 'POST', 'Accept': 'text/html,application/json;q=0.8'}
```

### Setup

If you wish to run bellow examples, first do :

```python
from kiss_headers import parse_it
from requests import get

headers = parse_it(get('https://www.python.org'))
```

### Check for existence of a header

```python
'Content-Type' in headers
# OR
'Content-Type' in headers.keys()
# OR
hasattr(headers, 'content-type')
# OR
headers.has('content-type')
```

### Accessing a header

```python
headers.content_type
# OR
headers['content-type']
# OR
headers.get('content-type')
```

### Removing the header

It is possible to remove an header in multiple ways. 
*e.g.* If you would like to remove `Content-Type` header.

#### Using del

```python
del headers['Content-Type']
# OR
del headers.content_type
```

#### Using native subtract

```python
headers -= 'Content-Type'
# OR
headers = headers - 'Content-Type'
```

### Adding a header

It is possible to add an header in multiple ways. 
eg. If you would like to add `Content-Type` header.

You will have to import the `Header` class, in addition to `parse_it`, as done below.
```python
from kiss_headers import Header
```

#### Using native addition

```python
headers += Header('Content-Type', 'application/json')
```

#### Using assignments

```python
headers['content-type'] = 'application/json'
# OR
headers.content_type = 'application/json'
```

### Compare content

Consider this : `Content-Type` content is `application/json; charset=utf-8`.

The following would result in a `True` statement.

```python
headers.content_type == 'application/json'
'application/json' in headers.content_type
'charset' in headers.content_type
```

The following would result in a `False` statement.
```python
headers.content_type == 'application'
'application' in headers.content_type
```

### Cast to dict 

You could use `to_dict()` method to obtain a `CaseInsensibleDict` from a `Headers` object.
Any headers that are OneToMany will be concatenated into one entry, separated with a comma.

You could also directly cast a Headers instance to dict using `dict(headers)`, the values are of type `Union[Header, List[Header]]`. Keys won't be case insensitive.
