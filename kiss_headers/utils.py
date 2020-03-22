from email.parser import HeaderParser, BytesHeaderParser
from io import BytesIO, IOBase
from typing import (
    List,
    Optional,
    Union,
    Dict,
    Mapping,
    Iterator,
    Tuple,
    Iterable,
    Any,
    NoReturn,
)
from email.header import decode_header
from re import findall, IGNORECASE, escape
from kiss_headers.structures import CaseInsensitiveDict
from copy import deepcopy

RESERVED_KEYWORD = [
    "and_",
    "assert_",
    "in_",
    "not_",
    "pass_",
    "finally_",
    "while_",
    "yield_",
    "is_",
    "as_",
    "break_",
    "return_",
    "elif_",
    "except_",
    "def_",
    "from_",
    "for_",
]


class Header(object):
    """
    Object representation of a single Header.
    """

    # Most common attribute that are associated with value in headers.
    # Used for type hint, auto completion purpose
    charset: str
    format: str
    boundary: str
    expires: str
    timeout: str
    max: str
    path: str
    samesite: str
    domain: str

    def __init__(self, name: str, content: str):

        self._name: str = name
        self._normalized_name: str = Header.normalize_name(self._name)
        self._content: str = content

        self._members: List[str] = [el.lstrip() for el in self._content.split(";")]

        self._not_valued_attrs: List[str] = list()
        self._valued_attrs: Dict[str, Union[str, List[str]]] = dict()
        self._valued_attrs_normalized: Dict[str, Union[str, List[str]]] = dict()

        for member in self._members:
            if "=" in member:
                key, value = tuple(member.split("=", maxsplit=1))

                # avoid confusing base64 look alike single value for (key, value)
                if value.count("=") == len(value) or len(value) == 0 or " " in key:
                    self._not_valued_attrs.append(member)
                    continue

                if key not in self._valued_attrs:
                    self._valued_attrs[key] = value
                else:
                    if isinstance(self._valued_attrs[key], str):
                        self._valued_attrs[key] = [self._valued_attrs[key], value]
                    else:
                        self._valued_attrs[key].append(value)

                self._valued_attrs_normalized[
                    Header.normalize_name(key)
                ] = self._valued_attrs[key]
                continue

            self._not_valued_attrs.append(member)

    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Normalize header name or attribute name by applying lowercase and replacing '-' to '_'.
        """
        return name.lower().replace("-", "_")

    @property
    def name(self) -> str:
        """
        Output the original header name as it was captured initially
        """
        return self._name

    @property
    def normalized_name(self) -> str:
        """
        Output header name but normalized, lower case and '-' character become '_'.
        """
        return self._normalized_name

    @property
    def content(self) -> str:
        """
        Output associated content to header as it was captured initially.
        """
        if len(self.attrs) == 1:
            if self._content.startswith('"') and self._content.endswith('"'):
                return self._content[1:-1]

        return self._content

    def __deepcopy__(self, memodict: Dict) -> "Header":
        return Header(deepcopy(self.name), deepcopy(self.content))

    def __setattr__(self, key: str, value: str) -> NoReturn:
        """
        Set attribute on header using the property notation.
        """

        # Avoid conflict with __init__ sequence of Header
        if key in [
            "_name",
            "_normalized_name",
            "_content",
            "_members",
            "_not_valued_attrs",
            "_valued_attrs_normalized",
            "_valued_attrs",
        ]:
            return super().__setattr__(key, value)

        if key[0] == "_":
            key = key[1:]

        if key.lower() in RESERVED_KEYWORD:
            key = key[:-1]

        self[key] = value

    def __setitem__(self, key: str, value: str) -> NoReturn:
        """
        Set an attribute bracket syntax like. This will erase previously set attribute named after the key.
        """
        key_normalized = Header.normalize_name(key)

        if key in self:
            del self[key]

        self._valued_attrs[key] = value
        self._valued_attrs_normalized[key_normalized] = self._valued_attrs[key]

        self._content += '; {key}="{value}"'.format(key=key, value=value)

    def __delitem__(self, key: str) -> NoReturn:
        """
        Remove any attribute named after the key in header using the bracket syntax.
           >>> del headers.content_type['charset']
        """
        key_normalized = Header.normalize_name(key)

        if key_normalized not in self._valued_attrs_normalized:
            raise KeyError(
                "'{item}' attribute is not defined within '{header}' header.".format(
                    item=key, header=self.name
                )
            )

        del self._valued_attrs_normalized[key]
        not_normalized_keys = self._valued_attrs.keys()

        for key_ in not_normalized_keys:
            if Header.normalize_name(key_) == key_normalized:
                del self._valued_attrs[key_]
                break

        for elem in findall(
            r"{key_name}=.*?(?=[;\n])".format(key_name=escape(key)),
            self._content + "\n",
            IGNORECASE,
        ):

            has_semicolon_at_the_end: bool = False

            try:
                self._content.index(elem + ";")
                has_semicolon_at_the_end = True
            except ValueError:
                pass

            self._content: str = self._content.replace(
                elem + (";" if has_semicolon_at_the_end else ""), ""
            ).rstrip(" ").lstrip(" ")

            if self._content.startswith(";"):
                self._content = self._content[1:]

            if self._content.endswith(";"):
                self._content = self._content[:-1]

    def __delattr__(self, item: str) -> NoReturn:
        """
        Remove any attribute named after the key in header using the property notation.
           >>> del headers.content_type.charset
        """
        item = Header.normalize_name(item)

        if item not in self._valued_attrs_normalized:
            raise AttributeError(
                "'{item}' attribute is not defined within '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        del self[item]

    def __iter__(self) -> Iterator[Tuple[str, Optional[str]]]:
        for key, value in self._valued_attrs.items():
            yield key, self[key]
        for adjective in self._not_valued_attrs:
            yield adjective, None

    def __eq__(self, other: Union[str, "Header"]) -> bool:
        """
        Verify equality between a Header object and str or another Header object.
        If testing against str, the first thing is to match it to raw content, if not equal verify if not in members.
        """
        if isinstance(other, str):
            return self.content == other or other in self._not_valued_attrs
        if isinstance(other, Header):
            return (
                self.normalized_name == other.normalized_name
                and self.content == other.content
            )
        raise TypeError(
            "Cannot compare type {type_} to an Header. Use str or Header.".format(
                type_=type(other)
            )
        )

    def __str__(self) -> str:
        """
        Allow to cast a single header to a string. Only content would be exposed here.
        """
        return self._content

    def __repr__(self) -> str:
        """
        Unambiguous representation of a single header.
        """
        return "{head}: {content}".format(head=self._name, content=self._content)

    def __dir__(self) -> Iterable[str]:
        """
        Provide a better auto-completion when using python interpreter. We are feeding __dir__ so Python can be aware
        of what properties are callable. In other word, more precise auto-completion when not using IDE.
        """
        return super().__dir__() + list(self._valued_attrs_normalized.keys())

    @property
    def attrs(self) -> List[str]:
        """
        List of members or attributes found in provided content.
        eg. Content-Type: application/json; charset=utf-8; format=origin
        Would output : ['application/json', 'charset', 'format']
        """
        return list(self._valued_attrs.keys()) + self._not_valued_attrs

    def has(self, attr: str) -> bool:
        """
        Safely check is current header has an attribute or adjective in it.
        """
        return attr in self

    def get(self, attr: str) -> Optional[str]:
        """
        Retrieve associated value of an attribute.
        """
        if attr not in self._valued_attrs:
            return None
        return self._valued_attrs[attr]

    def __getitem__(self, item: Union[str, int]) -> Union[str, List[str]]:
        """
        This method will allow you to retrieve attribute value using the bracket syntax, list-like.
        """
        normalized_item = Header.normalize_name(item)

        if item in self._valued_attrs:
            value = self._valued_attrs[item]
        elif normalized_item in self._valued_attrs_normalized:
            value = self._valued_attrs_normalized[normalized_item]
        else:
            raise KeyError(
                "'{item}' attribute is not defined within '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        # Unquote value if necessary
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            return value[1:-1]

        return value

    def __getattr__(self, item: str) -> str:
        """
        All the magic happen here, this method should be invoked when trying to call (not declared) properties.
        For instance, calling self.charset should end up here and be replaced by self['charset'].
        """
        if item[0] == "_":
            item = item[1:]

        if item.lower() in RESERVED_KEYWORD:
            item = item[:-1]

        if (
            item not in self._valued_attrs
            and Header.normalize_name(item) not in self._valued_attrs_normalized
        ):
            raise AttributeError(
                "'{item}' attribute is not defined within '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        return self[item]

    def __contains__(self, item: str) -> bool:
        if item in self.attrs:
            return True
        item = Header.normalize_name(item)
        for attr in self.attrs:
            if item == Header.normalize_name(attr):
                return True
        return False


class Headers:
    """
    Object oriented representation for Headers. Contains a list of Header with some level of abstraction.
    Combine advantages of dict, CaseInsensibleDict and objects.
    """

    # Most common headers that you may or may not find. This should be appreciated when having auto-completion.
    # Lowercase only.
    access_control_allow_origin: Header

    www_authenticate: Header
    authorization: Header
    proxy_authenticate: Header
    proxy_authorization: Header

    age: Header
    cache_control: Header
    clear_site_data: Header
    expires: Header
    pragma: Header
    warning: Header

    last_modified: Header
    etag: Header
    if_match: Header
    if_none_match: Header
    if_modified_since: Header
    if_unmodified_since: Header
    vary: Header
    connection: Header
    keep_alive: Header

    x_cache: Header
    via: Header

    accept: Header
    accept_charset: Header
    accept_encoding: Header
    accept_language: Header

    expect: Header

    cookie: Header
    set_cookie: Header

    content_disposition: Header

    content_type: Header

    host: Header
    referer: Header
    referrer_policy: Header
    user_agent: Header

    allow: Header
    server: Header

    transfer_encoding: Header
    date: Header

    from_: Header

    def __init__(self, headers: List[Header]):
        self._headers: List[Header] = headers

    def has(self, header: str) -> bool:
        """
        Safely check if header name is in headers
        """
        return header in self

    def get(self, header: str) -> Optional[Header]:
        """
        Retrieve header from headers if exists
        """
        if header not in self:
            return None
        return self[header]

    def __iter__(self) -> Iterator[Header]:
        for header in self._headers:
            yield header

    def keys(self) -> List[str]:
        """
        Return a list of distinct header name set in headers.
        """
        return list(set([header.name for header in self]))

    def items(self) -> Iterator[Tuple[str, str]]:
        """
        Provide an iterator witch each entry contain a tuple of header name and content.
        """
        for header in self:
            yield header.name, header.content

    def to_dict(self) -> CaseInsensitiveDict:
        """
        Provide a CaseInsensitiveDict output of current headers. This output type has been borrowed from psf/requests.
        If one header appear multiple times, if would be concatenated into the same value, separated by comma.
        Be aware that this repr could lead to mistake.
        """
        dict_headers = CaseInsensitiveDict()

        for header in self:
            header_name_no_underscore = header.name.replace("_", "-")
            if header_name_no_underscore not in dict_headers:
                dict_headers[header_name_no_underscore] = header.content
                continue
            dict_headers[header_name_no_underscore] += ", " + header.content

        return dict_headers

    def __deepcopy__(self, memodict: Dict) -> "Headers":
        return Headers(deepcopy(self._headers))

    def __delitem__(self, key: str) -> NoReturn:
        """
        Remove all matching header named after called key.
           >>> del headers['content-type']
        """
        key = Header.normalize_name(key)
        to_be_removed = []

        if key not in self:
            raise KeyError(
                "'{item}' header is not defined in headers.".format(item=key)
            )

        for header in self:
            if header.normalized_name == key:
                to_be_removed.append(header)

        for header in to_be_removed:
            self._headers.remove(header)

    def __setitem__(self, key: str, value: str) -> NoReturn:
        """
        Set header using the bracket syntax. This operation would remove any existing header named after the key.
        """
        if key in self:
            del self[key]

        self._headers.append(Header(key, value))

    def __delattr__(self, item: str) -> NoReturn:
        """
        Remove header using the property notation.
           >>> del headers.content_type
        """
        if item not in self:
            raise AttributeError(
                "'{item}' header is not defined in headers.".format(item=item)
            )

        del self[item]

    def __setattr__(self, key: str, value: str) -> NoReturn:
        """
        Set header like it is a property/member. This operation would remove any existing header named after the key.
        """
        if key == "_headers":
            return super().__setattr__(key, value)

        self[key] = value

    def __eq__(self, other: "Headers") -> bool:
        """
        Basically compare if one Headers instance equal to another. Order does not matter and instance length matter.
        """
        if len(other) != len(self):
            return False

        for header in self:
            if header not in other:
                return False

        return True

    def __len__(self) -> int:
        """
        Return number of headers. If one header appear multiple time, it is not reduced to one in this count.
        """
        return len(self._headers)

    def __str__(self) -> str:
        """
        Just calling __repr__ of self. see __repr__.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Non-ambiguous representation of an Headers instance.
        """
        return "\n".join([header.__repr__() for header in self])

    def __add__(self, other: Header) -> "Headers":
        """
        Add using syntax c = a + b. The result is a newly created object.
        """
        headers = deepcopy(self)
        headers += other

        return headers

    def __sub__(self, other: Union[Header, str]) -> "Headers":
        """
        Subtract using syntax c = a - b. The result is a newly created object.
        """
        headers = deepcopy(self)
        headers -= other

        return headers

    def __iadd__(self, other: Header) -> "Headers":
        """
        Inline add, using operator '+'. It is only possible to add to it another Header object.
        """
        if isinstance(other, Header):
            self._headers.append(other)
            return self

        raise TypeError(
            'Cannot add type "{type_}" to Headers.'.format(type_=str(type(other)))
        )

    def __isub__(self, other: Union[Header, str]) -> "Headers":
        """
        Inline subtract, using operator '-'. If a str is subtracted to it,
        would be looking for header named like provided str.
        eg.
           >>> headers -= 'Set-Cookies'
        Would remove any entries named 'Set-Cookies'.
        """
        if isinstance(other, str):
            other_normalized = Header.normalize_name(other)
            to_be_removed = list()

            for header in self:
                if other_normalized == header.normalized_name:
                    to_be_removed.append(header)

            for header in to_be_removed:
                self._headers.remove(header)

            return self

        if isinstance(other, Header):
            if other in self:
                self._headers.remove(other)
                return self

        raise TypeError(
            'Cannot subtract type "{type_}" to Headers.'.format(type_=str(type(other)))
        )

    def __getitem__(self, item: Union[str, int]) -> Union[Header, List[Header]]:
        """
        Extract header using the bracket syntax, dict-like. The result is either a single Header or a list of Header.
        """
        item = Header.normalize_name(item)

        if item not in self:
            raise KeyError(
                "'{item}' header is not defined in headers.".format(item=item)
            )

        headers: List[Header] = list()

        for header in self._headers:
            if header.normalized_name == item:
                headers.append(header)

        return headers if len(headers) > 1 else headers.pop()

    def __getattr__(self, item: str) -> Union[Header, List[Header]]:
        """
        Where the magic happen, every header are accessible via the property notation.
        The result is either a single Header or a list of Header.
        eg.
           >>> headers.content_type
        """
        if item[0] == "_":
            item = item[1:]

        if item.lower() in RESERVED_KEYWORD:
            item = item[:-1]

        if item not in self:
            raise AttributeError(
                "'{item}' header is not defined in headers.".format(item=item)
            )

        return self[item]

    def __contains__(self, item: Union[Header, str]) -> bool:
        """
        This method will allow you to test if a header, based on it's string name, is present or not in headers.
        You could also use a Header object to verify it's presence.
        """
        item = Header.normalize_name(item) if isinstance(item, str) else item

        for header in self:
            if isinstance(item, str) and header.normalized_name == item:
                return True
            if isinstance(item, Header) and header == item:
                return True

        return False

    def __dir__(self) -> Iterable[str]:
        """
        Provide a better auto-completion when using python interpreter. We are feeding __dir__ so Python can be aware
        of what properties are callable. In other word, more precise auto-completion when not using IDE.
        """
        return super().__dir__() + list(
            set([header.normalized_name for header in self])
        )


def parse_it(raw_headers: Any) -> Headers:
    """
    Just decode anything that could contain headers. That simple PERIOD.
    """

    headers: Optional[List[Tuple[str, Any]]] = None

    if isinstance(raw_headers, str):
        headers = HeaderParser().parsestr(raw_headers, headersonly=True).items()
    elif isinstance(raw_headers, bytes) or isinstance(raw_headers, IOBase):
        buf: BytesIO = (
            BytesIO(raw_headers) if not hasattr(raw_headers, "closed") else raw_headers
        )
        headers = BytesHeaderParser().parse(buf, headersonly=True).items()
    elif isinstance(raw_headers, Mapping):
        headers = raw_headers.items()
    else:
        r = findall(r"<class '([a-zA-Z0-9.]+)'>", str(type(raw_headers)))

        if r and r[0] == "requests.models.Response":
            headers = []
            for header_name in raw_headers.raw.headers:
                for header_content in raw_headers.raw.headers.getlist(header_name):
                    headers.append((header_name, header_content))

    if headers is None:
        raise TypeError(
            "Cannot parse type {type_} as it is not supported by kiss-header.".format(
                type_=type(raw_headers)
            )
        )

    revised_headers = list()

    for head, content in headers:
        revised_content: str = str()

        for partial, partial_encoding in decode_header(content):
            if isinstance(partial, str):
                revised_content += partial
            if isinstance(partial, bytes):
                revised_content += partial.decode(
                    partial_encoding if partial_encoding is not None else "utf-8",
                    errors="ignore",
                )

        revised_headers.append((head, revised_content))

    # Sometime raw content does not begin with headers. If that is the case, search for the next line.
    if (
        len(revised_headers) == 0
        and len(raw_headers) > 0
        and (isinstance(raw_headers, bytes) or isinstance(raw_headers, str))
    ):
        next_iter = raw_headers.split(
            b"\n" if isinstance(raw_headers, bytes) else "\n", maxsplit=1
        )

        if len(next_iter) >= 2:
            return parse_it(next_iter[-1])

    return Headers([Header(head, content) for head, content in revised_headers])
