# Build headers

This library also permits you to create headers using ready-to-use classes.

## Use it for your HTTP request

```python
from kiss_headers import Headers, Authorization
from requests import get

response = get("https://httpbin.org/bearer", headers=Headers(Authorization("Bearer", "qwerty")))
print(response.status_code)  # 200
```

## Create raw headers from objects

```python
from kiss_headers import *

headers = (
    Host("developer.mozilla.org")
    + UserAgent(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0"
    )
    + Accept("text/html")
    + Accept("application/xhtml+xml")
    + Accept("application/xml", qualifier=0.9)
    + Accept(qualifier=0.8)
    + AcceptLanguage("en-US")
    + AcceptLanguage("en", qualifier=0.5)
    + AcceptEncoding("gzip")
    + AcceptEncoding("deflate")
    + AcceptEncoding("br")
    + Referer("https://developer.mozilla.org/testpage.html")
    + Connection(should_keep_alive=True)
    + UpgradeInsecureRequests()
    + IfModifiedSince("Mon, 18 Jul 2016 02:36:04 GMT")
    + IfNoneMatch("c561c68d0ba92bbeb8b0fff2a9199f722e3a621a")
    + CacheControl(max_age=0)
)

raw_headers = str(headers)
```

`raw_headers` now retain the following :

```
Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html, application/xhtml+xml, application/xml; q="0.9", */*; q="0.8"
Accept-Language: en-US, en; q="0.5"
Accept-Encoding: gzip, deflate, br
Referer: https://developer.mozilla.org/testpage.html
Connection: keep-alive
Upgrade-Insecure-Requests: 1
If-Modified-Since: Mon, 18 Jul 2016 02:36:04 GMT
If-None-Match: "c561c68d0ba92bbeb8b0fff2a9199f722e3a621a"
Cache-Control: max-age="0"
```

See the complete list of available header class in the full documentation. 

## Create yours

Also, you can create your own custom header object using the class `kiss_headers.CustomHeader`.

```python
from kiss_headers import CustomHeader

class MyExtraHeader(CustomHeader):
    """My extra header purpose is to..."""
    
    __squash__ = False  # Determine if multiple instance of MyExtraHeader should be squashed into one entry using coma.
    __override__ = None # Replace it by a string if the default "class to header name" does suit you.  
    # Here MyExtraHeader class would be named 'My-Extra-Header'.

    def __init__(self, checksum: str, param_1: str):
        super().__init__(checksum, **{"param_1": param_1})
```

Now you can instance `MyExtraHeader` like this :

```python
header = MyExtraHeader("azerty", param_1="abc")
repr(header)  # output: 'My-Extra-Header: azerty; param_1="abc"'
```

!!! note
    You can implement your own methods in a `CustomHeader` subclass but you cannot create properties, attributes as this behavior  (get/set) is overridden by the library.
