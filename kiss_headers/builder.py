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

    __squash__: bool = False
    __tags__: List[str] = []

    def __init__(self, initial_content: str = "", **kwargs):
        """
        :param initial_content: Initial content of the Header if any.
        :param kwargs: Provided args. Any key that associate a None value are just ignored.
        """
        if self.__class__ == CustomHeader:
            raise NotImplementedError(
                "You can not instantiate CustomHeader class. You may create first your class that inherit it."
            )

        super().__init__(class_to_header_name(self.__class__), initial_content)

        for attribute, value in kwargs.items():
            if value is None:
                continue
            self[attribute] = value


class Accept(CustomHeader):
    """
    The Accept request HTTP header advertises which content types, expressed as MIME types,
    the client is able to understand. Using content negotiation, the server then selects one of
    the proposals, uses it and informs the client of its choice with the Content-Type response header.
    """

    __squash__: bool = True
    __tags__: List[str] = ["request"]

    def __init__(
        self,
        mime_type: str = "*",
        mime_subtype: str = "*",
        qualifier: float = 1.0,
        **kwargs,
    ):
        """
        :param mime_type:
        :param mine_subtype:
        :param qualifier: Any value used is placed in an order of preference expressed using relative quality value called the weight.
        :param kwargs:
        """
        args: Dict = {"q": qualifier if qualifier < 1.0 else None}

        args.update(kwargs)

        super().__init__(
            "{mime_type}/{mime_subtype}".format(
                mime_type=mime_type, mime_subtype=mime_subtype
            ),
            **args,
        )


class ContentType(CustomHeader):
    """
    The Content-Type entity header is used to indicate the media type of the resource.

    In responses, a Content-Type header tells the client what the content type of the returned content actually is.
    Browsers will do MIME sniffing in some cases and will not necessarily follow the value of this header;
    to prevent this behavior, the header X-Content-Type-Options can be set to nosniff.
    """

    __tags__: List[str] = ["request", "response"]

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

        args: Dict = {"charset": charset, "format": format_, "boundary": boundary}

        args.update(kwargs)

        super().__init__(mime_type, **args)


class XContentTypeOptions(CustomHeader):
    """
    The X-Content-Type-Options response HTTP header is a marker used by the server to indicate that
    the MIME types advertised in the Content-Type headers should not be changed and be followed.
    This allows to opt-out of MIME type sniffing, or, in other words, it is a way to say that
    the webmasters knew what they were doing.
    """

    __tags__: List[str] = ["response"]

    def __init__(self, nosniff: bool = True, **kwargs):
        """
        :param nosniff: see https://fetch.spec.whatwg.org/#x-content-type-options-header
        :param kwargs:
        """
        super().__init__("nosniff" if nosniff else "", **kwargs)


class ContentDisposition(CustomHeader):
    """
    In a regular HTTP response, the Content-Disposition response header is a header indicating
    if the content is expected to be displayed inline in the browser, that is, as a Web page or
    as part of a Web page, or as an attachment, that is downloaded and saved locally.
    """

    __tags__: List[str] = ["request", "response"]

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

        args: Dict = {
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
            "ntlm",
        ]:
            raise ValueError(
                "Authorization type should exist in IANA registry of Authentication schemes"
            )

        super().__init__(
            "{type_} {credentials}".format(type_=type_, credentials=credentials)
        )


class ProxyAuthorization(Authorization):
    """
    The HTTP Proxy-Authorization request header contains the credentials to authenticate a user agent to a proxy server,
    usually after the server has responded with a 407 Proxy Authentication Required status
    and the Proxy-Authenticate header.
    """

    def __init__(self, type_: str, credentials: str):
        """
        :param type_: Authentication type. A common type is "Basic". See IANA registry of Authentication schemes for others.
        :param credentials: Associated credentials to use. Preferably Base-64 encoded.
        """
        super().__init__(type_, credentials)


