<h1 align="center">Welcome to Headers for Human 👋 <a href="https://twitter.com/intent/tweet?text=So%20simple,%20you%20may%20fall%20in%20love%20at%20first%20sight%20!%20With%20auto-completion%20!&url=https://www.github.com/Ousret/kiss-headers&hashtags=python,headers"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"/></a></h1>

<p align="center">
  <img alt="Temporary logo" src="https://user-images.githubusercontent.com/9326700/76708477-64a96600-66f7-11ea-9d4a-8cc07866e185.png"/><br>
  <sup>So simple, you may fall in love at first sight ! With auto-completion !</sup><br>
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

## Your support

Please ⭐ this repository if this project helped you!

### ✨ Installation

Whatever you like, use `Pipenv` or `pip`, it simply work. We are expecting you to have python 3.6+ installed.
```sh 
pip install kiss-headers
```

### 🍰 Usage

`parse_it()` method take `bytes`, `str`, `fp` or `dict` and give you back a `Headers` object.

```python
from requests import get
from kiss_headers import parse_it

response = get('https://httpbin.org/get')
headers = parse_it(response.headers)

'Content-Type' in headers  # output: True
'Content_type' in headers  # output: True

str(headers.content_type)  # output : application/json
'application/json' in headers.content_type  # output: True

str(headers.content_type.charset)  # output : utf-8
```

## 👤 Contributing

Contributions, issues and feature requests are very much welcome.<br />
Feel free to check [issues page](https://github.com/Ousret/kiss-headers/issues) if you want to contribute.

## 📝 License

Copyright © 2020 [Ahmed TAHRI @Ousret](https://github.com/Ousret).<br />
This project is [MIT](https://github.com/Ousret/kiss-headers/blob/master/LICENSE) licensed.
