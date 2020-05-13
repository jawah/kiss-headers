# Polymorphism

Sometimes we get extra lazy, kiss-headers provide two bases classes, named `Header` and `Headers`. 
When handling `Header` object we might want to do more complex things than extracting an attribute value.

The library proposes more than 40+ ready-to-use custom `Header` subclasses with specifics methods associated.

## Transformation

Since version 2.1 you can transform an Header object to its target `CustomHeader` subclass in order to access more methods.

```python
from kiss_headers import parse_it, get_polymorphic, SetCookie

my_cookies = """set-cookie: 1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT; path=/; domain=.google.fr; Secure; SameSite=none
set-cookie: CONSENT=WP.284b10; expires=Fri, 01-Jan-2038 00:00:00 GMT; path=/; domain=.google.fr"""

headers = parse_it(my_cookies)

type(headers.set_cookie[0])  # output: Header

set_cookie = get_polymorphic(headers.set_cookie[0], SetCookie)

type(set_cookie)  # output: SetCookie

set_cookie.get_cookie_name()  # output: 1P_JAR
set_cookie.get_expire()  # output: datetime(...)
```

See complete list of supported subclasses in *Developer Interface*.