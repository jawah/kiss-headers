# Module `kiss_headers.utils` {#kiss_headers.utils}



## Functions



### Function `class_to_header_name` {#kiss_headers.utils.class_to_header_name}




> `def class_to_header_name(type_: Type) -> str`


Take a type and infer its header name.
```python
from kiss_headers.builder import ContentType, XContentTypeOptions, BasicAuthorization
class_to_header_name(ContentType)
'Content-Type'
class_to_header_name(XContentTypeOptions)
'X-Content-Type-Options'
class_to_header_name(BasicAuthorization)
'Authorization'
```



### Function `count_leftover_space` {#kiss_headers.utils.count_leftover_space}




> `def count_leftover_space(content: str) -> int`


Recursive function that count trailing white space at the end of given string.
```python
count_leftover_space("hello   ")
3
count_leftover_space("byebye ")
1
count_leftover_space("  hello ")
1
count_leftover_space("  hello    ")
4
```



### Function `decode_partials` {#kiss_headers.utils.decode_partials}




> `def decode_partials(items: Iterable[Tuple[str, Any]]) -> List[Tuple[str, str]]`


This function takes a list of tuple, representing headers by key, value. Where value is bytes or string containing
(RFC 2047 encoded) partials fragments like the following :
```python
decode_partials([("Subject", "=?iso-8859-1?q?p=F6stal?=")])
[('Subject', 'pöstal')]
```



### Function `extract_class_name` {#kiss_headers.utils.extract_class_name}




> `def extract_class_name(type_: Type) -> Union[str, NoneType]`


Typically extract a class name from a Type.


### Function `extract_comments` {#kiss_headers.utils.extract_comments}




> `def extract_comments(content: str) -> List[str]`


Extract parts of content that are considered as comments. Between parenthesis.
```python
extract_comments("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0 (hello) llll (abc)")
['Macintosh; Intel Mac OS X 10.9; rv:50.0', 'hello', 'abc']
```



### Function `extract_encoded_headers` {#kiss_headers.utils.extract_encoded_headers}




> `def extract_encoded_headers(payload: bytes) -> Tuple[str, bytes]`


This function purpose is to extract lines that can be decoded using utf-8.
```python
extract_encoded_headers("Host: developer.mozilla.org\r\nX-Hello-World: 死の漢字\r\n\r\n".encode("utf-8"))
('Host: developer.mozilla.org\r\nX-Hello-World: 死の漢字\r\n', b'')
extract_encoded_headers("Host: developer.mozilla.org\r\nX-Hello-World: 死の漢字\r\n\r\nThat IS totally random.".encode("utf-8"))
('Host: developer.mozilla.org\r\nX-Hello-World: 死の漢字\r\n', b'That IS totally random.')
```



### Function `header_content_split` {#kiss_headers.utils.header_content_split}




> `def header_content_split(string: str, delimiter: str) -> List[str]`


Take a string and split it according to the passed delimiter.
It will ignore delimiter if inside between double quote, inside a value or in parenthesis.
The input string is considered perfectly formed. This function do not split coma on a day
when attached, see "RFC 7231, section 7.1.1.2: Date".
```python
header_content_split("Wed, 15-Apr-2020 21:27:31 GMT, Fri, 01-Jan-2038 00:00:00 GMT", ",")
['Wed, 15-Apr-2020 21:27:31 GMT', 'Fri, 01-Jan-2038 00:00:00 GMT']
header_content_split('quic=":443"; ma=2592000; v="46,43", h3-Q050=":443"; ma=2592000, h3-Q049=":443"; ma=2592000', ",")
['quic=":443"; ma=2592000; v="46,43"', 'h3-Q050=":443"; ma=2592000', 'h3-Q049=":443"; ma=2592000']
header_content_split("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0", ";")
['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0']
header_content_split("text/html; charset=UTF-8", ";")
['text/html', 'charset=UTF-8']
```



### Function `header_name_to_class` {#kiss_headers.utils.header_name_to_class}




> `def header_name_to_class(name: str, root_type: Type) -> Type`


