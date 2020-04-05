from kiss_headers.models import Header
from kiss_headers.utils import class_to_header_name
from typing import Optional, Union, Dict, List

from datetime import datetime
from email import utils

"""
Use https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ to create subclasses of CustomHeader.
"""


class CustomHeader(Header):
    """
    This class is a helper to create ready-to-use Header object with creation assistance.
    Should NOT be instantiated.
    """

    def __init__(self, initial_content: str = "", **kwargs):
        """
        :param initial_content: Initial content of the Header if any.
        :param kwargs: Provided args. Any key that associate a None value are just ignored.
        """
        if self.__class__ == CustomHeader:
            raise NotImplementedError

        super().__init__(class_to_header_name(self.__class__), initial_content)

        for attribute, value in kwargs.items():
            if value is None:
                continue
            self[attribute] = value


class ContentType(CustomHeader):
    """
    The Content-Type entity header is used to indicate the media type of the resource.

    In responses, a Content-Type header tells the client what the content type of the returned content actually is.
    Browsers will do MIME sniffing in some cases and will not necessarily follow the value of this header;
    to prevent this behavior, the header X-Content-Type-Options can be set to nosniff.
    """

    def __init__(
        self,
        mime_type: str,
        charset: Optional[str] = None,
        format_: Optional[str] = None,
        boundary: Optional[str] = None,
        **kwargs,
    ):
        """
        :param mime_type: The MIME type of the resource or the data. Format <MIME_type>/<MIME_subtype>.
        :param charset: The character encoding standard. Should be an IANA name.
        :param format_: Mostly used in IMAP, could be one of : original or flowed.
        :param boundary: For multipart entities the boundary directive is required, which consists of 1 to 70 characters from a set of characters known to be very robust through email gateways, and not ending with white space. It is used to encapsulate the boundaries of the multiple parts of the message.
        :param kwargs:
        """

        args = {"charset": charset, "format": format_, "boundary": boundary}

        args.update(kwargs)

        super().__init__(mime_type, **args)


class ContentDisposition(CustomHeader):
    """
    In a regular HTTP response, the Content-Disposition response header is a header indicating
    if the content is expected to be displayed inline in the browser, that is, as a Web page or
    as part of a Web page, or as an attachment, that is downloaded and saved locally.
    """

    def __init__(
        self,
        is_form_data: bool = False,
        is_inline: bool = False,
        is_attachment: bool = False,
        name: Optional[str] = None,
        filename: Optional[str] = None,
        fallback_filename: Optional[str] = None,
        boundary: Optional[str] = None,
        **kwargs,
    ):
        """
        :param is_form_data: Indicating it is a form-data.
        :param is_inline: Default value, indicating it can be displayed inside the Web page, or as the Web page
        :param is_attachment: Indicating it should be downloaded; most browsers presenting a 'Save as' dialog.
        :param name: Is a string containing the name of the HTML field in the form that the content of this subpart refers to.
        :param filename: Is a string containing the original name of the file transmitted. The filename is always optional and must not be used blindly by the application.
        :param fallback_filename: Fallback filename if filename parameter does not uses the encoding defined in RFC 5987. ASCII-US Only.
        :param boundary: For multipart entities the boundary directive is required, which consists of 1 to 70 characters from a set of characters known to be very robust through email gateways, and not ending with white space. It is used to encapsulate the boundaries of the multiple parts of the message.
        :param kwargs:
        """
        if [is_inline, is_form_data, is_attachment].count(True) != 1:
            raise ValueError(
                "Content-Disposition should be either inline, form-data or attachment. Choose one."
            )

        args = {
            "name": name,
            "filename": filename,
            "filename*": fallback_filename,
            "boundary": boundary,
        }

        args.update(kwargs)

        super().__init__(
            "form-data"
            if is_form_data
            else "inline"
            if is_inline
            else "attachment"
            if is_attachment
            else "",
            **args,
        )


class Authorization(CustomHeader):
    """
    The HTTP Authorization request header contains the credentials to authenticate a user agent with a server,
    usually, but not necessarily, after the server has responded with a 401 Unauthorized status
    and the WWW-Authenticate header.
    """

    def __init__(self, type_: str, credentials: str):
        """
        :param type_: Authentication type. A common type is "Basic". See IANA registry of Authentication schemes for others.
        :param credentials: Associated credentials to use. Preferably Base-64 encoded.
        """
        if type_.lower() not in [
            "basic",
            "bearer",
            "digest",
            "hoba",
            "mutual",
            "negotiate",
            "oauth",
            "scram-sha-1",
            "scram-sha-256",
            "vapid",
            "aws4-hmac-sha256",
        ]:
            raise ValueError(
                "Authorization type should exist in IANA registry of Authentication schemes"
            )

        super().__init__(
            "{type_} {credentials}".format(type_=type_, credentials=credentials)
        )


