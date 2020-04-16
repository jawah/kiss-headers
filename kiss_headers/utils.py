from email.header import decode_header
from re import findall, search
from typing import Any, Iterable, List, Optional, Tuple, Type


def normalize_str(string: str) -> str:
    """
    Normalize a string by applying on it lowercase and replacing '-' to '_'.
    >>> normalize_str("Content-Type")
    'content_type'
    >>> normalize_str("X-content-type")
    'x_content_type'
    """
    return string.lower().replace("-", "_")


def extract_class_name(type_: Type) -> Optional[str]:
    """
    Typically extract a class name from a Type.
    """
    r = findall(r"<class '([a-zA-Z0-9._]+)'>", str(type_))
    return r[0] if r else None


def header_content_split(string: str, delimiter: str) -> List[str]:
    """
    Take a string and split it according to the passed delimiter.
    It will ignore delimiter if inside between double quote, inside a value or in parenthesis.
    The input string is considered perfectly formed. This function do not split coma on a day
    when attached, see "RFC 7231, section 7.1.1.2: Date".
    >>> header_content_split("Wed, 15-Apr-2020 21:27:31 GMT, Fri, 01-Jan-2038 00:00:00 GMT", ",")
    ['Wed, 15-Apr-2020 21:27:31 GMT', 'Fri, 01-Jan-2038 00:00:00 GMT']
    >>> header_content_split('quic=":443"; ma=2592000; v="46,43", h3-Q050=":443"; ma=2592000, h3-Q049=":443"; ma=2592000', ",")
    ['quic=":443"; ma=2592000; v="46,43"', 'h3-Q050=":443"; ma=2592000', 'h3-Q049=":443"; ma=2592000']
    >>> header_content_split("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0", ";")
    ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0']
    >>> header_content_split("text/html; charset=UTF-8", ";")
    ['text/html', 'charset=UTF-8']
    """
    if len(delimiter) != 1 or delimiter not in {";", ","}:
        raise ValueError("Delimiter should be either semi-colon or a coma.")

    in_double_quote: bool = False
    in_parenthesis: bool = False
    in_value: bool = False
    is_on_a_day: bool = False

    result: List[str] = [""]

    for letter, index in zip(string, range(0, len(string))):

        if letter == '"':
            in_double_quote = not in_double_quote

            if in_value and not in_double_quote:
                in_value = False

        elif letter == "(" and not in_parenthesis:
            in_parenthesis = True
        elif letter == ")" and in_parenthesis:
            in_parenthesis = False
        else:
            is_on_a_day = index >= 3 and string[index - 3 : index] in {
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
            }

        if not in_double_quote:

            if not in_value and letter == "=":
                in_value = True
            elif letter == ";" and in_value:
                in_value = False

            if in_value and letter == delimiter and not is_on_a_day:
                in_value = False

        if letter == delimiter and (
            (in_value or in_double_quote or in_parenthesis or is_on_a_day) is False
        ):

            result[-1] = result[-1].lstrip().rstrip()
            result.append("")

            continue

        result[-1] += letter

    if result:
        result[-1] = result[-1].lstrip().rstrip()

    return result


def class_to_header_name(type_: Type) -> str:
    """
    Take a type and infer its header name.
    >>> from kiss_headers.builder import ContentType, XContentTypeOptions
    >>> class_to_header_name(ContentType)
    'Content-Type'
    >>> class_to_header_name(XContentTypeOptions)
    'X-Content-Type-Options'
    """
    class_raw_name: str = str(type_).split("'")[-2].split(".")[-1]

    if class_raw_name.endswith("_"):
        class_raw_name = class_raw_name[:-1]

    if class_raw_name.startswith("_"):
        class_raw_name = class_raw_name[1:]

    header_name: str = str()

    for letter in class_raw_name:
        if letter.isupper() and header_name != "":
            header_name += "-" + letter
            continue
        header_name += letter

    return header_name


def header_name_to_class(name: str, root_type: Type) -> Type:
    """
    The opposite of class_to_header_name function. Will raise TypeError if no corresponding entry is found.
    Do it recursively from the root type.
    >>> from kiss_headers.builder import CustomHeader, ContentType, XContentTypeOptions, LastModified, Date
    >>> header_name_to_class("Content-Type", CustomHeader)
    <class 'kiss_headers.builder.ContentType'>
    >>> header_name_to_class("Last-Modified", CustomHeader)
    <class 'kiss_headers.builder.LastModified'>
    """

    normalized_name = normalize_str(name).replace("_", "")

    for subclass in root_type.__subclasses__():
        class_name = extract_class_name(subclass)

        if class_name is None:
            continue

        if normalize_str(class_name.split(".")[-1]) == normalized_name:
            return subclass

        if subclass.__subclasses__():
            try:
                return header_name_to_class(name, subclass)
            except TypeError:
                continue

    raise TypeError(
        "Cannot find a class matching header named '{name}'.".format(name=name)
    )


