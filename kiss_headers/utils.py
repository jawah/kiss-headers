from email.parser import HeaderParser, BytesHeaderParser
from io import BytesIO, IOBase
from typing import List, Optional, Union, Dict, Mapping, Iterator, Tuple, Iterable
from email.header import decode_header
from cached_property import cached_property


class Header(object):

    charset: Union['Header', str]
    format: Union['Header', str]
    boundary: Union['Header', str]
    expires: Union['Header', str]
    timeout: Union['Header', str]
    max: Union['Header', str]
    path: Union['Header', str]

    def __init__(self, head: str, content: str):

        self._head: str = head
        self._content: str = content

        self._members: List[str] = [el.lstrip() for el in self._content.split(';')]

        self._not_valued_attrs: List[str] = list()
        self._valued_attrs: Dict[str, Union[str, List[str]]] = dict()
        self._valued_attrs_normalized: Dict[str, Union[str, List[str]]] = dict()

        for member in self._members:
            if '=' in member:
                key, value = tuple(member.split('=', maxsplit=1))

                # avoid confusing base64 look alike single value for (key, value)
                if value.count('=') == len(value) or len(value) == 0:
                    self._not_valued_attrs.append(member)
                    continue

                if key not in self._valued_attrs:
                    self._valued_attrs[key] = value
                else:
                    if isinstance(self._valued_attrs[key], str):
                        self._valued_attrs[key] = [self._valued_attrs[key], value]
                    else:
                        self._valued_attrs[key].append(value)

                self._valued_attrs_normalized[Header.normalize_name(key)] = self._valued_attrs[key]
                continue

            self._not_valued_attrs.append(member)

    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Normalize header name or attribute name by applying lowercase and replacing '-' to '_'.
        """
        return name.lower().replace('-', '_')

    @property
    def name(self) -> str:
        """
        Output the original header name as it was captured initially
        """
        return self._head

    @cached_property
    def normalized_name(self) -> str:
        """
        Output header name but normalized, lower case and '-' character become '_'.
        """
        return Header.normalize_name(self.name)

    @property
    def content(self) -> str:
        """
        Output associated content to header as it was captured initially.
        """
        if len(self.attrs) == 1:
            if self._content.startswith('"') and self._content.endswith('"'):
                return self._content[1:-1]

        return self._content

    def __iter__(self) -> Iterator[Tuple[str, Optional[str]]]:
        for key, value in self._valued_attrs.items():
            yield key, self[key]
        for adjective in self._not_valued_attrs:
            yield adjective, None

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.content == other or other in self._not_valued_attrs
        if isinstance(other, Header):
            return self.normalized_name == other.normalized_name and self.content == other.content
        raise TypeError('Cannot compare type {type_} to an Header. Use str or Header.'.format(type_=type(other)))

    def __str__(self) -> str:
        return self._content

    def __repr__(self) -> str:
        return "{head}: {content}".format(head=self._head, content=self._content)

    def __dir__(self) -> Iterable[str]:
        return super().__dir__() + list(self._valued_attrs_normalized.keys())

    @property
    def attrs(self) -> List[str]:
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

    def __getitem__(self, item: str) -> Union[str, List[str]]:
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
                "'{item}' attribute is not defined within '{header}' header.".format(item=item, header=self.name))

        # Unquote value if necessary
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            return value[1:-1]

        return value

    def __getattr__(self, item) -> str:
        """
        All the magic happen here, this method should be invoked when trying to call (not declared) properties.
        For instance, calling self.charset should end up here and be replaced by self['charset'].
        """
        if item not in self._valued_attrs and Header.normalize_name(item) not in self._valued_attrs_normalized:
            raise AttributeError("'{item}' attribute is not defined within '{header}' header.".format(item=item, header=self.name))

        return self[item]

    def __contains__(self, item: str) -> bool:
        if item in self.attrs:
            return True
        for attr in self.attrs:
            if Header.normalize_name(item) == Header.normalize_name(attr):
                return True
        return False


class Headers:

    """
    Most common headers that you may or may not find. This should be appreciated when having auto-completion.
    """
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

    def __iter__(self):
        for header in self._headers:
            yield header

    def to_dict(self) -> Dict[str, str]:
        """
        Provide a dict output of current headers
        """
        return dict(
            [
                (header.name, header.content) for header in self
            ]
        )

    def __eq__(self, other: 'Headers') -> bool:
        if len(other) != len(self):
            return False

        for header in self:
            if header not in other:
                return False

        return True

    def __len__(self) -> int:
        return len(self._headers)

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return '\n'.join([header.__repr__() for header in self])

    def __getitem__(self, item: str) -> Union[Header, List[Header]]:
        item = Header.normalize_name(item)

        if item not in self:
            raise KeyError("'{item}' header is not defined in headers.".format(item=item))

        headers: List[Header] = list()

        for header in self._headers:
            if header.normalized_name == item:
                headers.append(header)

        return headers if len(headers) > 1 else headers.pop()

    def __getattr__(self, item: str) -> Union[Header, List[Header]]:
        if item not in self:
            raise AttributeError("'{item}' header is not defined in headers.".format(item=item))

        return self[item]

    def __contains__(self, item: Union[Header, str]) -> bool:
        item = Header.normalize_name(item) if isinstance(item, str) else item

        for header in self:
            if isinstance(item, str) and header.normalized_name == item:
                return True
            if isinstance(item, Header) and header == item:
                return True

        return False

    def __dir__(self) -> Iterable[str]:
        return super().__dir__() + list(set([header.normalized_name for header in self]))


def parse_it(raw_headers: Union[bytes, str, Dict[str, str], IOBase]) -> Headers:
    """
    Just decode anything that could represent headers. That simple PERIOD.
    """
    if isinstance(raw_headers, str):
        headers = HeaderParser().parsestr(raw_headers, headersonly=True).items()
    elif isinstance(raw_headers, bytes) or isinstance(raw_headers, IOBase):
        buf = BytesIO(raw_headers) if not hasattr(raw_headers, 'closed') else raw_headers
        headers = BytesHeaderParser().parse(buf, headersonly=True).items()
    elif isinstance(raw_headers, Mapping):
        headers = raw_headers.items()
    else:
        raise TypeError('Cannot parse type {type_} as it is not supported by kiss-header.'.format(type_=type(raw_headers)))

    revised_headers = list()

    for head, content in headers:
        revised_content: str = str()

        for partial, partial_encoding in decode_header(content):
            if isinstance(partial, str):
                revised_content += partial
            if isinstance(partial, bytes):
                revised_content += partial.decode(partial_encoding if partial_encoding is not None else 'utf-8', errors='ignore')

        revised_headers.append((head, revised_content))

    return Headers([Header(head, content) for head, content in revised_headers])