The opposite of class_to_header_name function. Will raise TypeError if no corresponding entry is found.
Do it recursively from the root type.
```python
from kiss_headers.builder import CustomHeader, ContentType, XContentTypeOptions, LastModified, Date
header_name_to_class("Content-Type", CustomHeader)
<class 'kiss_headers.builder.ContentType'>
header_name_to_class("Last-Modified", CustomHeader)
<class 'kiss_headers.builder.LastModified'>
```



### Function `header_strip` {#kiss_headers.utils.header_strip}




> `def header_strip(content: str, elem: str) -> str`


Remove a member for a given header content and take care of the unneeded leftover semi-colon.
```python
header_strip("text/html; charset=UTF-8; format=flowed", "charset=UTF-8")
'text/html; format=flowed'
header_strip("text/html; charset=UTF-8;    format=flowed", "charset=UTF-8")
'text/html; format=flowed'
```



### Function `is_legal_header_name` {#kiss_headers.utils.is_legal_header_name}




> `def is_legal_header_name(name: str) -> bool`


Verify if a provided header name is valid.
```python
is_legal_header_name(":hello")
False
is_legal_header_name("hello")
True
is_legal_header_name("Content-Type")
True
is_legal_header_name("Hello;")
False
is_legal_header_name("Hello\rWorld")
False
is_legal_header_name("Hello \tWorld")
False
```



### Function `normalize_str` {#kiss_headers.utils.normalize_str}




> `def normalize_str(string: str) -> str`


Normalize a string by applying on it lowercase and replacing '-' to '_'.
```python
normalize_str("Content-Type")
'content_type'
normalize_str("X-content-type")
'x_content_type'
```



### Function `prettify_header_name` {#kiss_headers.utils.prettify_header_name}




> `def prettify_header_name(name: str) -> str`


Take a header name and prettify it.
```python
prettify_header_name("x-hEllo-wORLD")
'X-Hello-World'
prettify_header_name("server")
'Server'
prettify_header_name("contEnt-TYPE")
'Content-Type'
prettify_header_name("content_type")
'Content-Type'
```



### Function `quote` {#kiss_headers.utils.quote}




> `def quote(string: str) -> str`


Surround string by double quote.
```python
quote("hello")
'"hello"'
quote('"hello')
'""hello"'
quote('"hello"')
'"hello"'
```



### Function `unfold` {#kiss_headers.utils.unfold}




> `def unfold(content: str) -> str`


Some header content may have folded content (LF + 9 spaces, LF + 7 spaces or LF + 1 spaces) in it, making your job at reading them a little more difficult.
This function undo the folding in given content.
```python
unfold("eqHS2AQD+hfNNlTiLej73CiBUGVQifX4watAaxUkdjGeH578i7n3Wwcdw2nLz+U0bH\n         ehSe/2QytZGWM5CewwNdumT1IVGzjFs+cRgfK0V6JlEIOoV3bRXxnjenWFfWdVNXtw8s")
'eqHS2AQD+hfNNlTiLej73CiBUGVQifX4watAaxUkdjGeH578i7n3Wwcdw2nLz+U0bHehSe/2QytZGWM5CewwNdumT1IVGzjFs+cRgfK0V6JlEIOoV3bRXxnjenWFfWdVNXtw8s'
```



### Function `unpack_protected_keyword` {#kiss_headers.utils.unpack_protected_keyword}




> `def unpack_protected_keyword(name: str) -> str`


By choice this project aim to allow developper to access header or attribute in header by using the property
notation. Some keyword are protected by the language itself. So :
When starting by a number, prepend a underscore to it. When using a protected keyword, append a underscore to it.
```python
unpack_protected_keyword("_3to1")
'3to1'
unpack_protected_keyword("from_")
'from'
unpack_protected_keyword("_from")
'_from'
unpack_protected_keyword("3")
'3'
unpack_protected_keyword("FroM_")
'FroM_'
```



### Function `unquote` {#kiss_headers.utils.unquote}




> `def unquote(string: str) -> str`


Remove simple quote or double quote around a string if any.
```python
unquote('"hello"')
'hello'
unquote('"hello')
'"hello'
unquote('"a"')
'a'
unquote('""')
''
```




