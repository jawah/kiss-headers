<h1 align="center">Welcome to Headers for Human 👋 <a href="https://twitter.com/intent/tweet?text=So%20simple,%20you%20may%20fall%20in%20love%20at%20first%20sight%20!%20With%20auto-completion%20!&url=https://www.github.com/Ousret/kiss-headers&hashtags=python,headers"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"/></a></h1>

<p align="center">
  <img alt="Temporary logo" src="https://user-images.githubusercontent.com/9326700/76708477-64a96600-66f7-11ea-9d4a-8cc07866e185.png"/><br>
  <sup>So simple ! With auto-completion !</sup><br>
  <a href="https://travis-ci.org/Ousret/kiss-headers">
    <img src="https://travis-ci.org/Ousret/kiss-headers.svg?branch=master"/>
  </a>
  <img src="https://img.shields.io/pypi/pyversions/kiss-headers.svg?orange=blue" />
  <a href="https://github.com/ousret/kiss-headers/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-purple.svg" target="_blank" />
  </a>
  <a href="https://www.codacy.com/manual/Ousret/kiss-headers?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Ousret/kiss-headers&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/0994a03546094b519601e33554c48535"/>
  </a>
  <a href="https://codecov.io/gh/Ousret/kiss-headers">
      <img src="https://codecov.io/gh/Ousret/kiss-headers/branch/master/graph/badge.svg" />
  </a>
  <a href='https://kiss-headers.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/kiss-headers/badge/?version=latest' alt='Documentation Status' />
  </a>
</p>

### Why ?

No matters your religion, IMAP4 or HTTP, you should not worries about accessing easily header and associated attributes, adjectives or values.

<p align="center">
<img src="https://user-images.githubusercontent.com/9326700/76709832-32513600-6702-11ea-81cd-b68a7e85abb2.gif" alt="using kiss-headers from python interpreter"/>
</p>

I have seen so much chunk of code trying to deal with them, often I saw this :
```python
charset = headers['Content-Type'].split(';')[-1].split('=')[-1]
```
**No more of that !**

### Your support

Please ⭐ this repository if this project helped you!

### ✨ Installation

Whatever you like, use `Pipenv` or `pip`, it simply work. We are expecting you to have python 3.6+ installed.
```sh 
pip install kiss-headers
```

### 🍰 Usage

`parse_it()` method take `bytes`, `str`, `fp`, `dict` or even `requests.Response` itself and give you back a `Headers` object.

```python
from requests import get
from kiss_headers import parse_it

response = get('https://www.google.fr')
headers = parse_it(response)

'Content-Type' in headers  # output: True
'Content_type' in headers  # output: True

str(headers.content_type)  # output : text/html; charset=ISO-8859-1
'application/json' in headers.content_type  # output: False
'text/html' in headers.content_type # output: True

str(headers.content_type.charset)  # output : ISO-8859-1
type(headers.set_cookie) # output: list
'Secure' in headers.set_cookie[0] # output: True
'domain' in headers.set_cookie[0] # output: True
headers.set_cookie[0].domain # output: .google.fr
```

Do not forget that headers are not 1 TO 1. One header can be repeated multiple time and attribute can have multiple value within the same header.

```python
from kiss_headers import parse_it

my_cookies = """set-cookie: 1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT; path=/; domain=.google.fr; Secure; SameSite=none
set-cookie: CONSENT=WP.284b10; expires=Fri, 01-Jan-2038 00:00:00 GMT; path=/; domain=.google.fr"""

headers = parse_it(my_cookies)

type(headers.set_cookie)  # output: list
headers.set_cookie[0].expires # output Wed, 15-Apr-2020 21:27:31 GMT
```

## 👤 Contributing

Contributions, issues and feature requests are very much welcome.<br />
Feel free to check [issues page](https://github.com/Ousret/kiss-headers/issues) if you want to contribute.

## 📝 License

Copyright © 2020 [Ahmed TAHRI @Ousret](https://github.com/Ousret).<br />
This project is [MIT](https://github.com/Ousret/kiss-headers/blob/master/LICENSE) licensed.
