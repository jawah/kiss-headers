from kiss_headers.models import Headers, Header, OUTPUT_LOCK_TYPE

from typing import Optional, Iterable, Tuple, Any, Mapping
from re import findall
from email.header import decode_header
from email.parser import HeaderParser, BytesHeaderParser
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
    else:
        r = findall(r"<class '([a-zA-Z0-9._]+)'>", str(type(raw_headers)))

        if r:
            if r[0] == "requests.models.Response":
                headers = []
                for header_name in raw_headers.raw.headers:
                    for header_content in raw_headers.raw.headers.getlist(header_name):
                        headers.append((header_name, header_content))
            elif r[0] == "httpx._models.Response":
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

    return Headers([Header(head, content) for head, content in revised_headers])


def lock_output_type(lock: bool = True):
    """
    This method will restrict type entropy by always return a List[Header] instead of Union[Header, List[Header]]
    """
    global OUTPUT_LOCK_TYPE
    OUTPUT_LOCK_TYPE = lock
