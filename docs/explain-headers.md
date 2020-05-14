# Explain Headers

This library ship with the function `explain()` that would allows you to get a short explanation for each distinct Header (On Name) 
in Headers.

```python
from kiss_headers import parse_it, explain
from requests import get
from pprint import pprint

if __name__ == "__main__":

    headers = parse_it(get("https://www.python.org"))
    pprint(explain(headers))
```

The function `explain` return a `CaseInsensibleDict`. Expected result from before code :

!!! hint
    Explanations are extracted from available docstring of subclasses of `Header`. If non-existent would return 'Unknown explanation.'

```text
{'Accept-Ranges': 'Unknown explanation.',
 'Age': 'Unknown explanation.',
 'Connection': 'The Connection general header controls whether or not the '
               'network connection stays open after the current transaction '
               'finishes.  If the value sent is keep-alive, the connection is '
               'persistent and not closed, allowing for subsequent requests to '
               'the same server to be done.',
 'Content-Length': 'The Content-Length entity header indicates the size of the '
                   'entity-body, in bytes, sent to the recipient.',
 'Content-Type': 'The Content-Type entity header is used to indicate the media '
                 'type of the resource.  In responses, a Content-Type header '
                 'tells the client what the content type of the returned '
                 'content actually is.  Browsers will do MIME sniffing in some '
                 'cases and will not necessarily follow the value of this '
                 'header;  to prevent this behavior, the header '
                 'X-Content-Type-Options can be set to nosniff.',
 'Date': 'The Date general HTTP header contains the date and time at which the '
         'message was originated.',
 'Server': 'The Server header describes the software used by the origin server '
           'that handled the request —  that is, the server that generated the '
           'response.',
 'Strict-Transport-Security': 'The HTTP Strict-Transport-Security response '
                              'header (often abbreviated as HSTS) lets a web '
                              'site  tell browsers that it should only be '
                              'accessed using HTTPS, instead of using HTTP.',
 'Vary': 'The Vary HTTP response header determines how to match future request '
         'headers to decide whether a cached response  can be used rather than '
         'requesting a fresh one from the origin server.',
 'Via': 'Unknown explanation.',
 'X-Cache': 'Unknown explanation.',
 'X-Cache-Hits': 'Unknown explanation.',
 'X-Frame-Options': 'The X-Frame-Options HTTP response header can be used to '
                    'indicate whether or not a browser  should be allowed to '
                    'render a page in a <frame>, <iframe>, <embed> or '
                    '<object>. Sites can use this to  avoid clickjacking '
                    'attacks, by ensuring that their content is not embedded '
                    'into other sites.',
 'X-Served-By': 'Unknown explanation.',
 'X-Timer': 'Unknown explanation.'}
```
