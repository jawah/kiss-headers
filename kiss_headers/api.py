from email.message import Message
from email.parser import HeaderParser
from io import RawIOBase
from typing import Any, Iterable, List, Mapping, Optional, Tuple, Type, TypeVar, Union

from kiss_headers.models import Header, Headers
from kiss_headers.structures import CaseInsensitiveDict
from kiss_headers.utils import (
    class_to_header_name,
    decode_partials,
    extract_class_name,
    extract_encoded_headers,
    header_content_split,
    header_name_to_class,
    is_legal_header_name,
    normalize_str,
)

T = TypeVar("T")


def parse_it(raw_headers: Any) -> Headers:
    """
    Just decode anything that could contain headers. That simple PERIOD.
    :param raw_headers: Accept bytes, str, fp, dict, email.Message, requests.Response, urllib3.HTTPResponse and httpx.Response.
    :raises:
        TypeError: If passed argument cannot be parsed to extract headers from it.
    """

    headers: Optional[Iterable[Tuple[str, Any]]] = None

    if isinstance(raw_headers, str):
        headers = HeaderParser().parsestr(raw_headers, headersonly=True).items()
    elif isinstance(raw_headers, bytes) or isinstance(raw_headers, RawIOBase):
        decoded, not_decoded = extract_encoded_headers(
            raw_headers if isinstance(raw_headers, bytes) else raw_headers.read() or b""
        )
        return parse_it(decoded)
    elif isinstance(raw_headers, Mapping) or isinstance(raw_headers, Message):
        headers = raw_headers.items()
    else:
        r = extract_class_name(type(raw_headers))

        if r:
            if r == "requests.models.Response":
                headers = []
                for header_name in raw_headers.raw.headers:
                    for header_content in raw_headers.raw.headers.getlist(header_name):
                        headers.append((header_name, header_content))
            elif r in [
                "httpx._models.Response",
                "urllib3.response.HTTPResponse",
            ]:  # pragma: no cover
                headers = raw_headers.headers.items()

    if headers is None:
        raise TypeError(  # pragma: no cover
            "Cannot parse type {type_} as it is not supported by kiss-header.".format(
                type_=type(raw_headers)
            )
        )

    revised_headers: List[Tuple[str, str]] = decode_partials(headers)

    # Sometime raw content does not begin with headers. If that is the case, search for the next line.
    if (
        len(revised_headers) == 0
        and len(raw_headers) > 0
        and (isinstance(raw_headers, bytes) or isinstance(raw_headers, str))
    ):
        next_iter = raw_headers.split(
            b"\n" if isinstance(raw_headers, bytes) else "\n", maxsplit=1  # type: ignore
        )

        if len(next_iter) >= 2:
            return parse_it(next_iter[-1])

    # Prepare Header objects
    list_of_headers: List[Header] = []

    for head, content in revised_headers:

        # We should ignore when a illegal name is considered as an header. We avoid ValueError (in __init__ of Header)
        if is_legal_header_name(head) is False:
            continue

        entries: List[str] = header_content_split(content, ",")

        # Multiple entries are detected in one content at the only exception that its not IMAP header "Subject".
        if len(entries) > 1 and normalize_str(head) != "subject":
            for entry in entries:
                list_of_headers.append(Header(head, entry))
        else:
            list_of_headers.append(Header(head, content))

    return Headers(*list_of_headers)


def explain(headers: Headers) -> CaseInsensitiveDict:
    """
    Return a brief explanation of each header present in headers if available.
    """
    if not Header.__subclasses__():
        raise LookupError(  # pragma: no cover
            "You cannot use explain() function without properly importing the public package."
        )

    explanations: CaseInsensitiveDict = CaseInsensitiveDict()

    for header in headers:
        if header.name in explanations:
            continue

        try:
            target_class = header_name_to_class(header.name, Header.__subclasses__()[0])
        except TypeError:
            explanations[header.name] = "Unknown explanation."
            continue

        explanations[header.name] = (
            target_class.__doc__.replace("\n", "").lstrip().replace("  ", " ").rstrip()
            if target_class.__doc__
            else "Missing docstring."
        )

    return explanations


def get_polymorphic(
    target: Union[Headers, Header], desired_output: Type[T]
) -> Union[T, List[T], None]:
    """Experimental. Transform a Header or Headers object to its target `CustomHeader` subclass
    to access more ready-to-use methods. eg. You have a Header object named 'Set-Cookie' and you wish
    to extract the expiration date as a datetime.
    >>> header = Header("Set-Cookie", "1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT")
    >>> header["expires"]
    'Wed, 15-Apr-2020 21:27:31 GMT'
    >>> from kiss_headers import SetCookie
    >>> set_cookie = get_polymorphic(header, SetCookie)
    >>> set_cookie.get_expire()
    datetime.datetime(2020, 4, 15, 21, 27, 31, tzinfo=datetime.timezone.utc)
    """

    if not issubclass(desired_output, Header):
        raise TypeError(
            f"The desired output should be a subclass of Header not {desired_output}."
        )

    desired_output_header_name: str = class_to_header_name(desired_output)

    if isinstance(target, Headers):
        r = target.get(desired_output_header_name)

        if r is None:
            return None

    elif isinstance(target, Header):
        if header_name_to_class(target.name, Header) != desired_output:
            raise TypeError(
                f"The target class does not match the desired output class. {target.__class__} != {desired_output}."
            )
        r = target
    else:
        raise TypeError(f"Unable to apply get_polymorphic on type {target.__class__}.")

    # Change __class__ attribute.
    if not isinstance(r, list):
        r.__class__ = desired_output
    else:
        for header in r:
            header.__class__ = desired_output

    return r  # type: ignore
