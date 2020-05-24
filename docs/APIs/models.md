# Module `kiss_headers.models` {#kiss_headers.models}


## Functions

### Function `lock_output_type` {#kiss_headers.models.lock_output_type}


> `def lock_output_type(lock: bool = True) -> NoneType`

This method will restrict type entropy by always returning a List[Header] instead of Union[Header, List[Header]]

## Classes

### Class `Attributes` {#kiss_headers.models.Attributes}


> `class Attributes(members: List[str])`

Dedicated class to handle attributes within a Header. Wrap an AttributeBag and offer methods to manipulate it
with ease.
Store advanced info on attributes, case insensitive on keys and keep attrs ordering.

#### Instance variables

##### Variable `last_index` {#kiss_headers.models.Attributes.last_index}

Simply output the latest index used in attributes. Index start from zero.

#### Methods

##### Method `insert` {#kiss_headers.models.Attributes.insert}

> `def insert(self, key: str, value: Union[str, NoneType], index: Union[int, NoneType] = None) -> NoneType`

##### Method `keys` {#kiss_headers.models.Attributes.keys}

> `def keys(self) -> List[str]`

This method return a list of attribute name that have at least one value associated to them.

##### Method `remove` {#kiss_headers.models.Attributes.remove}

> `def remove(self, key: str, index: Union[int, NoneType] = None, with_value: Union[bool, NoneType] = None) -> NoneType`

### Class `Header` {#kiss_headers.models.Header}

> `class Header(name: str, content: str)`

Object representation of a single Header.

:param name: The name of the header, should contain only ASCII characters with no spaces in it.
:param content: Initial content associated with the header.

#### Descendants

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)

#### Instance variables



##### Variable `attrs` {#kiss_headers.models.Header.attrs}

List of members or attributes found in provided content. This list is ordered and normalized.
eg. Content-Type: application/json; charset=utf-8; format=origin
Would output : ['application/json', 'charset', 'format']


##### Variable `comments` {#kiss_headers.models.Header.comments}

Retrieve comments in header content.


##### Variable `content` {#kiss_headers.models.Header.content}

Output associated content to the header as it was captured initially.
```python
header = Header("ETag", '"33a64df551425fcc55e4d42a148795d9f25f89d4"')
header.content
'33a64df551425fcc55e4d42a148795d9f25f89d4'
```



##### Variable `name` {#kiss_headers.models.Header.name}

Output the original header name as it was captured initially.


##### Variable `normalized_name` {#kiss_headers.models.Header.normalized_name}

Output header name but normalized, lower case and '-' character become '_'.


##### Variable `pretty_name` {#kiss_headers.models.Header.pretty_name}

Output a prettified name of the header. The first letter capitalized on each word.


##### Variable `unfolded_content` {#kiss_headers.models.Header.unfolded_content}

Output unfolded associated content to the header. Meaning that every LF + n space(s) would be properly
replaced.


##### Variable `valued_attrs` {#kiss_headers.models.Header.valued_attrs}

List of distinct attributes that have at least one value associated with them. This list is ordered and normalized.
This property could have been written under the keys() method, but implementing it would interfere with dict()
cast and the __iter__() method.
eg. Content-Type: application/json; charset=utf-8; format=origin
Would output : ['charset', 'format']

#### Methods



##### Method `get` {#kiss_headers.models.Header.get}


> `def get(self, attr: str) -> Union[str, List[str], NoneType]`

Retrieve the associated value of an attribute.
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


Safely check if the current header has an attribute or adjective in it.


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



##### Method `insert` {#kiss_headers.models.Header.insert}




> `def insert(self, _Header__index: int, *_Header__members: str, **_Header__attributes: Union[str, NoneType]) -> NoneType`


This method allows you to properly insert attributes into a Header instance.


##### Method `pop` {#kiss_headers.models.Header.pop}




> `def pop(self) -> Tuple[str, Union[str, List[str], NoneType]]`


Permit to pop an element from a Header with a given index.
```python
header = Header("X", "a; b=k; h; h; z=0; y=000")
header.pop(1)
('b', 'k')
header.pop()
('y', '000')
header.pop('z')
('z', '0')
```



### Class `Headers` {#kiss_headers.models.Headers}



> `class Headers(*headers: Union[List[kiss_headers.models.Header], kiss_headers.models.Header])`


