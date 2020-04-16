from copy import deepcopy
from json import dumps
from re import IGNORECASE, escape, findall
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    Union,
)

from kiss_headers.structures import CaseInsensitiveDict
from kiss_headers.utils import (
    header_content_split,
    header_name_to_class,
    header_strip,
    is_legal_header_name,
    normalize_str,
    prettify_header_name,
    unquote,
)

RESERVED_KEYWORD: List[str] = [
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

OUTPUT_LOCK_TYPE: bool = False


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
    filename: str

    def __init__(self, name: str, content: str):
        """
        :param name: The name of the header, should contain only ASCII characters with no spaces in it.
        :param content: Initial content associated with the header.
        """
        if not is_legal_header_name(name):
            raise ValueError(
                f"'{name}' is not a valid header name. Cannot proceed with it."
            )

        self._name: str = name
        self._normalized_name: str = normalize_str(self._name)
        self._pretty_name: str = prettify_header_name(self._name)
        self._content: str = content

        self._members: List[str] = [
            el.lstrip() for el in header_content_split(self._content, ";")
        ]

        self._not_valued_attrs: List[str] = list()
        self._valued_attrs: MutableMapping[str, Union[str, List[str]]] = dict()
        self._valued_attrs_normalized: MutableMapping[
            str, Union[str, List[str]]
        ] = dict()

        for member in self._members:
            if member == "":
                continue

            if "=" in member:
                key, value = tuple(member.split("=", maxsplit=1))

                # avoid confusing base64 look alike single value for (key, value)
                if value.count("=") == len(value) or len(value) == 0 or " " in key:
                    self._not_valued_attrs.append(unquote(member))
                    continue

                if key not in self._valued_attrs:
                    self._valued_attrs[key] = value
                else:
                    if isinstance(self._valued_attrs[key], str):
                        self._valued_attrs[key] = [self._valued_attrs[key], value]  # type: ignore
                    else:
                        self._valued_attrs[key].append(value)  # type: ignore

                self._valued_attrs_normalized[normalize_str(key)] = self._valued_attrs[
                    key
                ]
                continue

            self._not_valued_attrs.append(unquote(member))

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
    def pretty_name(self) -> str:
        """
        Output a prettified name of the header. First letter capitalized of each word.
        """
        return self._pretty_name

    @property
    def content(self) -> str:
        """
        Output associated content to header as it was captured initially.
        >>> header = Header("ETag", '"33a64df551425fcc55e4d42a148795d9f25f89d4"')
        >>> header.content
        '33a64df551425fcc55e4d42a148795d9f25f89d4'
        """
        # Unquote content if their is only one value/attribute in it. Like the ETag header.
        if len(self.attrs) == 1:
            return unquote(self._content)

        return self._content

    def __lt__(self, other: object) -> bool:
        """
        This method is only implemented to make sorted work with Header.
        The lower than is based on alphabetical order using the header name.
        >>> Header("A", "") < Header("Z", "")
        True
        """
        if not isinstance(other, Header):
            raise NotImplementedError
        return self.normalized_name < other.normalized_name

    def __gt__(self, other: object) -> bool:
        """
        This method is only implemented to make sorted work with Header.
        The greater than is based on alphabetical order using the header name.
        >>> Header("A", "") > Header("Z", "")
        False
        """
        if not isinstance(other, Header):
            raise NotImplementedError
        return self.normalized_name > other.normalized_name

    def __deepcopy__(self, memodict: Dict) -> "Header":
        """Simply provide a deepcopy of an Header object. Pointer/Reference free of the initial reference."""
        return Header(deepcopy(self.name), deepcopy(self.content))

    def __iadd__(self, other: Union[str, "Header"]) -> "Header":
        """
        Allow you to assign-add any string to an Header instance. The string will be a new member of your header.
        >>> header = Header("X-Hello-World", "")
        >>> repr(header)
        'X-Hello-World: '
        >>> header += "preload"
        >>> repr(header)
        'X-Hello-World: preload'
        >>> header += "inclSubDomain"
        >>> repr(header)
        'X-Hello-World: preload; inclSubDomain'
        >>> header += 1
        Traceback (most recent call last):
          ...
        TypeError: Cannot assign-add with type <class 'int'> to an Header.
        """
        if not isinstance(other, str):
            raise TypeError(
                "Cannot assign-add with type {type_} to an Header.".format(
                    type_=type(other)
                )
            )

        self._not_valued_attrs.append(other)

        self._content += "; " + other if self._content.lstrip() != "" else other

        return self

    def __add__(self, other: Union[str, "Header"]) -> Union["Header", "Headers"]:
        """
        This implementation permit to add either a string or a Header to your Header instance.
        When you add string to your Header instance, it will create another instance with a new
        member in it using the string; see iadd doc about it. But when its another Header the result is an Headers
        object containing both Header object.
        >>> headers = Header("X-Hello-World", "1") + Header("Content-Type", "happiness=True")
        >>> len(headers)
        2
        >>> headers.keys()
        ['X-Hello-World', 'Content-Type']
        >>> Header("Content-Type", "happiness=True") + 1
        Traceback (most recent call last):
          ...
        TypeError: Cannot make addition with type <class 'int'> to an Header.
        """
        if not isinstance(other, str) and not isinstance(other, Header):
            raise TypeError(
                "Cannot make addition with type {type_} to an Header.".format(
                    type_=type(other)
                )
            )

        if isinstance(other, Header):

            headers = Headers()
            headers += self
            headers += other

            return headers

        header_ = deepcopy(self)
        header_ += other

        return header_

    def __isub__(self, other: str) -> "Header":
        """
        This method should allow you to remove attribute or member from header.
        """
        if not isinstance(other, str):
            raise TypeError(
                "You cannot subtract {type_} to an Header.".format(
                    type_=str(type(other))
                )
            )

        if other not in self:
            raise ValueError(
                "You cannot subtract '{element}' from '{header_name}' Header because its not there.".format(
                    element=other, header_name=self.pretty_name
                )
            )

        other = normalize_str(other)

        if other in self._valued_attrs_normalized:
            del self[other]

        if other in self._not_valued_attrs:
            self._not_valued_attrs.remove(other)
            while True:
                try:
                    self._not_valued_attrs.remove(other)
                except ValueError:
                    break
            for elem in findall(
                r"{member_name}(?=[;\n])".format(member_name=escape(other)),
                self._content + "\n",
                IGNORECASE,
            ):
                self._content = header_strip(self._content, elem)

        return self

    def __sub__(self, other: str) -> "Header":
        """
        This method should allow you to remove attribute or member from header.
        """
        header_ = deepcopy(self)
        header_ -= other

        return header_

    def __setattr__(self, key: str, value: str) -> None:
        """
        Set attribute on header using the property notation.
        """

        # Avoid conflict with __init__ sequence of Header
        if key in [
            "_name",
            "_normalized_name",
            "_pretty_name",
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

    def __setitem__(self, key: str, value: str) -> None:
        """
        Set an attribute bracket syntax like. This will erase previously set attribute named after the key.
        Any value that are not a str are casted to str.
        """
        key_normalized = normalize_str(key)

        if key in self:
            del self[key]
        if not isinstance(value, str):
            value = str(value)

        self._valued_attrs[key] = value
        self._valued_attrs_normalized[key_normalized] = self._valued_attrs[key]

        self._content += '{semi_colon_r}{key}="{value}"'.format(
            key=key,
            value=value,
            semi_colon_r="; " if self._content.lstrip() != "" else "",
        )

    def __delitem__(self, key: str) -> None:
        """
        Remove any attribute named after the key in header using the bracket syntax.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Allow", "POST")
        >>> str(headers.content_type)
        'text/html; charset=UTF-8'
        >>> del headers.content_type['charset']
        >>> str(headers.content_type)
        'text/html'
        """
        key_normalized = normalize_str(key)

        if key_normalized not in self._valued_attrs_normalized:
            raise KeyError(
                "'{item}' attribute is not defined within '{header}' header.".format(
                    item=key, header=self.name
                )
            )

        del self._valued_attrs_normalized[key]
        not_normalized_keys = self._valued_attrs.keys()

        for key_ in not_normalized_keys:
            if normalize_str(key_) == key_normalized:
                del self._valued_attrs[key_]
                break

        for elem in findall(
            r"{key_name}=.*?(?=[;\n])".format(key_name=escape(key)),
            self._content + "\n",
            IGNORECASE,
        ):
            self._content = header_strip(self._content, elem)

    def __delattr__(self, item: str) -> None:
        """
        Remove any attribute named after the key in header using the property notation.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Vary", "Content-Type")
        >>> repr(headers.content_type)
        'Content-Type: text/html; charset=UTF-8'
        >>> del headers.content_type.charset
        >>> repr(headers.content_type)
        'Content-Type: text/html'
        """
        item = normalize_str(item)

        if item not in self._valued_attrs_normalized:
            raise AttributeError(
                "'{item}' attribute is not defined within '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        del self[item]

    def __iter__(self) -> Iterator[Tuple[str, Optional[Union[str, List[str]]]]]:
        """Provide a way to iter over an Header object. This will yield a Tuple of key, value.
        Value would be None if the key is a member without associated value."""
        for key in self._valued_attrs:
            yield key, self[key]
        for adjective in self._not_valued_attrs:
            yield adjective, None

    def __eq__(self, other: object) -> bool:
        """
        Verify equality between a Header object and str or another Header object.
        If testing against str, the first thing is to match it to raw content, if not equal verify if not in members.
        """
        if isinstance(other, str):
            return self.content == other or other in self._not_valued_attrs
        if isinstance(other, Header):
            if (
                self.normalized_name == other.normalized_name
                and len(self._not_valued_attrs) == len(other._not_valued_attrs)
                and len(self._valued_attrs) == len(other._valued_attrs)
            ):
                for adjective in self._not_valued_attrs:
                    if adjective not in other._not_valued_attrs:
                        return False
                for key in self._valued_attrs:
                    if key not in other or self[key] != other[key]:
                        return False
                return True
            return False
        raise NotImplementedError(
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

    def __bytes__(self) -> bytes:
        """
        Provide a bytes repr of header. Warning, this output does not have a RC at the end. Any error encountered
        in encoder would be treated by 'surrogateescape' clause.
        """
        return repr(self).encode("utf-8", errors="surrogateescape")

    def __dir__(self) -> Iterable[str]:
        """
        Provide a better auto-completion when using python interpreter. We are feeding __dir__ so Python can be aware
        of what properties are callable. In other word, more precise auto-completion when not using IDE.
        """
        return list(super().__dir__()) + list(self._valued_attrs_normalized.keys())

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

    def get(self, attr: str) -> Optional[Union[str, List[str]]]:
        """
        Retrieve associated value of an attribute.
        """
        if attr not in self._valued_attrs:
            return None
        return self._valued_attrs[attr]

    def __getitem__(self, item: Union[str]) -> Union[str, List[str]]:
        """
        This method will allow you to retrieve attribute value using the bracket syntax, list-like.
        """
        normalized_item = normalize_str(item)

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

        if OUTPUT_LOCK_TYPE and not isinstance(value, list):
            value = [value]

        return (
            unquote(value)
            if not isinstance(value, list)
            else [unquote(v) for v in value]
        )

    def __getattr__(self, item: str) -> Union[str, List[str]]:
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
            and normalize_str(item) not in self._valued_attrs_normalized
        ):
            raise AttributeError(
                "'{item}' attribute is not defined within '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        return self[item]

    def __contains__(self, item: str) -> bool:
        """
        Verify if a string match a member or an attribute name of an Header.
        """
        if item in self.attrs:
            return True
        item = normalize_str(item)
        for attr in self.attrs:
            target = normalize_str(attr)
            if item == target or item in target.split(","):
                return True
        return False


class Headers(object):
    """
    Object oriented representation for Headers. Contains a list of Header with some level of abstraction.
    Combine advantages of dict, CaseInsensibleDict and native objects.
    Headers does not inherit of the Mapping type, but it does borrow some concept from it.
    """

    # Most common headers that you may or may not find. This should be appreciated when having auto-completion.
    # Lowercase only.
    access_control_allow_origin: Union[Header, List[Header]]

    www_authenticate: Union[Header, List[Header]]
    authorization: Union[Header, List[Header]]
    proxy_authenticate: Union[Header, List[Header]]
    proxy_authorization: Union[Header, List[Header]]

    alt_svc: Union[Header, List[Header]]

    age: Union[Header, List[Header]]
    cache_control: Union[Header, List[Header]]
    clear_site_data: Union[Header, List[Header]]
    expires: Union[Header, List[Header]]
    pragma: Union[Header, List[Header]]
    warning: Union[Header, List[Header]]

    last_modified: Union[Header, List[Header]]
    etag: Union[Header, List[Header]]
    if_match: Union[Header, List[Header]]
    if_none_match: Union[Header, List[Header]]
    if_modified_since: Union[Header, List[Header]]
    if_unmodified_since: Union[Header, List[Header]]
    vary: Union[Header, List[Header]]
    connection: Union[Header, List[Header]]
    keep_alive: Union[Header, List[Header]]

    x_cache: Union[Header, List[Header]]
    via: Union[Header, List[Header]]

    accept: Union[Header, List[Header]]
    accept_charset: Union[Header, List[Header]]
    accept_encoding: Union[Header, List[Header]]
    accept_language: Union[Header, List[Header]]

    expect: Union[Header, List[Header]]

    cookie: Union[Header, List[Header]]
    set_cookie: Union[Header, List[Header]]

    content_disposition: Union[Header, List[Header]]

    content_type: Union[Header, List[Header]]

    host: Union[Header, List[Header]]
    referer: Union[Header, List[Header]]
    referrer_policy: Union[Header, List[Header]]
    user_agent: Union[Header, List[Header]]

    allow: Union[Header, List[Header]]
    server: Union[Header, List[Header]]

    transfer_encoding: Union[Header, List[Header]]
    date: Union[Header, List[Header]]

    from_: Union[Header, List[Header]]

    def __init__(self, *headers: Union[List[Header], Header]):
        """
        :param headers: Initial list of header. Can be empty.
        """
        self._headers: List[Header] = headers[0] if len(headers) == 1 and isinstance(
            headers[0], list
        ) else list(
            headers  # type: ignore
        )

    def has(self, header: str) -> bool:
        """
        Safely check if header name is in headers
        """
        return header in self

    def get(self, header: str) -> Optional[Union[Header, List[Header]]]:
        """
        Retrieve header from headers if exists
        """
        if header not in self:
            return None
        return self[header]

    def __iter__(self) -> Iterator[Header]:
        """
        Act like a list by yielding one element at a time. Each element is a Header object.
        """
        for header in self._headers:
            yield header

    def keys(self) -> List[str]:
        """
        Return a list of distinct header name set in headers.
        Be aware that it wont return a typing.KeysView
        """
        keys = list()

        # I decided to go with this to conserve order of appearance in list.
        for header in self:
            if header.name not in keys:
                keys.append(header.name)

        return keys

    def values(self) -> NotImplemented:
        """
        I choose not to implement values() on Headers as it would bring more confusion..
        Either we make it the same len as keys() or we don't. Either way don't please me. Hope to ear from the
        community about this.
        """
        return NotImplemented

    def items(self) -> List[Tuple[str, str]]:
        """
        Provide an iterator witch each entry contain a tuple of header name and content.
        This wont return a ItemView.
        >>> headers = Header("X-Hello-World", "1") + Header("Content-Type", "happiness=True") + Header("Content-Type", "happiness=False")
        >>> headers.items()
        [('X-Hello-World', '1'), ('Content-Type', 'happiness=True'), ('Content-Type', 'happiness=False')]
        """
        items: List[Tuple[str, str]] = []

        for header in self:
            items.append((header.name, header.content))

        return items

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
        """
        Just provide a deepcopy of current Headers object. Pointer/reference free of the current instance.
        """
        return Headers(deepcopy(self._headers))

    def __delitem__(self, key: str) -> None:
        """
        Remove all matching header named after called key.
        >>> headers = Header("Content-Type", "text/html") + Header("Allow", "POST")
        >>> headers.has("Content-Type")
        True
        >>> del headers['content-type']
        >>> headers.has("Content-Type")
        False
        """
        key = normalize_str(key)
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

    def __setitem__(self, key: str, value: str) -> None:
        """
        Set header using the bracket syntax. This operation would remove any existing header named after the key.
        """
        if not isinstance(value, str):
            raise TypeError(
                "Cannot assign header '{key}' using type {type_} to headers.".format(
                    key=key, type_=type(value)
                )
            )
        if key in self:
            del self[key]

        self._headers.append(Header(key, value))

    def __delattr__(self, item: str) -> None:
        """
        Remove header using the property notation.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Vary", "Content-Type")
        >>> headers.has("Content-Type")
        True
        >>> del headers.content_type
        >>> headers.has("Content-Type")
        False
        """
        if item not in self:
            raise AttributeError(
                "'{item}' header is not defined in headers.".format(item=item)
            )

        del self[item]

    def __setattr__(self, key: str, value: str) -> None:
        """
        Set header like it is a property/member. This operation would remove any existing header named after the key.
        """
        if key == "_headers":
            return super().__setattr__(key, value)

        self[key] = value

    def __eq__(self, other: object) -> bool:
        """
        Basically compare if one Headers instance equal to another. Order does not matter and instance length matter.
        """
        if not isinstance(other, Headers):
            raise NotImplementedError(
                "Cannot compare type {type_} to an Header. Use str or Header.".format(
                    type_=type(other)
                )
            )
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
        Non-ambiguous representation of an Headers instance. Using CRLF as described in rfc2616.
        The repr of Headers will not end with blank(s) line(s). You have to add it yourself, depending on your needs.
        """
        result: List[str] = []

        for header_name in self.keys():

            r = self.get(header_name)

            if not r:
                raise LookupError(
                    f"This should not happen. Cannot get '{header_name}' from headers when keys() said its there."
                )

            target_subclass: Optional[Type] = None

            try:
                target_subclass = (
                    header_name_to_class(header_name, Header.__subclasses__()[0])
                    if Header.__subclasses__()
                    else None
                )
            except TypeError:
                pass

            if (
                isinstance(r, list)
                and len(r) > 1
                and target_subclass
                and hasattr(target_subclass, "__squash__")
                and target_subclass.__squash__ is True
            ):
                result.append(
                    "{name}: {content}".format(
                        name=header_name, content=", ".join([el.content for el in r])
                    )
                )
            elif isinstance(r, list):
                for el in r:
                    result.append(repr(el))
            else:
                result.append(repr(r))

        return "\r\n".join(result)

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
        Would remove any entries named 'Set-Cookies'. eg :
        >>> headers = Header("Set-Cookies", "HELLO=WORLD") + Header("Allow", "POST")
        >>> headers.has("Set-Cookies")
        True
        >>> headers -= 'Set-Cookies'
        >>> headers.has("Set-Cookies")
        False
        """
        if isinstance(other, str):
            other_normalized = normalize_str(other)
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
        if isinstance(item, int):
            return self._headers[item]

        item = normalize_str(item)

        if item not in self:
            raise KeyError(
                "'{item}' header is not defined in headers.".format(item=item)
            )

        headers: List[Header] = list()

        for header in self._headers:
            if header.normalized_name == item:
                headers.append(header)

        return headers if len(headers) > 1 or OUTPUT_LOCK_TYPE else headers.pop()

    def __getattr__(self, item: str) -> Union[Header, List[Header]]:
        """
        Where the magic happen, every header are accessible via the property notation.
        The result is either a single Header or a list of Header.
        eg.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Allow", "POST")
        >>> headers.content_type
        Content-Type: text/html; charset=UTF-8
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

    def to_json(self) -> str:
        """
        Provide a JSON representation of Headers
        """
        return dumps(self.items())

    def __bytes__(self) -> bytes:
        """
        Will encode your headers as bytes using utf-8 charset encoding. Any error encountered in encoder would be
        treated by the 'surrogateescape' clause.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Allow", "POST")
        >>> bytes(headers)
        b'Content-Type: text/html; charset=UTF-8\\r\\nAllow: POST'
        """
        return repr(self).encode("utf-8", errors="surrogateescape")

    def __reversed__(self) -> "Headers":
        list_of_headers: List[Header] = deepcopy(self._headers)
        list_of_headers.reverse()

        return Headers(list_of_headers)

    def __contains__(self, item: Union[Header, str]) -> bool:
        """
        This method will allow you to test if a header, based on it's string name, is present or not in headers.
        You could also use a Header object to verify it's presence.
        """
        item = normalize_str(item) if isinstance(item, str) else item

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
        return list(super().__dir__()) + list(
            set([header.normalized_name for header in self])
        )


def lock_output_type(lock: bool = True) -> None:
    """
    This method will restrict type entropy by always returning a List[Header] instead of Union[Header, List[Header]]
    """
    global OUTPUT_LOCK_TYPE
    OUTPUT_LOCK_TYPE = lock