class Host(CustomHeader):
    """
    The Host request header specifies the domain name of the server (for virtual hosting),
    and (optionally) the TCP port number on which the server is listening.
    """

    __tags__: List[str] = ["request"]

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

    __tags__: List[str] = ["request", "response"]

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

    __tags__: List[str] = ["response"]

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

        args: Dict = {
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


class StrictTransportSecurity(CustomHeader):
    """
    The HTTP Strict-Transport-Security response header (often abbreviated as HSTS) lets a web site
    tell browsers that it should only be accessed using HTTPS, instead of using HTTP.
    """

    __tags__: List[str] = ["response"]

    def __init__(
        self,
        max_age: int,
        does_includesubdomains: bool = False,
        is_preload: bool = False,
        **kwargs,
    ):
        """
        :param max_age: The time, in seconds, that the browser should remember that a site is only to be accessed using HTTPS.
        :param does_includesubdomains: If this optional parameter is specified, this rule applies to all of the site's subdomains as well.
        :param is_preload: Preloading Strict Transport Security. Google maintains an HSTS preload service. By following the guidelines and successfully submitting your domain, browsers will never connect to your domain using an insecure connection.
        :param kwargs:
        """
        args: Dict = {"max-age": max_age}

        args.update(kwargs)

        super().__init__("", **args)

        if does_includesubdomains:
            self += "includeSubDomains"  # type: ignore

        if is_preload:
            self += "preload"  # type: ignore


class UpgradeInsecureRequests(CustomHeader):
    """
    The HTTP Upgrade-Insecure-Requests request header sends a signal to the server expressing
    the client’s preference for an encrypted and authenticated response, and that it
    can successfully handle the upgrade-insecure-requests CSP directive.
    """

    def __init__(self, **kwargs):
        super().__init__("1", **kwargs)


class TransferEncoding(CustomHeader):
    """
    The Transfer-Encoding header specifies the form of encoding used to safely transfer the payload body to the user.
    """

    __tags__: List[str] = ["response"]
    __squash__: bool = True

    def __init__(
        self, method: str, **kwargs,
    ):
        """
        :param method: Either chunked, compress, deflate, gzip or identity.
        :param kwargs:
        """

        if method.lower() not in ["chunked", "compress", "deflate", "gzip", "identity"]:
            raise ValueError(
                "You should choose between 'chunked', 'compress', 'deflate', 'gzip', 'identity' for Transfer-Encoding method."
            )

        super().__init__(method, **kwargs)


class Dnt(CustomHeader):
    """
    The DNT (Do Not Track) request header indicates the user's tracking preference.
    It lets users indicate whether they would prefer privacy rather than personalized content.
    """

    __tags__: List[str] = ["request"]

    def __init__(self, tracking_consent: bool = False, **kwargs):
        """
        :param tracking_consent: The user prefers to allow tracking on the target site or not.
        :param kwargs:
        """
        super().__init__("1" if tracking_consent else "0", **kwargs)


class AltSvc(CustomHeader):
    """
    The Alt-Svc HTTP response header is used to advertise alternative services through which
    the same resource can be reached. An alternative service is defined by a protocol/host/port combination.
    """

    __tags__: List[str] = ["response"]
    __squash__: bool = True

    def __init__(
        self,
        protocol_id: str,
        alt_authority: str,
        max_age: Optional[int] = None,
        do_persist: Optional[bool] = None,
        **kwargs,
    ):
        """
        :param protocol_id: The ALPN protocol identifier. Examples include h2 for HTTP/2 and h3-25 for draft 25 of the HTTP/3 protocol.
        :param alt_authority: The quoted string specifying the alternative authority which consists of an optional host override, a colon, and a mandatory port number.
        :param max_age: The number of seconds for which the alternative service is considered fresh. If omitted, it defaults to 24 hours.
        :param do_persist: Use the parameter to ensures that the entry is not deleted through network configuration changes.
        :param kwargs:
        """
        args: Dict = {protocol_id: alt_authority}

        if max_age:
            args["ma"] = max_age

        if do_persist:
            args["persist"] = 1

        args.update(kwargs)

        super().__init__(**kwargs)


class Forwarded(CustomHeader):
    """
    The Forwarded header contains information from the client-facing side of proxy servers
    that is altered or lost when a proxy is involved in the path of the request.
    """

    def __init__(
        self, by: str, for_: str, using_proto: str, host: Optional[str] = None, **kwargs
    ):
        """
        :param by: The interface where the request came in to the proxy server. Could be an IP address, an obfuscated identifier or "unknown".
        :param for_: The client that initiated the request and subsequent proxies in a chain of proxies.
        :param host: The Host request header field as received by the proxy.
        :param using_proto: Indicates which protocol was used to make the request (typically "http" or "https").
        :param kwargs:
        """
        args: Dict = {"by": by, "for": for_, "host": host, "proto": using_proto}

        args.update(kwargs)

        super().__init__("", **args)


class LastModified(Date):
    """
    The Last-Modified response HTTP header contains the date and time at which the origin server
    believes the resource was last modified. It is used as a validator
    to determine if a resource received or stored is the same.
    """

    def __init__(self, my_date: Union[datetime, str], **kwargs):
        """
        :param my_date:
        :param kwargs:
        """
        super().__init__(my_date, **kwargs)


class Referer(CustomHeader):
    """
    The Referer request header contains the address of the previous web page from which a link to the currently
    requested page was followed. The Referer header allows servers to identify where people are
    visiting them from and may use that data for analytics, logging, or optimized caching, for example.

    Note that referer is actually a misspelling of the word "referrer". See https://en.wikipedia.org/wiki/HTTP_referer
    """

    __tags__: List[str] = ["request"]

    def __init__(self, url: str, **kwargs):
        """
        :param url: An absolute or partial address of the previous web page from which a link to the currently requested page was followed. URL fragments not included.
        :param kwargs:
        """
        super().__init__(url, **kwargs)


class ReferrerPolicy(CustomHeader):
    """
    The Referrer-Policy HTTP header controls how much referrer information
    (sent via the Referer header) should be included with requests.
    """

    __tags__: List[str] = ["request", "response"]

    def __init__(self, *policies: List[str], **kwargs):
        pass


class RetryAfter(Date):
    """
    The Retry-After response HTTP header indicates how long the user agent should wait
    before making a follow-up request.
    """

    __tags__: List[str] = ["response"]

    def __init__(self, delay_or_date: Union[datetime, int], **kwargs):
        super().__init__(
            delay_or_date
            if isinstance(delay_or_date, datetime)
            else str(delay_or_date),
            **kwargs,
        )


class AcceptLanguage(CustomHeader):
    """
    The Accept-Language request HTTP header advertises which languages the client is able to understand,
    and which locale variant is preferred. (By languages, we mean natural languages,
    such as English, and not programming languages.)
    """

    __squash__: bool = True
    __tags__: List[str] = ["request"]

    def __init__(self, language: str = "*", qualifier: float = 1.0, **kwargs):
        args: Dict = {"q": qualifier if qualifier < 1.0 else None}

        args.update(kwargs)

        super().__init__(
            language, **args,
        )


class Etag(CustomHeader):
    """
    The ETag HTTP response header is an identifier for a specific version of a resource.
    It lets caches be more efficient and save bandwidth, as a web server does not need to
    resend a full response if the content has not changed.
    """

    def __init__(self, etag_value: str, is_a_weak_validator: bool = False, **kwargs):
        """
        :param etag_value: Entity tag uniquely representing the requested resource. ASCII string only. Not quoted.
        :param is_a_weak_validator: Indicates that a weak validator is used. Weak etags are easy to generate, but are far less useful for comparisons.
        :param kwargs:
        """
        pass


class XFrameOptions(CustomHeader):
    """
    The X-Frame-Options HTTP response header can be used to indicate whether or not a browser
    should be allowed to render a page in a <frame>, <iframe>, <embed> or <object>. Sites can use this to
    avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.
    """

    def __init__(
        self, should_deny: bool = True, should_allow_sameorigin: bool = False, **kwargs
    ):
        pass


class XXssProtection(CustomHeader):
    """
    The HTTP X-XSS-Protection response header is a feature of Internet Explorer, Chrome and Safari that
    stops pages from loading when they detect reflected cross-site scripting (XSS) attacks.
    Although these protections are largely unnecessary in modern browsers when sites implement a strong
    Content-Security-Policy that disables the use of inline JavaScript
    """

    __tags__: List[str] = ["response"]

    def __init__(
        self,
        enable_filtering: bool = True,
        enable_block_rendering: bool = False,
        report_uri: Optional[str] = None,
        **kwargs,
    ):
        """
        :param enable_filtering: Enables XSS filtering (usually default in browsers). If a cross-site scripting attack is detected, the browser will sanitize the page (remove the unsafe parts).
        :param enable_block_rendering: Rather than sanitizing the page, the browser will prevent rendering of the page if an attack is detected.
        :param report_uri: (Chromium only) If a cross-site scripting attack is detected, the browser will sanitize the page and report the violation. This uses the functionality of the CSP report-uri directive to send a report.
        :param kwargs:
        """
        pass


class WwwAuthenticate(CustomHeader):
    """
    The HTTP WWW-Authenticate response header defines the authentication
    method that should be used to gain access to a resource.
    """

    def __init__(
        self, auth_type: str, realm: str, charset: Optional[str] = None, **kwargs
    ):
        pass
