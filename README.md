<h1 align="center">Welcome to Headers for Humans 👋 <a href="https://twitter.com/intent/tweet?text=Python%20library%20for%20oriented%20object%20HTTP%20style%20headers.&url=https://www.github.com/Ousret/kiss-headers&hashtags=python,headers,opensource"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"/></a></h1>

<p align="center">
  <sup>Object oriented headers, parser and builder.</sup><br>
  <a href="https://travis-ci.org/Ousret/kiss-headers">
    <img src="https://travis-ci.org/Ousret/kiss-headers.svg?branch=master"/>
  </a>
  <a href='https://pypi.org/project/kiss-headers/'>
     <img src="https://img.shields.io/pypi/pyversions/kiss-headers.svg?orange=blue" />
  </a>
  <a href="https://www.codacy.com/manual/Ousret/kiss-headers?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Ousret/kiss-headers&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/0994a03546094b519601e33554c48535"/>
  </a>
  <a href="https://codecov.io/gh/Ousret/kiss-headers">
      <img src="https://codecov.io/gh/Ousret/kiss-headers/branch/master/graph/badge.svg" />
  </a>
  <a href='https://pypi.org/project/kiss-headers/'>
    <img src='https://badge.fury.io/py/kiss-headers.svg' alt='PyPi Publish Action' />
  </a>
  <a href="https://github.com/psf/black">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
  <a href="http://mypy-lang.org/">
    <img alt="Checked with mypy" src="http://www.mypy-lang.org/static/mypy_badge.svg"/>
  </a>
  <a href="https://pepy.tech/project/kiss-headers/">
     <img alt="Download Count Total" src="https://pepy.tech/badge/kiss-headers" />
  </a>
</p>

### ❓ Why

No matter if you are currently building software using HTTP or IMAP _(message, email)_, you should not worry about easily accessing header and associated attributes, adjectives or values.

<p align="center">
<img src="https://user-images.githubusercontent.com/9326700/77257881-55866300-6c77-11ea-820c-7550e6bdeee7.gif" alt="using kiss-headers from python interpreter"/>
</p>

I have seen so many chunks of code trying to deal with these headers; often I saw this implementation:
```python
charset = headers['Content-Type'].split(';')[-1].split('=')[-1].replace('"', '')
```
**No more of that!**

## 🔪 Features

`kiss-headers` is a basic library that allow you to handle headers as objects.

* A backwards-compatible syntax using bracket style.
* Capability to alter headers using simple, human-readable operator notation `+` and `-`.
* Flexibility if headers are from an email or HTTP, use as you need with one library.
* Ability to parse any object and extract recognized headers from it, it also supports UTF-8 encoded headers.
* Fully type-annotated.
* Provide great auto-completion in Python interpreter or any capable IDE.
* No dependencies. And never will be.
* 90% test coverage.

Plus all the features that you would expect from handling headers...

* Properties syntax for headers and attribute in header.
* Supports headers and attributes OneToOne, OneToMany and ManySquashedIntoOne.
* Capable of parsing `bytes`, `fp`, `str`, `dict`, `email.Message`, `requests.Response`, `httpx._models.Response` and `urllib3.HTTPResponse`.
* Automatically unquote and unfold the value of an attribute when retrieving it.
* Keep headers and attributes ordering.
* Case insensitive with header name and attribute key.
* Character `-` equal `_` in addition of above feature.
* Any syntax you like, we like.

### ✨ Installation

Whatever you like, use `pipenv` or `pip`, it simply works. Requires Python 3.6+ installed.
```sh 
pip install kiss-headers --upgrade
```

### 🍰 Usage

`parse_it()` method takes `bytes`, `str`, `fp`, `dict`, `email.Message` or even a `requests.Response` or `httpx._models.Response` itself and returns a `Headers` object.

```python
from requests import get
from kiss_headers import parse_it

response = get('https://www.google.fr')
headers = parse_it(response)

headers.content_type.charset  # output: ISO-8859-1
# Its the same as
headers["content-type"]["charset"]  # output: ISO-8859-1
```

Do not forget that headers are not OneToOne. One header can be repeated multiple times and attributes can have multiple values within the same header.

```python
from kiss_headers import parse_it

my_cookies = """set-cookie: 1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT; path=/; domain=.google.fr; Secure; SameSite=none
set-cookie: CONSENT=WP.284b10; expires=Fri, 01-Jan-2038 00:00:00 GMT; path=/; domain=.google.fr"""

headers = parse_it(my_cookies)

type(headers.set_cookie)  # output: list
headers.set_cookie[0].expires # output: Wed, 15-Apr-2020 21:27:31 GMT
headers.set_cookie[0]._1p_jar # output: 2020-03-16-21
headers.set_cookie[0]["1P_JAR"] # output: 2020-03-16-21
```

Since v2.1 you can transform an Header object to its target `CustomHeader` subclass to access more methods.

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

Just a note: Accessing a header that has the same name as a reserved keyword must be done this way :
```python
headers = parse_it('From: Ousret; origin=www.github.com\nIS: 1\nWhile: Not-True')

# this flavour
headers.from_ # to access From, just add a single underscore to it
# or.. just using :
headers['from']
```

## 🛠️ The builder

Introduced in the version 2.0, kiss-headers now allow you to create headers with more than 40+ ready-to-use, fully documented, header objects.

1st example usage
```python
from kiss_headers import Headers, Authorization
from requests import get

response = get("https://httpbin.org/bearer", headers=Headers(Authorization("Bearer", "qwerty")))
print(response.status_code)  # 200
```

2nd example usage
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
Also, you can create your own custom header object using the class `kiss_headers.CustomHeader`.

## 📜 Documentation

See the full documentation for advanced usages : [www.kiss-headers.tech](https://www.kiss-headers.tech/)

## 👤 Contributing

Contributions, issues and feature requests are very much welcome.<br />
Feel free to check [issues page](https://github.com/Ousret/kiss-headers/issues) if you want to contribute.

Firstly, after getting your own local copy, run `./scripts/install` to initialize your virtual environment.
Then run `./scripts/check` before you commit, make sure everything is still working.

Remember to keep it sweet and simple when contributing to this project.

## 📝 License

Copyright © 2020 [Ahmed TAHRI @Ousret](https://github.com/Ousret).<br />
This project is [MIT](https://github.com/Ousret/kiss-headers/blob/master/LICENSE) licensed.