def prettify_header_name(name: str) -> str:
    """
    Take a header name and prettify it.
    >>> prettify_header_name("x-hEllo-wORLD")
    'X-Hello-World'
    >>> prettify_header_name("server")
    'Server'
    >>> prettify_header_name("contEnt-TYPE")
    'Content-Type'
    >>> prettify_header_name("content_type")
    'Content-Type'
    """
    return "-".join([el.capitalize() for el in name.replace("_", "-").split("-")])


def decode_partials(items: Iterable[Tuple[str, Any]]) -> List[Tuple[str, str]]:
    """
    This function takes a list of tuple, representing headers by key, value. Where value is bytes or string containing
    (RFC 2047 encoded) partials fragments like the following :
    >>> decode_partials([("Subject", "=?iso-8859-1?q?p=F6stal?=")])
    [('Subject', 'pöstal')]
    """
    revised_items: List[Tuple[str, str]] = list()

    for head, content in items:
        revised_content: str = str()

        for partial, partial_encoding in decode_header(content):
            if isinstance(partial, str):
                revised_content += partial
            if isinstance(partial, bytes):
                revised_content += partial.decode(
                    partial_encoding if partial_encoding is not None else "utf-8",
                    errors="ignore",
                )

        revised_items.append((head, revised_content))

    return revised_items


def unquote(string: str) -> str:
    """
    Remove simple quote or double quote around a string if any.
    >>> unquote('"hello"')
    'hello'
    >>> unquote('"hello')
    '"hello'
    >>> unquote('"a"')
    'a'
    >>> unquote('""')
    ''
    """
    if (
        len(string) >= 2
        and (string.startswith('"') and string.endswith('"'))
        or (string.startswith("'") and string.endswith("'"))
    ):
        return string[1:-1]

    return string


def quote(string: str) -> str:
    """
    Surround string by double quote.
    >>> quote("hello")
    '"hello"'
    >>> quote('"hello')
    '""hello"'
    >>> quote('"hello"')
    '"hello"'
    """
    return '"' + unquote(string) + '"'


def count_leftover_space(content: str) -> int:
    """
    Recursive function that count trailing white space at the end of given string.
    >>> count_leftover_space("hello   ")
    3
    >>> count_leftover_space("byebye ")
    1
    >>> count_leftover_space("  hello ")
    1
    >>> count_leftover_space("  hello    ")
    4
    """
    if content.endswith(" "):
        return count_leftover_space(content[:-1]) + 1
    return 0


def header_strip(content: str, elem: str) -> str:
    """
    Remove a member for a given header content and take care of the unneeded leftover semi-colon.
    >>> header_strip("text/html; charset=UTF-8; format=flowed", "charset=UTF-8")
    'text/html; format=flowed'
    >>> header_strip("text/html; charset=UTF-8;    format=flowed", "charset=UTF-8")
    'text/html; format=flowed'
    """
    next_semi_colon_index: Optional[int] = None

    try:
        elem_index: int = content.index(elem)
    except ValueError:
        # If the target element in not found within the content, just return the unmodified content.
        return content

    elem_end_index: int = elem_index + len(elem)

    elem = (" " * count_leftover_space(content[:elem_index])) + elem

    try:
        next_semi_colon_index = elem_end_index + content[elem_end_index:].index(";")
    except ValueError:
        pass

    content = (
        content.replace(
            elem
            + (
                content[elem_end_index:next_semi_colon_index] + ";"
                if next_semi_colon_index is not None
                else ""
            ),
            "",
        )
        .rstrip(" ")
        .lstrip(" ")
    )

    if content.startswith(";"):
        content = content[1:]

    if content.endswith(";"):
        content = content[:-1]

    return content


def is_legal_header_name(name: str) -> bool:
    """
    Verify if a provided header name is valid.
    >>> is_legal_header_name(":hello")
    False
    >>> is_legal_header_name("hello")
    True
    >>> is_legal_header_name("Content-Type")
    True
    >>> is_legal_header_name("Hello;")
    False
    >>> is_legal_header_name("Hello\\rWorld")
    False
    >>> is_legal_header_name("Hello \\tWorld")
    False
    """
    return (
        name != ""
        and search(r"[^\x00-\x7F]|[:;(),<>=@?\[\]\r\n\t &{}\\]", name) is None
    )
