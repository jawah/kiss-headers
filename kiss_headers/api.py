from email.message import Message
from email.parser import BytesHeaderParser, HeaderParser
from io import BytesIO, IOBase
from typing import Any, Iterable, List, Mapping, Optional, Tuple

from kiss_headers.models import Header, Headers
from kiss_headers.structures import CaseInsensitiveDict
from kiss_headers.utils import (
    decode_partials,
    extract_class_name,
    header_content_split,
    header_name_to_class,
    is_legal_header_name,
)


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
    elif isinstance(raw_headers, bytes) or isinstance(raw_headers, IOBase):
        headers = (
            BytesHeaderParser()
            .parse(
                BytesIO(raw_headers) if isinstance(raw_headers, bytes) else raw_headers,  # type: ignore
                headersonly=True,
            )
            .items()
        )
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
            elif r in ["httpx._models.Response", "urllib3.response.HTTPResponse"]:
                headers = raw_headers.headers.items()

    if headers is None:
        raise TypeError(
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

        # Multiple entries are detected in one content
        if len(entries) > 1:
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
        raise LookupError(
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
