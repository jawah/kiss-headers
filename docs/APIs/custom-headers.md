# Module `kiss_headers.builder` {#kiss_headers.builder}








## Classes



### Class `Accept` {#kiss_headers.builder.Accept}



> `class Accept(mime: str = '*/*', qualifier: float = 1.0, **kwargs: Union[str, NoneType])`


The Accept request HTTP header advertises which content types, expressed as MIME types,
the client is able to understand. Using content negotiation, the server then selects one of
the proposals, uses it and informs the client of its choice with the Content-Type response header.

:param mime: Describe the MIME using this syntax <MIME_type/MIME_subtype>
:param qualifier: Any value used is placed in an order of preference expressed using relative quality value called the weight.
:param kwargs:
```python
header = Accept("text/html", qualifier=0.8)
header.content
'text/html; q="0.8"'
repr(header)
'Accept: text/html; q="0.8"'
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_mime` {#kiss_headers.builder.Accept.get_mime}




> `def get_mime(self) -> Union[str, NoneType]`


Return defined mime in current accept header.


##### Method `get_qualifier` {#kiss_headers.builder.Accept.get_qualifier}




> `def get_qualifier(self) -> Union[float, NoneType]`


Return defined qualifier for specified mime. If not set, output 1.0.


### Class `AcceptEncoding` {#kiss_headers.builder.AcceptEncoding}



> `class AcceptEncoding(method: str, qualifier: float = 1.0, **kwargs: Union[str, NoneType])`


The Accept-Encoding request HTTP header advertises which content encoding, usually a compression algorithm,
the client is able to understand. Using content negotiation, the server selects one of the proposals,
uses it and informs the client of its choice with the Content-Encoding response header.

:param method: Either chunked, compress, deflate, gzip, identity, br or a wildcard.
:param qualifier: Any value used is placed in an order of preference expressed using relative quality value called the weight.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.TransferEncoding](#kiss_headers.builder.TransferEncoding)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_qualifier` {#kiss_headers.builder.AcceptEncoding.get_qualifier}




> `def get_qualifier(self) -> Union[float, NoneType]`


Return defined qualifier for specified encoding. If not set, output 1.0.


### Class `AcceptLanguage` {#kiss_headers.builder.AcceptLanguage}



> `class AcceptLanguage(language: str = '*', qualifier: float = 1.0, **kwargs: Union[str, NoneType])`


The Accept-Language request HTTP header advertises which languages the client is able to understand,
and which locale variant is preferred. (By languages, we mean natural languages,
such as English, and not programming languages.)

:param language: A language tag (which is sometimes referred to as a "locale identifier"). This consists of a 2-3 letter base language tag representing the language.
:param qualifier: Any value placed in an order of preference expressed using a relative quality value called weight.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_qualifier` {#kiss_headers.builder.AcceptLanguage.get_qualifier}




> `def get_qualifier(self) -> Union[float, NoneType]`


Return defined qualifier for specified language. If not set, output 1.0.


### Class `Allow` {#kiss_headers.builder.Allow}



> `class Allow(supported_verb: str, **kwargs: Union[str, NoneType])`


The Allow header lists the set of methods supported by a resource.

:param supported_verb: Choose exactly one of "HEAD", "GET", "POST", "PUT", "PATCH", "DELETE", "PURGE", "CONNECT" or "TRACE" HTTP verbs.
:param kwargs:
```python
header = Allow("POST")
repr(header)
'Allow: POST'
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `AltSvc` {#kiss_headers.builder.AltSvc}



> `class AltSvc(protocol_id: str, alt_authority: str, max_age: Union[int, NoneType] = None, versions: Union[List[str], NoneType] = None, do_persist: Union[bool, NoneType] = None, **kwargs: Union[str, NoneType])`


The Alt-Svc HTTP response header is used to advertise alternative services through which
the same resource can be reached. An alternative service is defined by a protocol/host/port combination.

:param protocol_id: The ALPN protocol identifier. Examples include h2 for HTTP/2 and h3-25 for draft 25 of the HTTP/3 protocol.
:param alt_authority: The quoted string specifying the alternative authority which consists of an optional host override, a colon, and a mandatory port number.
:param max_age: The number of seconds for which the alternative service is considered fresh. If omitted, it defaults to 24 hours.
:param versions: List of supported versions of the protocol id if the protocol id can be ambiguous. (like QUIC)
:param do_persist: Use the parameter to ensures that the entry is not deleted through network configuration changes.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_alt_authority` {#kiss_headers.builder.AltSvc.get_alt_authority}




> `def get_alt_authority(self) -> str`


Extract the alternative authority which consists of an optional host override, a colon, and a mandatory port number.


##### Method `get_max_age` {#kiss_headers.builder.AltSvc.get_max_age}




> `def get_max_age(self) -> Union[int, NoneType]`


Output the number of seconds for which the alternative service is considered fresh. None if undefined.


##### Method `get_protocol_id` {#kiss_headers.builder.AltSvc.get_protocol_id}




> `def get_protocol_id(self) -> str`


Get the ALPN protocol identifier.


##### Method `get_versions` {#kiss_headers.builder.AltSvc.get_versions}




> `def get_versions(self) -> Union[List[str], NoneType]`


May return, if available, a list of versions of the ALPN protocol identifier.


##### Method `should_persist` {#kiss_headers.builder.AltSvc.should_persist}




> `def should_persist(self) -> Union[bool, NoneType]`


Verify if the entry should not be deleted through network configuration changes. None if no indication.


### Class `Authorization` {#kiss_headers.builder.Authorization}



> `class Authorization(type_: str, credentials: str, **kwargs: Union[str, NoneType])`


The HTTP Authorization request header contains the credentials to authenticate a user agent with a server,
usually, but not necessarily, after the server has responded with a 401 Unauthorized status
and the WWW-Authenticate header.

:param type_: Authentication type. A common type is "Basic". See IANA registry of Authentication schemes for others.
:param credentials: Associated credentials to use. Preferably Base-64 encoded.
```python
header = Authorization("Bearer", "base64encoded")
repr(header)
'Authorization: Bearer base64encoded'
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)



#### Descendants

* [kiss_headers.builder.BasicAuthorization](#kiss_headers.builder.BasicAuthorization)
* [kiss_headers.builder.ProxyAuthorization](#kiss_headers.builder.ProxyAuthorization)






#### Methods



##### Method `get_auth_type` {#kiss_headers.builder.Authorization.get_auth_type}




> `def get_auth_type(self) -> str`


Return the auth type used in Authorization.


##### Method `get_credentials` {#kiss_headers.builder.Authorization.get_credentials}




> `def get_credentials(self) -> str`


Output the credentials.


### Class `BasicAuthorization` {#kiss_headers.builder.BasicAuthorization}



> `class BasicAuthorization(username: str, password: str, charset: str = 'latin1', **kwargs: Union[str, NoneType])`


Same as Authorization header but simplified for the Basic method. Also an example of __override__ usage.

:param username:
:param password:
:param charset: By default, credentials are encoded using latin1 charset. You may want to choose otherwise.
:param kwargs:
```python
header = BasicAuthorization("azerty", "qwerty")
header
Authorization: Basic YXplcnR5OnF3ZXJ0eQ==
header.get_username_password()
('azerty', 'qwerty')
```




#### Ancestors (in MRO)

* [kiss_headers.builder.Authorization](#kiss_headers.builder.Authorization)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_credentials` {#kiss_headers.builder.BasicAuthorization.get_credentials}




> `def get_credentials(self) -> str`


Decode base64 encoded credentials from Authorization header.


##### Method `get_username_password` {#kiss_headers.builder.BasicAuthorization.get_username_password}




> `def get_username_password(self) -> Tuple[str, ...]`


Extract username and password as a tuple from Basic Authorization.


### Class `CacheControl` {#kiss_headers.builder.CacheControl}



> `class CacheControl(directive: Union[str, NoneType] = None, max_age: Union[int, NoneType] = None, max_stale: Union[int, NoneType] = None, min_fresh: Union[int, NoneType] = None, s_maxage: Union[int, NoneType] = None, **kwargs: Union[str, NoneType])`


The Cache-Control HTTP header holds directives (instructions) for caching in
both requests and responses. A given directive in a request does not mean the
same directive should be in the response.

Pass only one parameter per CacheControl instance.
:param directive: Could be one of must-revalidate, no-cache, no-store, no-transform, public, private, proxy-revalidate, only-if-cached, no-transform.
:param max_age: The maximum amount of time a resource is considered fresh. Unlike Expires, this directive is relative to the time of the request.
:param max_stale: Indicates the client will accept a stale response. An optional value in seconds indicates the upper limit of staleness the client will accept.
:param min_fresh: Indicates the client wants a response that will still be fresh for at least the specified number of seconds.
:param s_maxage: Overrides max-age or the Expires header, but only for shared caches (e.g., proxies). Ignored by private caches.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Connection` {#kiss_headers.builder.Connection}



> `class Connection(should_keep_alive: bool, **kwargs: Union[str, NoneType])`


The Connection general header controls whether or not the network connection stays open after the current transaction finishes.
If the value sent is keep-alive, the connection is persistent and not closed, allowing for subsequent requests to the same server to be done.

:param should_keep_alive: Indicates that the client would like to keep the connection open or not.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `ContentDisposition` {#kiss_headers.builder.ContentDisposition}



> `class ContentDisposition(disposition: str = 'inline', name: Union[str, NoneType] = None, filename: Union[str, NoneType] = None, fallback_filename: Union[str, NoneType] = None, boundary: Union[str, NoneType] = None, **kwargs: Union[str, NoneType])`


In a regular HTTP response, the Content-Disposition response header is a header indicating
if the content is expected to be displayed inline in the browser, that is, as a Web page or
as part of a Web page, or as an attachment, that is downloaded and saved locally.

:param disposition: Could be either inline, form-data, attachment or empty. Choose one. Default to inline.
:param name: Is a string containing the name of the HTML field in the form that the content of this subpart refers to.
:param filename: Is a string containing the original name of the file transmitted. The filename is always optional and must not be used blindly by the application. ASCII-US Only.
:param fallback_filename: Fallback filename if filename parameter does not uses the encoding defined in RFC 5987.
:param boundary: For multipart entities the boundary directive is required, which consists of 1 to 70 characters from a set of characters known to be very robust through email gateways, and not ending with white space. It is used to encapsulate the boundaries of the multiple parts of the message.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `ContentEncoding` {#kiss_headers.builder.ContentEncoding}



> `class ContentEncoding(method: str, **kwargs: Union[str, NoneType])`


The Content-Encoding entity header is used to compress the media-type. When present,
its value indicates which encodings were applied to the entity-body. It lets the client
know how to decode in order to obtain the media-type referenced by the Content-Type header.

If multiple, keep them in the order in which they were applied.

:param method: Either chunked, compress, deflate, gzip, identity or br.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.TransferEncoding](#kiss_headers.builder.TransferEncoding)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `ContentLength` {#kiss_headers.builder.ContentLength}



> `class ContentLength(length: int, **kwargs: Union[str, NoneType])`


The Content-Length entity header indicates the size of the entity-body, in bytes, sent to the recipient.

:param length: The length in decimal number of octets.



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `ContentRange` {#kiss_headers.builder.ContentRange}



> `class ContentRange(unit: str, start: int, end: int, size: Union[str, int], **kwargs: Union[str, NoneType])`


The Content-Range response HTTP header indicates where in a full body message a partial message belongs.

:param unit: The unit in which ranges is specified. This is usually bytes.
:param start: An integer in the given unit indicating the beginning of the request range.
:param end: An integer in the given unit indicating the end of the requested range.
:param size: The total size of the document (or '*' if unknown).
:param kwargs:
```python
header = ContentRange("bytes", 0, 1024, 4096)
repr(header)
'Content-Range: bytes 0-1024/4096'
header.get_size()
4096
header.unpack()
('bytes', '0', '1024', '4096')
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_end` {#kiss_headers.builder.ContentRange.get_end}




> `def get_end(self) -> int`


Get the end of the requested range.


##### Method `get_size` {#kiss_headers.builder.ContentRange.get_size}




> `def get_size(self) -> Union[str, int]`


Get the total size of the document (or '*' if unknown).


##### Method `get_start` {#kiss_headers.builder.ContentRange.get_start}




> `def get_start(self) -> int`


Get the beginning of the request range.


##### Method `get_unit` {#kiss_headers.builder.ContentRange.get_unit}




> `def get_unit(self) -> str`


Retrieve the unit in which ranges is specified.


##### Method `unpack` {#kiss_headers.builder.ContentRange.unpack}




> `def unpack(self) -> Tuple[str, str, str, str]`


Provide a basic way to parse ContentRange format.


### Class `ContentSecurityPolicy` {#kiss_headers.builder.ContentSecurityPolicy}



> `class ContentSecurityPolicy(*policies: List[str])`


Content-Security-Policy is the name of a HTTP response header
that modern browsers use to enhance the security of the document (or web page).
The Content-Security-Policy header allows you to restrict how resources such as
JavaScript, CSS, or pretty much anything that the browser loads.

:param policies: One policy consist of a list of str like ["default-src", "'none'"].
```python
header = ContentSecurityPolicy(["default-src", "'none'"], ["img-src", "'self'", "img.example.com"])
repr(header)
"Content-Security-Policy: default-src 'none'; img-src 'self' img.example.com"
header.get_policies_names()
['default-src', 'img-src']
header.get_policy_args("img-src")
["'self'", 'img.example.com']
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_policies_names` {#kiss_headers.builder.ContentSecurityPolicy.get_policies_names}




> `def get_policies_names(self) -> List[str]`


Fetch a list of policy name set in content.


##### Method `get_policy_args` {#kiss_headers.builder.ContentSecurityPolicy.get_policy_args}




> `def get_policy_args(self, policy_name: str) -> Union[List[str], NoneType]`


Retrieve given arguments for a policy.


### Class `ContentType` {#kiss_headers.builder.ContentType}



> `class ContentType(mime: str, charset: Union[str, NoneType] = None, format_: Union[str, NoneType] = None, boundary: Union[str, NoneType] = None, **kwargs: Union[str, NoneType])`


The Content-Type entity header is used to indicate the media type of the resource.

In responses, a Content-Type header tells the client what the content type of the returned content actually is.
Browsers will do MIME sniffing in some cases and will not necessarily follow the value of this header;
to prevent this behavior, the header X-Content-Type-Options can be set to nosniff.

:param mime_type: The MIME type of the resource or the data. Format <MIME_type>/<MIME_subtype>.
:param charset: The character encoding standard. Should be an IANA name.
:param format_: Mostly used in IMAP, could be one of : original or flowed.
:param boundary: For multipart entities the boundary directive is required, which consists of 1 to 70 characters from a set of characters known to be very robust through email gateways, and not ending with white space. It is used to encapsulate the boundaries of the multiple parts of the message.
:param kwargs:
```python
header = ContentType("text/html", charset="utf-8")
repr(header)
'Content-Type: text/html; charset="UTF-8"'
header.get_charset()
'UTF-8'
header.get_mime()
'text/html'
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_charset` {#kiss_headers.builder.ContentType.get_charset}




> `def get_charset(self) -> Union[str, NoneType]`


Extract defined charset, if not present will return 'ISO-8859-1' by default.


##### Method `get_mime` {#kiss_headers.builder.ContentType.get_mime}




> `def get_mime(self) -> Union[str, NoneType]`


Return defined mime in content type.


### Class `Cookie` {#kiss_headers.builder.Cookie}



> `class Cookie(**kwargs: Union[str, NoneType])`


The Cookie HTTP request header contains stored HTTP cookies previously sent by
the server with the Set-Cookie header.

:param kwargs: Pair of cookie name associated with a value.



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_cookie_value` {#kiss_headers.builder.Cookie.get_cookie_value}




> `def get_cookie_value(self, cookie_name: str) -> Union[str, NoneType]`


Retrieve associated value with a given cookie name.


##### Method `get_cookies_names` {#kiss_headers.builder.Cookie.get_cookies_names}




> `def get_cookies_names(self) -> List[str]`


Retrieve all defined cookie names from Cookie header.


### Class `CrossOriginResourcePolicy` {#kiss_headers.builder.CrossOriginResourcePolicy}



> `class CrossOriginResourcePolicy(policy: str, **kwargs: Union[str, NoneType])`


The HTTP Cross-Origin-Resource-Policy response header conveys a desire that
the browser blocks no-cors cross-origin/cross-site requests to the given resource.

:param policy: Accepted values are same-site, same-origin or cross-origin.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `CustomHeader` {#kiss_headers.builder.CustomHeader}



> `class CustomHeader(initial_content: str = '', **kwargs: Union[str, NoneType])`


This class is a helper to create ready-to-use Header object with creation assistance.
Should NOT be instantiated.
Use this class as a direct parent for creating ready-to-use header object. Inspire yourself with already defined
class bellow this one.

:param initial_content: Initial content of the Header if any.
:param kwargs: Provided args. Any key that associate a None value are just ignored.



#### Ancestors (in MRO)

* [kiss_headers.models.Header](#kiss_headers.models.Header)



#### Descendants

* [kiss_headers.builder.Accept](#kiss_headers.builder.Accept)
* [kiss_headers.builder.AcceptLanguage](#kiss_headers.builder.AcceptLanguage)
* [kiss_headers.builder.Allow](#kiss_headers.builder.Allow)
* [kiss_headers.builder.AltSvc](#kiss_headers.builder.AltSvc)
* [kiss_headers.builder.Authorization](#kiss_headers.builder.Authorization)
* [kiss_headers.builder.CacheControl](#kiss_headers.builder.CacheControl)
* [kiss_headers.builder.Connection](#kiss_headers.builder.Connection)
* [kiss_headers.builder.ContentDisposition](#kiss_headers.builder.ContentDisposition)
* [kiss_headers.builder.ContentLength](#kiss_headers.builder.ContentLength)
* [kiss_headers.builder.ContentRange](#kiss_headers.builder.ContentRange)
* [kiss_headers.builder.ContentSecurityPolicy](#kiss_headers.builder.ContentSecurityPolicy)
* [kiss_headers.builder.ContentType](#kiss_headers.builder.ContentType)
* [kiss_headers.builder.Cookie](#kiss_headers.builder.Cookie)
* [kiss_headers.builder.CrossOriginResourcePolicy](#kiss_headers.builder.CrossOriginResourcePolicy)
* [kiss_headers.builder.Date](#kiss_headers.builder.Date)
* [kiss_headers.builder.Digest](#kiss_headers.builder.Digest)
* [kiss_headers.builder.Dnt](#kiss_headers.builder.Dnt)
* [kiss_headers.builder.Etag](#kiss_headers.builder.Etag)
* [kiss_headers.builder.Forwarded](#kiss_headers.builder.Forwarded)
* [kiss_headers.builder.From](#kiss_headers.builder.From)
* [kiss_headers.builder.Host](#kiss_headers.builder.Host)
* [kiss_headers.builder.IfMatch](#kiss_headers.builder.IfMatch)
* [kiss_headers.builder.KeepAlive](#kiss_headers.builder.KeepAlive)
* [kiss_headers.builder.Location](#kiss_headers.builder.Location)
* [kiss_headers.builder.Referer](#kiss_headers.builder.Referer)
* [kiss_headers.builder.ReferrerPolicy](#kiss_headers.builder.ReferrerPolicy)
* [kiss_headers.builder.Server](#kiss_headers.builder.Server)
* [kiss_headers.builder.SetCookie](#kiss_headers.builder.SetCookie)
* [kiss_headers.builder.StrictTransportSecurity](#kiss_headers.builder.StrictTransportSecurity)
* [kiss_headers.builder.TransferEncoding](#kiss_headers.builder.TransferEncoding)
* [kiss_headers.builder.UpgradeInsecureRequests](#kiss_headers.builder.UpgradeInsecureRequests)
* [kiss_headers.builder.UserAgent](#kiss_headers.builder.UserAgent)
* [kiss_headers.builder.Vary](#kiss_headers.builder.Vary)
* [kiss_headers.builder.WwwAuthenticate](#kiss_headers.builder.WwwAuthenticate)
* [kiss_headers.builder.XContentTypeOptions](#kiss_headers.builder.XContentTypeOptions)
* [kiss_headers.builder.XDnsPrefetchControl](#kiss_headers.builder.XDnsPrefetchControl)
* [kiss_headers.builder.XFrameOptions](#kiss_headers.builder.XFrameOptions)
* [kiss_headers.builder.XXssProtection](#kiss_headers.builder.XXssProtection)






### Class `Date` {#kiss_headers.builder.Date}



> `class Date(my_date: Union[datetime.datetime, str], **kwargs: Union[str, NoneType])`


The Date general HTTP header contains the date and time at which the message was originated.

:param my_date: Can either be a datetime that will be automatically converted or a raw string.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)



#### Descendants

* [kiss_headers.builder.Expires](#kiss_headers.builder.Expires)
* [kiss_headers.builder.IfModifiedSince](#kiss_headers.builder.IfModifiedSince)
* [kiss_headers.builder.IfUnmodifiedSince](#kiss_headers.builder.IfUnmodifiedSince)
* [kiss_headers.builder.LastModified](#kiss_headers.builder.LastModified)
* [kiss_headers.builder.RetryAfter](#kiss_headers.builder.RetryAfter)






#### Methods



##### Method `get_datetime` {#kiss_headers.builder.Date.get_datetime}




> `def get_datetime(self) -> datetime.datetime`


Parse and return a datetime according to content.


### Class `Digest` {#kiss_headers.builder.Digest}



> `class Digest(algorithm: str, value: str, **kwargs: Union[str, NoneType])`


The Digest response HTTP header provides a digest of the requested resource. RFC 7231.

:param algorithm: Supported digest algorithms are defined in RFC 3230 and RFC 5843, and include SHA-256 and SHA-512.
:param value: The result of applying the digest algorithm to the resource representation and encoding the result.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Dnt` {#kiss_headers.builder.Dnt}



> `class Dnt(tracking_consent: bool = False, **kwargs: Union[str, NoneType])`


The DNT (Do Not Track) request header indicates the user's tracking preference.
It lets users indicate whether they would prefer privacy rather than personalized content.

:param tracking_consent: The user prefers to allow tracking on the target site or not.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Etag` {#kiss_headers.builder.Etag}



> `class Etag(etag_value: str, is_a_weak_validator: bool = False, **kwargs: Union[str, NoneType])`


The ETag HTTP response header is an identifier for a specific version of a resource.
It lets caches be more efficient and save bandwidth, as a web server does not need to
resend a full response if the content has not changed.

:param etag_value: Entity tag uniquely representing the requested resource. ASCII string only. Not quoted.
:param is_a_weak_validator: Indicates that a weak validator is used. Weak etags are easy to generate, but are far less useful for comparisons.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Expires` {#kiss_headers.builder.Expires}



> `class Expires(datetime_or_custom: Union[datetime.datetime, str], **kwargs: Union[str, NoneType])`


The Expires header contains the date/time after which the response is considered stale.
Invalid dates, like the value 0, represent a date in the past and mean that the resource is already expired.

:param my_date: Can either be a datetime that will be automatically converted or a raw string.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.Date](#kiss_headers.builder.Date)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Forwarded` {#kiss_headers.builder.Forwarded}



> `class Forwarded(by: str, for_: str, using_proto: str, host: Union[str, NoneType] = None, **kwargs: Union[str, NoneType])`


The Forwarded header contains information from the client-facing side of proxy servers
that is altered or lost when a proxy is involved in the path of the request.

:param by: The interface where the request came in to the proxy server. Could be an IP address, an obfuscated identifier or "unknown".
:param for_: The client that initiated the request and subsequent proxies in a chain of proxies.
:param host: The Host request header field as received by the proxy.
:param using_proto: Indicates which protocol was used to make the request (typically "http" or "https").
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `From` {#kiss_headers.builder.From}



> `class From(email: str, **kwargs: Union[str, NoneType])`


The From request header contains an Internet email address for a human user who controls the requesting user agent.
If you are running a robotic user agent (e.g. a crawler), the From header should be sent, so you can be contacted
if problems occur on servers, such as if the robot is sending excessive, unwanted, or invalid requests.

:param email: A machine-usable email address. See RFC 5322.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Host` {#kiss_headers.builder.Host}



> `class Host(host: str, port: Union[int, NoneType] = None, **kwargs: Union[str, NoneType])`


The Host request header specifies the domain name of the server (for virtual hosting),
and (optionally) the TCP port number on which the server is listening.

:param host: The domain name of the server (for virtual hosting).
:param port: TCP port number on which the server is listening.
```python
header = Host("www.python.org")
repr(header)
'Host: www.python.org'
header = Host("www.python.org", port=8000)
repr(header)
'Host: www.python.org:8000'
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `IfMatch` {#kiss_headers.builder.IfMatch}



> `class IfMatch(etag_value: str, **kwargs: Union[str, NoneType])`


The If-Match HTTP request header makes the request conditional. For GET and HEAD methods,
the server will send back the requested resource only if it matches one of the listed ETags.
For PUT and other non-safe methods, it will only upload the resource in this case.

:param etag_value: Entity tags uniquely representing the requested resources. They are a string of ASCII characters placed between double quotes (like "675af34563dc-tr34").
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)



#### Descendants

* [kiss_headers.builder.IfNoneMatch](#kiss_headers.builder.IfNoneMatch)






### Class `IfModifiedSince` {#kiss_headers.builder.IfModifiedSince}



> `class IfModifiedSince(dt: Union[datetime.datetime, str], **kwargs: Union[str, NoneType])`


The If-Modified-Since request HTTP header makes the request conditional

:param dt:
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.Date](#kiss_headers.builder.Date)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `IfNoneMatch` {#kiss_headers.builder.IfNoneMatch}



> `class IfNoneMatch(etag_value: str, **kwargs: Union[str, NoneType])`


The If-None-Match HTTP request header makes the request conditional. For GET and HEAD methods,
the server will send back the requested resource, with a 200 status, only if it doesn't have an ETag matching
the given ones. For other methods, the request will be processed only if the eventually existing resource's
ETag doesn't match any of the values listed.

:param etag_value: Entity tags uniquely representing the requested resources. They are a string of ASCII characters placed between double quotes (like "675af34563dc-tr34").
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.IfMatch](#kiss_headers.builder.IfMatch)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `IfUnmodifiedSince` {#kiss_headers.builder.IfUnmodifiedSince}



> `class IfUnmodifiedSince(dt: Union[datetime.datetime, str], **kwargs: Union[str, NoneType])`


The If-Unmodified-Since request HTTP header makes the request conditional

:param dt:
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.Date](#kiss_headers.builder.Date)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `KeepAlive` {#kiss_headers.builder.KeepAlive}



> `class KeepAlive(timeout: Union[int, NoneType] = None, max_: Union[int, NoneType] = None, **kwargs: Union[str, NoneType])`


The Keep-Alive general header allows the sender to hint about how the connection may be used to
set a timeout and a maximum amount of requests.

:param timeout: indicating the minimum amount of time an idle connection has to be kept opened (in seconds).
:param max: indicating the maximum number of requests that can be sent on this connection before closing it.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `LastModified` {#kiss_headers.builder.LastModified}



> `class LastModified(my_date: Union[datetime.datetime, str], **kwargs: Union[str, NoneType])`


The Last-Modified response HTTP header contains the date and time at which the origin server
believes the resource was last modified. It is used as a validator
to determine if a resource received or stored is the same.

:param my_date:
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.Date](#kiss_headers.builder.Date)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Location` {#kiss_headers.builder.Location}



> `class Location(uri: str, **kwargs: Union[str, NoneType])`


The Location response header indicates the URL to redirect a page to.
It only provides a meaning when served with a 3xx (redirection) or 201 (created) status response.

:param uri: A relative (to the request URL) or absolute URL.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `ProxyAuthorization` {#kiss_headers.builder.ProxyAuthorization}



> `class ProxyAuthorization(type_: str, credentials: str)`


The HTTP Proxy-Authorization request header contains the credentials to authenticate a user agent to a proxy server,
usually after the server has responded with a 407 Proxy Authentication Required status
and the Proxy-Authenticate header.

:param type_: Authentication type. A common type is "Basic". See IANA registry of Authentication schemes for others.
:param credentials: Associated credentials to use. Preferably Base-64 encoded.



#### Ancestors (in MRO)

* [kiss_headers.builder.Authorization](#kiss_headers.builder.Authorization)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Referer` {#kiss_headers.builder.Referer}



> `class Referer(url: str, **kwargs: Union[str, NoneType])`


The Referer request header contains the address of the previous web page from which a link to the currently
requested page was followed. The Referer header allows servers to identify where people are
visiting them from and may use that data for analytics, logging, or optimized caching, for example.

Note that referer is actually a misspelling of the word "referrer". See <https://en.wikipedia.org/wiki/HTTP_referer>

:param url: An absolute or partial address of the previous web page from which a link to the currently requested page was followed. URL fragments not included.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `ReferrerPolicy` {#kiss_headers.builder.ReferrerPolicy}



> `class ReferrerPolicy(policy: str, **kwargs: Union[str, NoneType])`


The Referrer-Policy HTTP header controls how much referrer information
(sent via the Referer header) should be included with requests.

:param policy: Either "no-referrer", "no-referrer-when-downgrade", "origin", "origin-when-cross-origin", "same-origin", "strict-origin", "strict-origin-when-cross-origin", "unsafe-url"
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `RetryAfter` {#kiss_headers.builder.RetryAfter}



> `class RetryAfter(delay_or_date: Union[datetime.datetime, int], **kwargs: Union[str, NoneType])`


The Retry-After response HTTP header indicates how long the user agent should wait
before making a follow-up request.

:param my_date: Can either be a datetime that will be automatically converted or a raw string.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.Date](#kiss_headers.builder.Date)
* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Server` {#kiss_headers.builder.Server}



> `class Server(product: str, **kwargs: Union[str, NoneType])`


The Server header describes the software used by the origin server that handled the request —
that is, the server that generated the response.

:param product: The name of the software or product that handled the request. Usually in a format similar to User-Agent.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `SetCookie` {#kiss_headers.builder.SetCookie}



> `class SetCookie(cookie_name: str, cookie_value: str, expires: Union[datetime.datetime, str, NoneType] = None, max_age: Union[int, NoneType] = None, domain: Union[str, NoneType] = None, path: Union[str, NoneType] = None, samesite: Union[str, NoneType] = None, is_secure: bool = False, is_httponly: bool = True, **kwargs: Union[str, NoneType])`


The Set-Cookie HTTP response header is used to send cookies from the server to the user agent,
so the user agent can send them back to the server later.

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



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_cookie_name` {#kiss_headers.builder.SetCookie.get_cookie_name}




> `def get_cookie_name(self) -> str`


Extract the cookie name.


##### Method `get_cookie_value` {#kiss_headers.builder.SetCookie.get_cookie_value}




> `def get_cookie_value(self) -> str`


Extract the cookie value.


##### Method `get_expire` {#kiss_headers.builder.SetCookie.get_expire}




> `def get_expire(self) -> Union[datetime.datetime, NoneType]`


Retrieve the parsed expiration date.


##### Method `get_max_age` {#kiss_headers.builder.SetCookie.get_max_age}




> `def get_max_age(self) -> Union[int, NoneType]`


Getting the max-age value as an integer if set.


##### Method `is_http_only` {#kiss_headers.builder.SetCookie.is_http_only}




> `def is_http_only(self) -> bool`


Determine if the cookie can only be accessed by the browser.


##### Method `is_secure` {#kiss_headers.builder.SetCookie.is_secure}




> `def is_secure(self) -> bool`


Determine if the cookie is TLS/SSL only.


### Class `StrictTransportSecurity` {#kiss_headers.builder.StrictTransportSecurity}



> `class StrictTransportSecurity(max_age: int, does_includesubdomains: bool = False, is_preload: bool = False, **kwargs: Union[str, NoneType])`


The HTTP Strict-Transport-Security response header (often abbreviated as HSTS) lets a web site
tell browsers that it should only be accessed using HTTPS, instead of using HTTP.

:param max_age: The time, in seconds, that the browser should remember that a site is only to be accessed using HTTPS.
:param does_includesubdomains: If this optional parameter is specified, this rule applies to all of the site's subdomains as well.
:param is_preload: Preloading Strict Transport Security. Google maintains an HSTS preload service. By following the guidelines and successfully submitting your domain, browsers will never connect to your domain using an insecure connection.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `does_includesubdomains` {#kiss_headers.builder.StrictTransportSecurity.does_includesubdomains}




> `def does_includesubdomains(self) -> bool`


Verify if this rule applies to all of the site's subdomains.


##### Method `get_max_age` {#kiss_headers.builder.StrictTransportSecurity.get_max_age}




> `def get_max_age(self) -> Union[int, NoneType]`


Get the time, in seconds, if set, that the browser should remember.


##### Method `should_preload` {#kiss_headers.builder.StrictTransportSecurity.should_preload}




> `def should_preload(self) -> bool`


Verify if Preloading Strict Transport Security should be set.


### Class `TransferEncoding` {#kiss_headers.builder.TransferEncoding}



> `class TransferEncoding(method: str, **kwargs: Union[str, NoneType])`


The Transfer-Encoding header specifies the form of encoding used to safely transfer the payload body to the user.

:param method: Either chunked, compress, deflate, gzip, identity or br.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)



#### Descendants

* [kiss_headers.builder.AcceptEncoding](#kiss_headers.builder.AcceptEncoding)
* [kiss_headers.builder.ContentEncoding](#kiss_headers.builder.ContentEncoding)






### Class `UpgradeInsecureRequests` {#kiss_headers.builder.UpgradeInsecureRequests}



> `class UpgradeInsecureRequests(**kwargs: Union[str, NoneType])`


The HTTP Upgrade-Insecure-Requests request header sends a signal to the server expressing
the client’s preference for an encrypted and authenticated response, and that it
can successfully handle the upgrade-insecure-requests CSP directive.

:param initial_content: Initial content of the Header if any.
:param kwargs: Provided args. Any key that associate a None value are just ignored.



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `UserAgent` {#kiss_headers.builder.UserAgent}



> `class UserAgent(characteristics: str, **kwargs: Union[str, NoneType])`


The User-Agent request header is a characteristic string that lets servers and network
peers identify the application, operating system, vendor, and/or version of the requesting user agent.

:param initial_content: Initial content of the Header if any.
:param kwargs: Provided args. Any key that associate a None value are just ignored.



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `Vary` {#kiss_headers.builder.Vary}



> `class Vary(header_name: str, **kwargs: Union[str, NoneType])`


The Vary HTTP response header determines how to match future request headers to decide whether a cached response
can be used rather than requesting a fresh one from the origin server.

:param header_name: An header name to take into account when deciding whether or not a cached response can be used.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `WwwAuthenticate` {#kiss_headers.builder.WwwAuthenticate}



> `class WwwAuthenticate(auth_type: Union[str, NoneType] = None, challenge: str = 'realm', value: str = 'Secured area', **kwargs: Union[str, NoneType])`


The HTTP WWW-Authenticate response header defines the authentication
method that should be used to gain access to a resource.
Fair-Warning : This header is like none other and is harder to parse. It need a specific case.

```python
www_authenticate = WwwAuthenticate("Basic", "realm", "Secured area")
repr(www_authenticate)
'Www-Authenticate: Basic realm="Secured area"'
headers = www_authenticate + WwwAuthenticate(challenge="charset", value="UTF-8")
repr(headers)
'Www-Authenticate: Basic realm="Secured area", charset="UTF-8"'
www_authenticate.get_challenge()
('realm', 'Secured area')
www_authenticate.get_auth_type()
'Basic'
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







#### Methods



##### Method `get_auth_type` {#kiss_headers.builder.WwwAuthenticate.get_auth_type}




> `def get_auth_type(self) -> Union[str, NoneType]`


Retrieve given authentication method if defined.


##### Method `get_challenge` {#kiss_headers.builder.WwwAuthenticate.get_challenge}




> `def get_challenge(self) -> Tuple[str, str]`


Output a tuple containing the challenge and the associated value. Raises :ValueError:


### Class `XContentTypeOptions` {#kiss_headers.builder.XContentTypeOptions}



> `class XContentTypeOptions(nosniff: bool = True, **kwargs: Union[str, NoneType])`


The X-Content-Type-Options response HTTP header is a marker used by the server to indicate that
the MIME types advertised in the Content-Type headers should not be changed and be followed.
This allows to opt-out of MIME type sniffing, or, in other words, it is a way to say that
the webmasters knew what they were doing.

:param nosniff: see <https://fetch.spec.whatwg.org/#x-content-type-options-header>
:param kwargs:
```python
header = XContentTypeOptions(nosniff=True)
repr(header)
'X-Content-Type-Options: nosniff'
```




#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `XDnsPrefetchControl` {#kiss_headers.builder.XDnsPrefetchControl}



> `class XDnsPrefetchControl(enable: bool = True, **kwargs: Union[str, NoneType])`


The X-DNS-Prefetch-Control HTTP response header controls DNS prefetching, a feature by which browsers proactively
perform domain name resolution on both links that the user may choose to follow as well as URLs
for items referenced by the document, including images, CSS, JavaScript, and so forth.

:param enable: Toggle the specified behaviour.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `XFrameOptions` {#kiss_headers.builder.XFrameOptions}



> `class XFrameOptions(policy: str, **kwargs: Union[str, NoneType])`


The X-Frame-Options HTTP response header can be used to indicate whether or not a browser
should be allowed to render a page in a <frame>, <iframe>, <embed> or <object>. Sites can use this to
avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.

:param policy: Can be either DENY or SAMEORIGIN.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)







### Class `XXssProtection` {#kiss_headers.builder.XXssProtection}



> `class XXssProtection(enable_filtering: bool = True, enable_block_rendering: bool = False, report_uri: Union[str, NoneType] = None, **kwargs: Union[str, NoneType])`


The HTTP X-XSS-Protection response header is a feature of Internet Explorer, Chrome and Safari that
stops pages from loading when they detect reflected cross-site scripting (XSS) attacks.
Although these protections are largely unnecessary in modern browsers when sites implement a strong
Content-Security-Policy that disables the use of inline JavaScript

:param enable_filtering: Enables XSS filtering (usually default in browsers). If a cross-site scripting attack is detected, the browser will sanitize the page (remove the unsafe parts).
:param enable_block_rendering: Rather than sanitizing the page, the browser will prevent rendering of the page if an attack is detected.
:param report_uri: (Chromium only) If a cross-site scripting attack is detected, the browser will sanitize the page and report the violation. This uses the functionality of the CSP report-uri directive to send a report.
:param kwargs:



#### Ancestors (in MRO)

* [kiss_headers.builder.CustomHeader](#kiss_headers.builder.CustomHeader)
* [kiss_headers.models.Header](#kiss_headers.models.Header)





