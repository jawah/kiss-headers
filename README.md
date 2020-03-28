<h1 align="center">Welcome to Headers for Human 👋 <a href="https://twitter.com/intent/tweet?text=So%20simple,%20you%20may%20fall%20in%20love%20at%20first%20sight%20!%20With%20auto-completion%20!&url=https://www.github.com/Ousret/kiss-headers&hashtags=python,headers"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"/></a></h1>

<p align="center">
  <img alt="Temporary logo" src="https://user-images.githubusercontent.com/9326700/76708477-64a96600-66f7-11ea-9d4a-8cc07866e185.png"/><br>
  <sup>Imagine you could combine advantages of many representations, with auto-completion!</sup><br>
  <a href="https://travis-ci.org/Ousret/kiss-headers">
    <img src="https://travis-ci.org/Ousret/kiss-headers.svg?branch=master"/>
  </a>
  <img src="https://img.shields.io/pypi/pyversions/kiss-headers.svg?orange=blue" />
  <a href="https://pepy.tech/project/kiss-headers/">
    <img alt="Download Count /Month" src="https://pepy.tech/badge/kiss-headers/month"/>
  </a>
  <a href="https://github.com/ousret/kiss-headers/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-purple.svg" />
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
  <img alt="Download Count Total" src="https://pepy.tech/badge/kiss-headers" />
</p>

### ❓ Why

No matter if you are currently building software using HTTP or IMAP, you should not worry about easily accessing header and associated attributes, adjectives or values.

<p align="center">
<img src="https://user-images.githubusercontent.com/9326700/77257881-55866300-6c77-11ea-820c-7550e6bdeee7.gif" alt="using kiss-headers from python interpreter"/>
</p>

I have seen so many chunks of code trying to deal with these headers; often I saw this implementation :
```python
charset = headers['Content-Type'].split(';')[-1].split('=')[-1].replace('"', '')
```
**No more of that !** 🤮

## 🔪 Features

`kiss-headers` is a library on steroids that allow you to handle headers with great care. 

* A backwards-compatible syntax using bracket style.
* Capability to alter headers using simple, human-readable operator notation `+` and `-`.
* Flexibility if headers are from IMAP4 or HTTP, use as you need with one library.
* Ability to parse any object and extract recognized headers from it.
* Fully type-annotated.
* Provide great auto-completion in Python interpreter or any capable IDE.
* 90% test coverage.

Plus all the features that you would expect from handling headers...

* Properties syntax for headers and attribute in header.
* Supports headers and attributes OneToOne and OneToMany.
* Capable of parsing `bytes`, `fp`, `str`, `dict`, `requests.Response` and `httpx._models.Response`.
* Automatically unquote value of an attribute when retrieving it.
* Case insensitive with header name and attribute key.
* Character `-` equal `_` in addition of above feature.
* Any syntax you like, we like.

## Your support

Please 🌟 this repository if this project helped you! ✨ That would be very much appreciated. ✨

### ✨ Installation

Whatever you like, use `pipenv` or `pip`, it simply works. Requires Python 3.6+ installed.
```sh 
pip install kiss-headers
```

### 🍰 Usage

`parse_it()` method takes `bytes`, `str`, `fp`, `dict` or even `requests.Response` or `httpx._models.Response` itself and returns a `Headers` object.

```python
from requests import get
from kiss_headers import parse_it

response = get('https://www.google.fr')
headers = parse_it(response)

headers.content_type.charset  # output: ISO-8859-1
```

Do not forget that headers are not OneToOne. One header can be repeated multiple times and attributes can have multiple values within the same header.

```python
from kiss_headers import parse_it

my_cookies = """set-cookie: 1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT; path=/; domain=.google.fr; Secure; SameSite=none
set-cookie: CONSENT=WP.284b10; expires=Fri, 01-Jan-2038 00:00:00 GMT; path=/; domain=.google.fr"""

headers = parse_it(my_cookies)

type(headers.set_cookie)  # output: list
headers.set_cookie[0].expires # output Wed, 15-Apr-2020 21:27:31 GMT
```

If this behaviour does bother you, you can lock output to always be a list. Just call `lock_output_type()` method.

Just a note: Accessing a header that has the same name as a reserved keyword must be done this way :
```python
headers = parse_it('From: Ousret; origin=www.github.com\nIS: 1\nWhile: Not-True')

# this flavour
headers.from_ # to access From, just add a single underscore to it
# or..
headers['from']
```

## 📜 Documentation

See the full documentation for advanced usages : [www.kiss-headers.tech](https://www.kiss-headers.tech/)

## 👤 Contributing

Contributions, issues and feature requests are very much welcome.<br />
Feel free to check [issues page](https://github.com/Ousret/kiss-headers/issues) if you want to contribute.

## 📝 License

Copyright © 2020 [Ahmed TAHRI @Ousret](https://github.com/Ousret).<br />
This project is [MIT](https://github.com/Ousret/kiss-headers/blob/master/LICENSE) licensed.
