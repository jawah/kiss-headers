from kiss_headers.models import Headers, Header
from kiss_headers.utils import flat_split, extract_class_name

from typing import Optional, Iterable, Tuple, Any, Mapping, List
from email.header import decode_header
from email.parser import HeaderParser, BytesHeaderParser
from email.message import Message
from io import BytesIO, IOBase


def parse_it(raw_headers: Any) -> Headers:
    """
    Just decode anything that could contain headers. That simple PERIOD.
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
    elif isinstance(raw_headers, Mapping):
        headers = raw_headers.items()
    elif isinstance(raw_headers, Message):
        headers = raw_headers.items()
    else:
        r = extract_class_name(raw_headers)

        if r:
            if r == "requests.models.Response":
                headers = []
                for header_name in raw_headers.raw.headers:
                    for header_content in raw_headers.raw.headers.getlist(header_name):
                        headers.append((header_name, header_content))
            elif r == "httpx._models.Response":
                headers = raw_headers.headers.items()

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
            b"\n" if isinstance(raw_headers, bytes) else "\n", maxsplit=1  # type: ignore
        )

        if len(next_iter) >= 2:
            return parse_it(next_iter[-1])

    # Build the Headers object
    headers: List[Header] = []

    for head, content in revised_headers:
        entries: List[str] = flat_split(content, ",")

        # Multiple entries are detected in one content and its not a "RFC 7231, section 7.1.1.2: Date"
        if len(entries) > 1 and entries[0] not in {
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        }:
            for entry in entries:
                headers.append(Header(head, entry))
        else:
            headers.append(Header(head, content))

    return Headers(headers)
