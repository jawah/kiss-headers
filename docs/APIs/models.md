# Module `kiss_headers.models` {#kiss_headers.models}


## Functions

### Function `lock_output_type` {#kiss_headers.models.lock_output_type}


> `def lock_output_type(lock: bool = True) -> NoneType`

This method will restrict type entropy by always returning a List[Header] instead of Union[Header, List[Header]]

## Classes

### Class `Header` {#kiss_headers.models.Header}

> `class Header(name: str, content: str)`

Object representation of a single Header.

:param name: The name of the header, should contain only ASCII characters with no spaces in it.
:param content: Initial content associated with the header.

#### Descendants

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)

#### Instance variables



##### Variable `attrs` {#kiss_headers.models.Header.attrs}

List of members or attributes found in provided content.
eg. Content-Type: application/json; charset=utf-8; format=origin
Would output : ['application/json', 'charset', 'format']


##### Variable `comments` {#kiss_headers.models.Header.comments}

Retrieve comments in header content.


##### Variable `content` {#kiss_headers.models.Header.content}

Output associated content to header as it was captured initially.
```python
header = Header("ETag", '"33a64df551425fcc55e4d42a148795d9f25f89d4"')
header.content
'33a64df551425fcc55e4d42a148795d9f25f89d4'
```



##### Variable `name` {#kiss_headers.models.Header.name}

Output the original header name as it was captured initially


##### Variable `normalized_name` {#kiss_headers.models.Header.normalized_name}

Output header name but normalized, lower case and '-' character become '_'.


##### Variable `pretty_name` {#kiss_headers.models.Header.pretty_name}

Output a prettified name of the header. First letter capitalized of each word.


##### Variable `unfolded_content` {#kiss_headers.models.Header.unfolded_content}

Output unfolded associated content to header. Meaning that every LF + n space(s) would be properly
replaced.




#### Methods



##### Method `get` {#kiss_headers.models.Header.get}




> `def get(self, attr: str) -> Union[str, List[str], NoneType]`


Retrieve associated value of an attribute.
```python
header = Header("Content-Type", "application/json; charset=UTF-8; format=flowed")
header.charset
'UTF-8'
header.ChArSeT
'UTF-8'
header.FORMAT
'flowed'
header.format
'flowed'
```



##### Method `has` {#kiss_headers.models.Header.has}




> `def has(self, attr: str) -> bool`


Safely check is current header has an attribute or adjective in it.


##### Method `has_many` {#kiss_headers.models.Header.has_many}




> `def has_many(self, name: str) -> bool`


Determine if an attribute name has multiple entries in Header. Detect OneToMany entries.
```python
header = Header("A", "charset=UTF-8; charset=ASCII; format=flowed")
header.has_many("charset")
True
header.has_many("format")
False
```



### Class `Headers` {#kiss_headers.models.Headers}



> `class Headers(*headers: Union[List[kiss_headers.models.Header], kiss_headers.models.Header])`


Object oriented representation for Headers. Contains a list of Header with some level of abstraction.
Combine advantages of dict, CaseInsensibleDict and native objects.
Headers does not inherit of the Mapping type, but it does borrow some concept from it.

:param headers: Initial list of header. Can be empty.








#### Methods



##### Method `get` {#kiss_headers.models.Headers.get}




> `def get(self, header: str) -> Union[kiss_headers.models.Header, List[kiss_headers.models.Header], NoneType]`


Retrieve header from headers if exists


##### Method `has` {#kiss_headers.models.Headers.has}




> `def has(self, header: str) -> bool`


Safely check if header name is in headers


##### Method `has_many` {#kiss_headers.models.Headers.has_many}




> `def has_many(self, name: str) -> bool`


Determine if an header name has multiple entries in Headers. Detect OneToMany entries.
```python
headers = Header("A", "0") + Header("A", "1") + Header("B", "sad")
headers.has_many("a")
True
headers.has_many("b")
False
```



##### Method `items` {#kiss_headers.models.Headers.items}




> `def items(self) -> List[Tuple[str, str]]`


Provide an iterator witch each entry contain a tuple of header name and content.
This wont return a ItemView.
```python
headers = Header("X-Hello-World", "1") + Header("Content-Type", "happiness=True") + Header("Content-Type", "happiness=False")
headers.items()
[('X-Hello-World', '1'), ('Content-Type', 'happiness=True'), ('Content-Type', 'happiness=False')]
```



##### Method `keys` {#kiss_headers.models.Headers.keys}




> `def keys(self) -> List[str]`


Return a list of distinct header name set in headers.
Be aware that it wont return a typing.KeysView


##### Method `pop` {#kiss_headers.models.Headers.pop}




> `def pop(self) -> Union[kiss_headers.models.Header, List[kiss_headers.models.Header]]`


Pop header from headers. By default the last one.


##### Method `popitem` {#kiss_headers.models.Headers.popitem}




> `def popitem(self) -> Tuple[str, str]`


Pop last header as a tuple (header name, header content).


##### Method `to_dict` {#kiss_headers.models.Headers.to_dict}




> `def to_dict(self) -> kiss_headers.structures.CaseInsensitiveDict`


Provide a CaseInsensitiveDict output of current headers. This output type has been borrowed from psf/requests.
If one header appear multiple times, if would be concatenated into the same value, separated by comma.
Be aware that this repr could lead to mistake.


##### Method `to_json` {#kiss_headers.models.Headers.to_json}




> `def to_json(self) -> str`


Provide a JSON representation of Headers


##### Method `values` {#kiss_headers.models.Headers.values}




> `def values(self) -> NotImplemented`


I choose not to implement values() on Headers as it would bring more confusion..
Either we make it the same len as keys() or we don't. Either way don't please me. Hope to ear from the
community about this.



