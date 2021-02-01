from typing import Dict, List, Optional, Union

from kiss_headers.models import Headers, Header


def encode(headers: Headers) -> Dict[str, List[Dict]]:
    """
    Provide an opinionated but reliable way to encode headers to dict for serialization purposes.
    """
    result: Dict[str, List[Dict]] = dict()

    for header in headers:

        if header.name not in result:
            result[header.name] = list()

        encoded_header: Dict[str, Union[Optional[str], List[str]]] = dict()

        for attribute, value in header:
            encoded_header[attribute] = value

        result[header.name].append(encoded_header)

    return result


def decode(encoded_headers: Dict[str, List[Dict]]) -> Headers:
    """
    Decode any previously encoded headers to a Headers object.
    """
    headers: Headers = Headers()

    for header_name, encoded_header_list in encoded_headers.items():
        if not isinstance(encoded_header_list, list):
            raise ValueError

        for encoded_header in encoded_header_list:
            if not isinstance(encoded_header, dict):
                raise ValueError

            header = Header(header_name, "")

            for attr, value in encoded_header.items():
                if value is not None:
                    header[attr] = value
                    continue
                header += attr

            headers += header

    return headers