Object-oriented representation for Headers. Contains a list of Header with some level of abstraction.
Combine advantages of dict, CaseInsensibleDict, list, multi-dict, and native objects.
Headers do not inherit the Mapping type, but it does borrow some concepts from it.

:param headers: Initial list of header. Can be empty.








#### Methods



##### Method `get` {#kiss_headers.models.Headers.get}




> `def get(self, header: str) -> Union[kiss_headers.models.Header, List[kiss_headers.models.Header], NoneType]`


Retrieve header from headers if exists.


##### Method `has` {#kiss_headers.models.Headers.has}




> `def has(self, header: str) -> bool`


Safely check if header name is in headers.


##### Method `has_many` {#kiss_headers.models.Headers.has_many}




> `def has_many(self, name: str) -> bool`


Determine if a header name has multiple entries in Headers. Detect OneToMany entries.
```python
headers = Header("A", "0") + Header("A", "1") + Header("B", "sad")
headers.has_many("a")
True
headers.has_many("b")
False
```



##### Method `index` {#kiss_headers.models.Headers.index}




> `def index(self, _Headers__value: Union[kiss_headers.models.Header, str]) -> int`


Search for the first appearance of an header based on its name or instance in Headers.
Same method signature as list().index().
Raises IndexError if not found.
```python
headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle")
headers.index("A")
0
headers.index("A", 1)
Traceback (most recent call last):
...
IndexError: Value 'A' is not present within Headers.
headers.index("A", 0, 1)
0
headers.index("C")
2
headers.index(headers[0])
0
headers.index(headers[1])
1
```



##### Method `insert` {#kiss_headers.models.Headers.insert}




> `def insert(self, _Headers__index: int, _Headers__header: kiss_headers.models.Header) -> NoneType`


Insert header before the given index.


##### Method `items` {#kiss_headers.models.Headers.items}




> `def items(self) -> List[Tuple[str, str]]`


Provide a list witch each entry contains a tuple of header name and content.
This won't return an ItemView as Headers does not inherit from Mapping.
```python
headers = Header("X-Hello-World", "1") + Header("Content-Type", "happiness=True") + Header("Content-Type", "happiness=False")
headers.items()
[('X-Hello-World', '1'), ('Content-Type', 'happiness=True'), ('Content-Type', 'happiness=False')]
```



##### Method `keys` {#kiss_headers.models.Headers.keys}




> `def keys(self) -> List[str]`


Return a list of distinct header name set in headers.
Be aware that it won't return a typing.KeysView.
Also this method allows you to create a case sensitive dict.


##### Method `pop` {#kiss_headers.models.Headers.pop}




> `def pop(self) -> Union[kiss_headers.models.Header, List[kiss_headers.models.Header]]`


Pop header instance(s) from headers. By default the last one. Accept index as integer or header name.
If you pass a header name, it will pop from Headers every entry named likewise.
```python
headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle")
header = headers.pop()
repr(header)
'C: funny; riddle'
headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle")
header = headers.pop(1)
repr(header)
'B: world'
header = headers.pop("A")
repr(header)
'A: hello'
headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle") + Header("B", "ending")
headers = headers.pop("B")
len(headers)
2
headers[0].name
'B'
(str(headers[0]), str(headers[1]))
('world', 'ending')
```



##### Method `popitem` {#kiss_headers.models.Headers.popitem}




> `def popitem(self) -> Tuple[str, str]`


Pop the last header as a tuple (header name, header content).


##### Method `to_dict` {#kiss_headers.models.Headers.to_dict}




> `def to_dict(self) -> kiss_headers.structures.CaseInsensitiveDict`


Provide a CaseInsensitiveDict output of current headers. This output type has been borrowed from psf/requests.
If one header appears multiple times, it would be concatenated into the same value, separated by a comma.
Be aware that this repr could lead to a mistake. You could also cast a Headers instance to dict() to get a
case sensitive one. see method keys().


##### Method `to_json` {#kiss_headers.models.Headers.to_json}




> `def to_json(self) -> str`


Provide a JSON representation of Headers. JSON is by definition a string.


##### Method `values` {#kiss_headers.models.Headers.values}




> `def values(self) -> NotImplemented`


I choose not to implement values() on Headers as it would bring more confusion...
Either we make it the same len as keys() or we don't. Either way don't please me. Hope to hear from the
community about this.

