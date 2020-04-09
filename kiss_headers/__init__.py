"""
Kiss-Headers
~~~~~~~~~~~~~~

Kiss-Headers is a headers, HTTP or IMAP4 flavour, utility, written in Python, for humans.
Object oriented headers. Keep it simple and stupid.
Basic usage:

   >>> import requests
   >>> from kiss_headers import parse_it
   >>> r = requests.get('https://www.python.org')
   >>> headers = parse_it(r)
   >>> 'charset' in headers.content_type
   True
   >>> headers.content_type.charset
   'utf-8'
   >>> 'text/html' in headers.content_type
   True
   >>> headers.content_type == 'text/html'
   True
   >>> headers -= 'content-type'
   >>> 'Content-Type' in headers
   False

... or from a raw IMAP4 message:

   >>> message = open('my-email.eml', 'rb').read()
   >>> headers = parse_it(message)
   >>> 'Received' in headers
   True

Others methods and usages are available - see the full documentation
at <https://github.com/Ousret/kiss-headers>.

:copyright: (c) 2020 by Ahmed TAHRI
:license: MIT, see LICENSE for more details.
"""

from kiss_headers.models import Headers, Header, lock_output_type
from kiss_headers.api import parse_it, explain
from kiss_headers.builder import (
    CustomHeader,
    Accept,
    ContentType,
    XContentTypeOptions,
    ContentDisposition,
    Authorization,
    ProxyAuthorization,
    Host,
    Connection,
    ContentLength,
    Date,
    CrossOriginResourcePolicy,
    Allow,
    Digest,
    SetCookie,
    StrictTransportSecurity,
    UpgradeInsecureRequests,
    TransferEncoding,
    ContentEncoding,
    AcceptEncoding,
    Dnt,
    UserAgent,
    AltSvc,
    Forwarded,
    LastModified,
    Referer,
    ReferrerPolicy,
    RetryAfter,
    AcceptLanguage,
    Etag,
    XFrameOptions,
    XXssProtection,
    WwwAuthenticate,
    XDnsPrefetchControl,
    Location,
    From,
    ContentRange,
    CacheControl,
    Expires,
    IfModifiedSince,
    IfUnmodifiedSince,
    KeepAlive,
    IfMatch,
    IfNoneMatch,
    Server,
    Vary,
)
from kiss_headers.version import __version__, VERSION