class Host(CustomHeader):
    """
    The Host request header specifies the domain name of the server (for virtual hosting),
    and (optionally) the TCP port number on which the server is listening.
    """

    def __init__(self, host: str, port: Optional[int], **kwargs):
        """
        :param host: The domain name of the server (for virtual hosting).
        :param port: TCP port number on which the server is listening.
        """
        super().__init__(host + (":" + str(port) if port else ""), **kwargs)


class Connection(CustomHeader):
    """
    The Connection general header controls whether or not the network connection stays open after the current transaction finishes.
    If the value sent is keep-alive, the connection is persistent and not closed, allowing for subsequent requests to the same server to be done.
    """

    def __init__(self, should_keep_alive: bool, **kwargs):
        """
        :param should_keep_alive: Indicates that the client would like to keep the connection open or not.
        :param kwargs:
        """
        super().__init__("keep-alive" if should_keep_alive else "close", **kwargs)


class ContentLength(CustomHeader):
    """
    The Content-Length entity header indicates the size of the entity-body, in bytes, sent to the recipient.
    """

    def __init__(self, length: int, **kwargs):
        """
        :param length: The length in decimal number of octets.
        """
        super().__init__(str(length), **kwargs)


class Date(CustomHeader):
    """
    The Date general HTTP header contains the date and time at which the message was originated.
    """

    def __init__(self, my_date: Union[datetime, str], **kwargs):
        """
        :param my_date: Can either be a datetime that will be automatically converted or a raw string.
        :param kwargs:
        """
        super().__init__(
            utils.format_datetime(my_date) if not isinstance(my_date, str) else my_date,
            **kwargs,
        )


class SetCookie(CustomHeader):
    """
    The Set-Cookie HTTP response header is used to send cookies from the server to the user agent,
    so the user agent can send them back to the server later.
    """

    def __init__(
        self,
        cookie_name: str,
        cookie_value: str,
        expires: Optional[Union[datetime, str]] = None,
        max_age: Optional[int] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
        samesite: Optional[str] = None,
        is_secure: bool = False,
        is_httponly: bool = True,
        **kwargs,
    ):
        """

        :param cookie_name: Can be any US-ASCII characters, except control characters, spaces, or tabs.
        :param cookie_value: Can include any US-ASCII characters excluding control characters, Whitespace, double quotes, comma, semicolon, and backslash.
        :param expires: The maximum lifetime of the cookie as an HTTP-date timestamp. Provided datetime will be converted automatically.
        :param max_age: Number of seconds until the cookie expires. A zero or negative number will expire the cookie immediately. If both Expires and Max-Age are set, Max-Age has precedence.
        :param domain: Hosts to where the cookie will be sent. If omitted, defaults to the host of the current document URL, not including subdomains.
        :param path: A path that must exist in the requested URL, or the browser won't send the Cookie header.
        :param samesite: Asserts that a cookie must not be sent with cross-origin requests, providing some protection against cross-site request forgery attacks.
        :param is_secure: A secure cookie is only sent to the server when a request is made with the https: scheme.
        :param is_httponly: Forbids JavaScript from accessing the cookie.
        :param kwargs:
        """

        for letter in cookie_name:
            if letter in {'<>@,;:\\"/[]?={}'}:
                raise ValueError(
                    'The cookie name can not contains any of the following char: <>@,;:"/[]?={}'
                )

        if samesite and samesite.lower() not in ["strict", "lax", "none"]:
            raise ValueError(
                "Samesite attribute can only be one of the following: Strict, Lax or None."
            )

        args = {
            cookie_name: cookie_value,
            "expires": utils.format_datetime(expires)
            if isinstance(expires, datetime)
            else expires,
            "max-age": max_age,
            "domain": domain,
            "path": path,
            "samesite": samesite,
        }

        args.update(kwargs)

        super().__init__("", **args)

        if is_secure:
            self += "Secure"  # type: ignore
        if is_httponly:
            self += "HttpOnly"  # type: ignore
