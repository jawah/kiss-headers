### Setup
Consider this :

```python
from kiss_headers import parse_it
from requests import get

headers = parse_it(get('https://www.python.org'))
```

### Test existence of an header

```python
'Content-Type' in headers
# OR
'Content-Type' in headers.keys()
# OR
hasattr(headers, 'content-type')
# OR
headers.has('content-type')
```

### Accessing it

```python
headers.content_type
# OR
headers['content-type']
# OR
headers.get('content-type')
```

### Removing

It is possible to remove an header using multiple way. 
eg. If you would like to remove `Content-Type` header.

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

### Adding

It is possible to add an header using multiple way. 
eg. If you would like to add `Content-Type` header.

You will have to import like bellow `Header` class in addition of `parse_it`.
```python
from kiss_headers import Header
```

#### Using native addition

```python
headers += Header('Content-Type', 'application/json')
```

#### Using assignation

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
