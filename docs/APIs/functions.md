# Module `kiss_headers.api` {#kiss_headers.api}

## Functions

### Function `explain` {#kiss_headers.api.explain}

> `def explain(headers: kiss_headers.models.Headers) -> kiss_headers.structures.CaseInsensitiveDict`

Return a brief explanation of each header present in headers if available.

### Function `get_polymorphic` {#kiss_headers.api.get_polymorphic}

> `def get_polymorphic(target: Union[kiss_headers.models.Headers, kiss_headers.models.Header], desired_output: Type[~T]) -> Union[~T, List[~T], NoneType]`

Experimental. Transform an Header or Headers object to its target <code>CustomHeader</code> subclass
in order to access more ready-to-use methods. eg. You have an Header object named 'Set-Cookie' and you wish
to extract the expiration date as a datetime.

```python
header = Header("Set-Cookie", "1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT")
header["expires"]
'Wed, 15-Apr-2020 21:27:31 GMT'
from kiss_headers import SetCookie
set_cookie = get_polymorphic(header, SetCookie)
set_cookie.get_expire()
datetime.datetime(2020, 4, 15, 21, 27, 31, tzinfo=datetime.timezone.utc)
```

### Function `parse_it` {#kiss_headers.api.parse_it}

> `def parse_it(raw_headers: Any) -> kiss_headers.models.Headers`


Just decode anything that could contain headers. That simple PERIOD.
:param raw_headers: Accept bytes, str, fp, dict, email.Message, requests.Response, urllib3.HTTPResponse and httpx.Response.
:raises:
    TypeError: If passed argument cannot be parsed to extract headers from it.


