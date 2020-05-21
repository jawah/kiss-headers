from copy import deepcopy
from json import dumps
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Type, Union

from kiss_headers.structures import AttributeBag, CaseInsensitiveDict
from kiss_headers.utils import (
    extract_comments,
    header_content_split,
    header_name_to_class,
    is_legal_header_name,
    normalize_list,
    normalize_str,
    prettify_header_name,
    unfold,
    unpack_protected_keyword,
    unquote,
)

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

        self._members: List[str] = header_content_split(self._content, ";")

        self._attrs: Attributes = Attributes(self._members)

    @property
    def name(self) -> str:
        """
        Output the original header name as it was captured initially.
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
        Output a prettified name of the header. The first letter capitalized on each word.
        """
        return self._pretty_name

    @property
    def content(self) -> str:
        """
        Output associated content to the header as it was captured initially.
        >>> header = Header("ETag", '"33a64df551425fcc55e4d42a148795d9f25f89d4"')
        >>> header.content
        '33a64df551425fcc55e4d42a148795d9f25f89d4'
        """
        # Unquote content if there is only one value/attribute in it. Like the ETag header.
        if len(self.attrs) == 1:
            return unquote(self._content)

        return self._content

    @property
    def unfolded_content(self) -> str:
        """Output unfolded associated content to the header. Meaning that every LF + n space(s) would be properly
        replaced."""
        return unfold(self.content)

    @property
    def comments(self) -> List[str]:
        """Retrieve comments in header content."""
        return extract_comments(self.content)

    def __lt__(self, other: object) -> bool:
        """
        This method is only implemented to make sorted work with Header.
        The lower than is based on alphabetical order using the header name.
        >>> Header("A", "") < Header("Z", "")
        True
        """
        if not isinstance(other, Header):
            raise NotImplementedError  # pragma: no cover
        return self.normalized_name < other.normalized_name

    def __gt__(self, other: object) -> bool:
        """
        This method is only implemented to make sorted work with Header.
        The greater than is based on alphabetical order using the header name.
        >>> Header("A", "") > Header("Z", "")
        False
        """
        if not isinstance(other, Header):
            raise NotImplementedError  # pragma: no cover
        return self.normalized_name > other.normalized_name

    def __deepcopy__(self, memodict: Dict) -> "Header":
        """Simply provide a deepcopy of a Header object. Pointer/Reference is free of the initial reference."""
        return Header(deepcopy(self.name), deepcopy(self.content))

    def pop(
        self, __index: Union[int, str] = -1
    ) -> Tuple[str, Optional[Union[str, List[str]]]]:
        """Permit to pop an element from a Header with a given index.
        >>> header = Header("X", "a; b=k; h; h; z=0; y=000")
        >>> header.pop(1)
        ('b', 'k')
        >>> header.pop()
        ('y', '000')
        >>> header.pop('z')
        ('z', '0')
        """

        if isinstance(__index, int):
            __index = __index if __index >= 0 else __index % len(self._attrs)
            key, value = self._attrs[__index]
        elif isinstance(__index, str):
            key, value = __index, self._attrs[__index]  # type: ignore
        else:
            raise ValueError(
                f"Cannot pop from Header using type {type(__index)}."
            )  # pragma: no cover

        self._attrs.remove(key, __index if isinstance(__index, int) else None)
        self._content = str(self._attrs)

        return key, value

    def insert(
        self, __index: int, *__members: str, **__attributes: Optional[str]
    ) -> None:
        """This method allows you to properly insert attributes into a Header instance."""

        __index = __index if __index >= 0 else __index % len(self._attrs)

        for member in __members:
            self._attrs.insert(member, None, __index)
            __index += 1
        for key, value in __attributes.items():
            self._attrs.insert(key, value, __index)
            __index += 1

        self._content = str(self._attrs)
        # We need to update our list of members
        self._members = header_content_split(self._content, ";")

    def __iadd__(self, other: Union[str, "Header"]) -> "Header":
        """
        Allow you to assign-add any string to a Header instance. The string will be a new member of your header.
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

        self._attrs.insert(other, None)
        # No need to rebuild the content completely.
        self._content += "; " + other if self._content.lstrip() != "" else other
        self._members.append(other)

        return self

    def __add__(self, other: Union[str, "Header"]) -> Union["Header", "Headers"]:
        """
        This implementation permits to add either a string or a Header to your Header instance.
        When you add a string to your Header instance, it will create another instance with a new
        member in it using the string; see iadd doc about it. But when its another Header the result is a Headers
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
        This method should allow you to remove attributes or members from the header.
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

        self._attrs.remove(other)
        self._content = str(self._attrs)
        self._members = header_content_split(self._content, ";")

        return self

    def __sub__(self, other: str) -> "Header":
        """
        This method should allow you to remove attributes or members from the header.
        """
        header_ = deepcopy(self)
        header_ -= other

        return header_

    def __setattr__(self, key: str, value: str) -> None:
        """
        Set attribute on header using the property notation.
        """

        # Avoid conflict with __init__ sequence of Header
        if key in {
            "_name",
            "_normalized_name",
            "_pretty_name",
            "_content",
            "_members",
            "_attrs",
            "__class__",
        }:
            return super().__setattr__(key, value)

        key = unpack_protected_keyword(key)

        self[key] = value

    def __setitem__(self, key: str, value: str) -> None:
        """
        Set an attribute bracket syntax like. This will erase the previously set attribute named after the key.
        Any values that are not str are cast to str.
        """

        if key in self:
            del self[key]
        if not isinstance(value, str):
            value = str(value)

        self._attrs.remove(key)
        self._attrs.insert(key, value)

        self._content = str(self._attrs)
        self._members = header_content_split(self._content, ";")

    def __delitem__(self, key: str) -> None:
        """
        Remove any attribute named after the key in the header using the bracket syntax.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Allow", "POST")
        >>> str(headers.content_type)
        'text/html; charset=UTF-8'
        >>> del headers.content_type['charset']
        >>> str(headers.content_type)
        'text/html'
        """

        if normalize_str(key) not in normalize_list(self.valued_attrs):
            raise KeyError(
                "'{item}' attribute is not defined or have at least one value associated within '{header}' header.".format(
                    item=key, header=self.name
                )
            )

        self._attrs.remove(key)
        self._content = str(self._attrs)
        self._members = header_content_split(self._content, ";")

    def __delattr__(self, item: str) -> None:
        """
        Remove any attribute named after the key in the header using the property notation.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Vary", "Content-Type")
        >>> repr(headers.content_type)
        'Content-Type: text/html; charset=UTF-8'
        >>> del headers.content_type.charset
        >>> repr(headers.content_type)
        'Content-Type: text/html'
        """
        item = normalize_str(item)

        if item not in normalize_list(self.valued_attrs):
            raise AttributeError(
                "'{item}' attribute is not defined or have at least one value associated within '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        del self[item]

    def __iter__(self) -> Iterator[Tuple[str, Optional[Union[str, List[str]]]]]:
        """Provide a way to iter over a Header object. This will yield a Tuple of key, value.
        The value would be None if the key is a member without associated value."""
        for i in range(0, len(self._attrs)):
            yield self._attrs[i]  # type: ignore

    def __eq__(self, other: object) -> bool:
        """
        Verify equality between a Header object and str or another Header object.
        If testing against str, the first thing is to match it to raw content, if not equal verify if not in members.
        """
        if isinstance(other, str):
            return self.content == other or other in self._attrs
        if isinstance(other, Header):
            if self.normalized_name == other.normalized_name and len(
                self._attrs
            ) == len(other._attrs):
                return self._attrs == other._attrs
            return False
        raise NotImplementedError(
            "Cannot compare type {type_} to an Header. Use str or Header.".format(
                type_=type(other)
            )
        )

    def __str__(self) -> str:
        """
        Allow casting a single header to a string. Only content would be exposed here.
        """
        return self._content

    def __repr__(self) -> str:
        """
        Unambiguous representation of a single header.
        """
        return "{head}: {content}".format(head=self._name, content=self._content)

    def __bytes__(self) -> bytes:
        """
        Provide a bytes repr of header. Warning, this output does not have an RC at the end. Any error encountered
        in encoder would be treated by 'surrogateescape' clause.
        """
        return repr(self).encode("utf-8", errors="surrogateescape")

    def __dir__(self) -> Iterable[str]:
        """
        Provide a better auto-completion when using a Python interpreter. We are feeding __dir__ so Python can be aware
        of what properties are callable. In other words, more precise auto-completion when not using IDE.
        """
        return list(super().__dir__()) + normalize_list(self._attrs.keys())

    @property
    def attrs(self) -> List[str]:
        """
        List of members or attributes found in provided content. This list is ordered and normalized.
        eg. Content-Type: application/json; charset=utf-8; format=origin
        Would output : ['application/json', 'charset', 'format']
        """
        attrs: List[str] = []

        if len(self._attrs) == 0:
            return attrs

        for i in range(0, len(self._attrs)):
            attr, value = self._attrs[i]
            attrs.append(attr)

        return attrs

    @property
    def valued_attrs(self) -> List[str]:
        """
        List of distinct attributes that have at least one value associated with them. This list is ordered and normalized.
        This property could have been written under the keys() method, but implementing it would interfere with dict()
        cast and the __iter__() method.
        eg. Content-Type: application/json; charset=utf-8; format=origin
        Would output : ['charset', 'format']
        """
        attrs: List[str] = []

        if len(self._attrs) == 0:
            return attrs

        for i in range(0, len(self._attrs)):
            attr, value = self._attrs[i]

            if value is not None and attr not in attrs:
                attrs.append(attr)

        return attrs

    def has(self, attr: str) -> bool:
        """
        Safely check if the current header has an attribute or adjective in it.
        """
        return attr in self

    def get(self, attr: str) -> Optional[Union[str, List[str]]]:
        """
        Retrieve the associated value of an attribute.
        >>> header = Header("Content-Type", "application/json; charset=UTF-8; format=flowed")
        >>> header.charset
        'UTF-8'
        >>> header.ChArSeT
        'UTF-8'
        >>> header.FORMAT
        'flowed'
        >>> header.format
        'flowed'
        """
        if normalize_str(attr) not in normalize_list(self.valued_attrs):
            return None

        return self._attrs[attr]  # type: ignore

    def has_many(self, name: str) -> bool:
        """
        Determine if an attribute name has multiple entries in Header. Detect OneToMany entries.
        >>> header = Header("A", "charset=UTF-8; charset=ASCII; format=flowed")
        >>> header.has_many("charset")
        True
        >>> header.has_many("format")
        False
        """
        if name not in self:
            return False

        r = self[name]

        return isinstance(r, list) and len(r) > 1

    def __getitem__(self, item: Union[str, int]) -> Union[str, List[str]]:
        """
        This method will allow you to retrieve attribute value using the bracket syntax, list-like, or dict-like.
        """
        if isinstance(item, int):
            return (
                self._members[item] if not OUTPUT_LOCK_TYPE else [self._members[item]]
            )

        if normalize_str(item) in normalize_list(self.valued_attrs):
            value = self._attrs[item]  # type: ignore
        else:
            raise KeyError(
                "'{item}' attribute is not defined or does not have at least one value within the '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        if OUTPUT_LOCK_TYPE and isinstance(value, str):
            value = [value]

        return (
            unfold(unquote(value))  # type: ignore
            if isinstance(value, str)
            else [unfold(unquote(v)) for v in value]  # type: ignore
        )

    def __getattr__(self, item: str) -> Union[str, List[str]]:
        """
        All the magic happens here, this method should be invoked when trying to call (not declared) properties.
        For instance, calling self.charset should end up here and be replaced by self['charset'].
        """
        item = unpack_protected_keyword(item)

        if normalize_str(item) not in normalize_list(self.valued_attrs):
            raise AttributeError(
                "'{item}' attribute is not defined or have at least one value within '{header}' header.".format(
                    item=item, header=self.name
                )
            )

        return self[item]

    def __contains__(self, item: str) -> bool:
        """
        Verify if a string matches a member or an attribute-name of a Header.
        """
        if item in self.attrs:
            return True
        item = normalize_str(item)
        for attr in self.attrs:
            target = normalize_str(attr)
            if item == target or item in header_content_split(target, " "):
                return True
        return False


class Headers(object):
    """
    Object-oriented representation for Headers. Contains a list of Header with some level of abstraction.
    Combine advantages of dict, CaseInsensibleDict, list, multi-dict, and native objects.
    Headers do not inherit the Mapping type, but it does borrow some concepts from it.
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
        Safely check if header name is in headers.
        """
        return header in self

    def get(self, header: str) -> Optional[Union[Header, List[Header]]]:
        """
        Retrieve header from headers if exists.
        """
        if header not in self:
            return None
        return self[header]

    def has_many(self, name: str) -> bool:
        """
        Determine if a header name has multiple entries in Headers. Detect OneToMany entries.
        >>> headers = Header("A", "0") + Header("A", "1") + Header("B", "sad")
        >>> headers.has_many("a")
        True
        >>> headers.has_many("b")
        False
        """
        if name not in self:
            return False

        r = self[name]

        return isinstance(r, list) and len(r) > 1

    def __iter__(self) -> Iterator[Header]:
        """
        Act like a list by yielding one element at a time. Each element is a Header object.
        """
        for header in self._headers:
            yield header

    def keys(self) -> List[str]:
        """
        Return a list of distinct header name set in headers.
        Be aware that it won't return a typing.KeysView.
        Also this method allows you to create a case sensitive dict.
        """
        keys = list()

        # I decided to go with this to conserve order of appearance in list.
        for header in self:
            if header.name not in keys:
                keys.append(header.name)

        return keys

    def values(self) -> NotImplemented:
        """
        I choose not to implement values() on Headers as it would bring more confusion...
        Either we make it the same len as keys() or we don't. Either way don't please me. Hope to hear from the
        community about this.
        """
        return NotImplemented

    def items(self) -> List[Tuple[str, str]]:
        """
        Provide a list witch each entry contains a tuple of header name and content.
        This won't return an ItemView as Headers does not inherit from Mapping.
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
        If one header appears multiple times, it would be concatenated into the same value, separated by a comma.
        Be aware that this repr could lead to a mistake. You could also cast a Headers instance to dict() to get a
        case sensitive one. see method keys().
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
        Just provide a deepcopy of the current Headers object. Pointer/reference is free of the current instance.
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
        Warning, if your value contain comma separated entries, it will split it into multiple Header instance.
        >>> headers = Headers()
        >>> headers.content_type = "application/json"
        >>> len(headers)
        1
        >>> headers.accept = "text/html, application/json;q=1.0"
        >>> len(headers)
        3
        """
        if not isinstance(value, str):
            raise TypeError(
                "Cannot assign header '{key}' using type {type_} to headers.".format(
                    key=key, type_=type(value)
                )
            )
        if key in self:
            del self[key]

        # Permit to detect multiple entries.
        if normalize_str(key) != "subject":

            entries: List[str] = header_content_split(value, ",")

            if len(entries) > 1:

                for entry in entries:
                    self._headers.append(Header(key, entry))

                return

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
        Essentially compare if one Headers instance equal to another. The order does not matter and instance length matter.
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
        Return number of headers. If one header appears multiple time, it is not reduced to one in this count.
        """
        return len(self._headers)

    def __str__(self) -> str:
        """
        Just calling __repr__ of self. see __repr__.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Non-ambiguous representation of a Headers instance. Using CRLF as described in rfc2616.
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
        Inline subtract, using the operator '-'. If str is subtracted to it,
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
        Where the magic happens, every header is accessible via the property notation.
        The result is either a single Header or a list of Header.
        eg.
        >>> headers = Header("Content-Type", "text/html; charset=UTF-8") + Header("Allow", "POST") + Header("From", "john-doe@gmail.com")
        >>> headers.content_type
        Content-Type: text/html; charset=UTF-8
        >>> headers.from_
        From: john-doe@gmail.com
        """
        item = unpack_protected_keyword(item)

        if item not in self:
            raise AttributeError(
                "'{item}' header is not defined in headers.".format(item=item)
            )

        return self[item]

    def to_json(self) -> str:
        """
        Provide a JSON representation of Headers. JSON is by definition a string.
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
        """Return a new instance of Headers containing headers in reversed order."""
        list_of_headers: List[Header] = deepcopy(self._headers)
        list_of_headers.reverse()

        return Headers(list_of_headers)

    def __bool__(self) -> bool:
        """Return True if Headers does contain at least one entry in it."""
        return bool(self._headers)

    def __contains__(self, item: Union[Header, str]) -> bool:
        """
        This method will allow you to test if a header, based on its string name, is present or not in headers.
        You could also use a Header object to verify it's presence.
        """
        item = normalize_str(item) if isinstance(item, str) else item

        for header in self:
            if isinstance(item, str) and header.normalized_name == item:
                return True
            if isinstance(item, Header) and header == item:
                return True
        return False

    def insert(self, __index: int, __header: Header) -> None:
        """Insert header before the given index."""
        if not isinstance(__header, Header):
            raise TypeError(
                f"Cannot insert element of type {type(__header)} in Headers."
            )

        self._headers.insert(__index, __header)

    def index(
        self, __value: Union[Header, str], __start: int = 0, __stop: int = -1
    ) -> int:
        """
        Search for the first appearance of an header based on its name or instance in Headers.
        Same method signature as list().index().
        Raises IndexError if not found.
        >>> headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle")
        >>> headers.index("A")
        0
        >>> headers.index("A", 1)
        Traceback (most recent call last):
        ...
        IndexError: Value 'A' is not present within Headers.
        >>> headers.index("A", 0, 1)
        0
        >>> headers.index("C")
        2
        >>> headers.index(headers[0])
        0
        >>> headers.index(headers[1])
        1
        """

        value_is_header: bool = isinstance(__value, Header)
        normalized_value: Optional[str] = normalize_str(
            __value  # type: ignore
        ) if not value_is_header else None
        headers_len: int = len(self)

        # Convert indices to positive indices
        __start = __start % headers_len if __start < 0 else __start
        __stop = __stop % headers_len if __stop < 0 else __stop

        for header, index in zip(
            self._headers[__start : __stop + 1], range(__start, __stop + 1)
        ):
            if value_is_header and __value == header:
                return index
            elif normalized_value == header.normalized_name:
                return index

        raise IndexError(f"Value '{__value}' is not present within Headers.")

    def pop(self, __index_or_name: Union[str, int] = -1) -> Union[Header, List[Header]]:
        """
        Pop header instance(s) from headers. By default the last one. Accept index as integer or header name.
        If you pass a header name, it will pop from Headers every entry named likewise.
        >>> headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle")
        >>> header = headers.pop()
        >>> repr(header)
        'C: funny; riddle'
        >>> headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle")
        >>> header = headers.pop(1)
        >>> repr(header)
        'B: world'
        >>> header = headers.pop("A")
        >>> repr(header)
        'A: hello'
        >>> headers = Header("A", "hello") + Header("B", "world") + Header("C", "funny; riddle") + Header("B", "ending")
        >>> headers = headers.pop("B")
        >>> len(headers)
        2
        >>> headers[0].name
        'B'
        >>> (str(headers[0]), str(headers[1]))
        ('world', 'ending')
        """
        if isinstance(__index_or_name, int):
            return self._headers.pop(__index_or_name)
        if isinstance(__index_or_name, str):
            headers = self.get(__index_or_name)

            if headers is None:
                raise IndexError()

            if isinstance(headers, list):
                for header in headers:
                    self._headers.remove(header)
            else:
                self._headers.remove(headers)

            if OUTPUT_LOCK_TYPE is True and isinstance(headers, Header):
                return [headers]

            return headers

        raise TypeError(
            f"Type {type(__index_or_name)} is not supported by pop() method on Headers."
        )

    def popitem(self) -> Tuple[str, str]:
        """Pop the last header as a tuple (header name, header content)."""
        header: Header = self.pop()  # type: ignore
        return header.name, header.content

    def __dir__(self) -> Iterable[str]:
        """
        Provide a better auto-completion when using python interpreter. We are feeding __dir__ so Python can be aware
        of what properties are callable. In other word, more precise auto-completion when not using IDE.
        """
        return list(super().__dir__()) + list(
            set([header.normalized_name for header in self])
        )


class Attributes(object):
    """
    Dedicated class to handle attributes within a Header. Wrap an AttributeBag and offer methods to manipulate it
    with ease.
    Store advanced info on attributes, case insensitive on keys and keep attrs ordering.
    """

    def __init__(self, members: List[str]):
        self._bag: AttributeBag = CaseInsensitiveDict()

        for member, index in zip(members, range(0, len(members))):

            if member == "":
                continue

            if "=" in member:
                key, value = tuple(member.split("=", maxsplit=1))

                # avoid confusing base64 look alike single value for (key, value)
                if value.count("=") == len(value) or len(value) == 0 or " " in key:
                    self.insert(unquote(member), None)
                    continue

                self.insert(key, unquote(value))
                continue

            self.insert(unquote(member), None)

    def __str__(self) -> str:
        """Convert an Attributes instance to its string repr."""
        content: str = ""

        if len(self._bag) == 0:
            return content

        for i in range(0, len(self)):
            key, value = self[i]

            if value is not None:
                content += '{semi_colon_r}{key}="{value}"'.format(
                    key=key, value=value, semi_colon_r="; " if content != "" else "",
                )
            else:
                content += "; " + key if content != "" else key

        return content

    def keys(self) -> List[str]:
        """This method return a list of attribute name that have at least one value associated to them."""
        keys: List[str] = []

        for index, key, value in self:
            if key not in keys and value is not None:
                keys.append(key)

        return keys

    def __eq__(self, other: object) -> bool:
        """Verify if two instance of Attributes are equal. We don't care about ordering."""
        if not isinstance(other, Attributes):
            raise NotImplementedError

        if len(self) != len(other):
            return False

        list_repr_a: List[Tuple[int, str, Optional[str]]] = list(self)
        list_repr_b: List[Tuple[int, str, Optional[str]]] = list(other)

        list_check: List[Tuple[int, str, Optional[str]]] = []

        for index_a, key_a, value_a in list_repr_a:

            key_a = normalize_str(key_a)

            for index_b, key_b, value_b in list_repr_b:

                key_b = normalize_str(key_b)

                if (
                    key_a == key_b
                    and value_a == value_b
                    and (index_a, key_a, key_b) not in list_check
                ):

                    list_check.append((index_a, key_a, key_b))

        return len(list_check) == len(list_repr_a)

    def __getitem__(
        self, item: Union[int, str]
    ) -> Union[Tuple[str, Optional[str]], Union[str, List[str]]]:
        """"""

        if isinstance(item, str):
            values: List[str] = [
                value for value in self._bag[item][0] if value is not None
            ]
            return values if len(values) > 1 else values[0]

        for attr in self._bag:
            if item in self._bag[attr][1]:
                pos: int = self._bag[attr][1].index(item)
                return attr, self._bag[attr][0][pos]

        raise IndexError(f"{item} not in defined indexes.")

    def insert(
        self, key: str, value: Optional[str], index: Optional[int] = None
    ) -> None:
        """"""
        to_be_inserted: int = index if index is not None else len(self)

        if index is not None:
            for attr in self._bag:
                values, indexes = self._bag[attr]

                for index_, cur in zip(indexes, range(0, len(indexes))):
                    if index_ >= index:
                        self._bag[attr][1][cur] += 1

        if key not in self._bag:
            self._bag[key] = ([value], [to_be_inserted])
        else:
            self._bag[key][0].append(value)
            self._bag[key][1].append(to_be_inserted)

    def remove(self, key: str, index: Optional[int] = None) -> None:
        """"""
        if key not in self._bag:
            return

        freed_indexes: List[int] = []

        if index is not None:
            index = index if index >= 0 else index % (len(self))

            pos: int = self._bag[key][1].index(index)

            self._bag[key][0].pop(pos)

            freed_indexes.append(self._bag[key][1].pop(pos))

        if index is None or len(self._bag[key][0]) == 0:
            freed_indexes += self._bag[key][1]
            del self._bag[key]

        for attr in self._bag:

            values, indexes = self._bag[attr]
            max_freed_index: int = max(freed_indexes)

            for index_, cur in zip(indexes, range(0, len(indexes))):
                if index_ - 1 in freed_indexes:
                    self._bag[attr][1][cur] -= 1
                elif index_ > max_freed_index:
                    self._bag[attr][1][cur] -= 1

    def __contains__(self, item: Union[str, Dict[str, Union[List[str], str]]]) -> bool:
        """Verify if a member/attribute/value is in an Attributes instance. See examples bellow :
        >>> attributes = Attributes(["application/xml", "q=0.9", "q=0.1"])
        >>> "q" in attributes
        True
        >>> {"Q": "0.9"} in attributes
        True
        >>> "z" in attributes
        False
        >>> {"Q": "0.2"} in attributes
        False
        """
        if len(self._bag) == 0:
            return False

        if isinstance(item, str):
            return item in self._bag

        target_key, target_value = item.popitem()
        target_key = normalize_str(target_key)

        for i in range(0, len(self)):
            key, value = self[i]

            if target_key == key and target_value == value:
                return True

        return False

    @property
    def last_index(self) -> Optional[int]:
        """Simply output the latest index used in attributes. Index start from zero."""
        if len(self._bag) == 0:
            return None

        max_index: int = 0

        for key in self._bag:
            values, indexes = self._bag[key]

            maximum_ind_key: int = max(indexes)

            if maximum_ind_key > max_index:
                max_index = maximum_ind_key

        return max_index

    def __len__(self) -> int:
        """The length of an Attributes instance is equal to the last index plus one. Not by keys() length."""
        last_index: Optional[int] = self.last_index
        return last_index + 1 if last_index is not None else 0

    def __iter__(self) -> Iterator[Tuple[int, str, Optional[str]]]:
        """Provide an iterator over all attributes with or without associated value.
        For each entry, output a tuple of index, attribute and a optional value."""
        for i in range(0, len(self)):
            key, value = self[i]
            yield i, key, value


def lock_output_type(lock: bool = True) -> None:
    """
    This method will restrict type entropy by always returning a List[Header] instead of Union[Header, List[Header]]
    """
    global OUTPUT_LOCK_TYPE
    OUTPUT_LOCK_TYPE = lock
