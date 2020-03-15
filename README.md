<h1 align="center">Welcome to Headers for Human 👋 <a href="https://twitter.com/intent/tweet?text=The%20Real%20First%20Universal%20Charset%20%26%20Language%20Detector&url=https://www.github.com/Ousret/charset_normalizer&hashtags=python,encoding,chardet,developers"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"/></a></h1>

<p align="center">

  <img alt="Temporary logo" src="https://user-images.githubusercontent.com/9326700/76708477-64a96600-66f7-11ea-9d4a-8cc07866e185.png"/>
  
  <sup>So simple, you may fall in love at first sight ! With auto-completion !</sup><br>
  
  <a href="https://travis-ci.org/Ousret/kiss-headers">
    <img src="https://travis-ci.org/Ousret/kiss-headers.svg?branch=master"/>
  </a>
  <img src="https://img.shields.io/pypi/pyversions/kiss-headers.svg?orange=blue" />
  <a href="https://github.com/ousret/kiss-headers/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-purple.svg" target="_blank" />
  </a>
  <a href="https://app.codacy.com/project/Ousret/kiss-headers/dashboard">
    <img alt="Code Quality Badge" src="https://api.codacy.com/project/badge/Grade/a0c85b7f56dd4f628dc022763f82762c"/>
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

### Installation

Whatever you like, use `Pipenv` or `pip`, it simply work. We are expecting you to have python 3.6+ installed.
```sh 
pip install kiss-headers
```

### Usage

`parse_it()` method take `bytes`, `str`, `fp` or `dict` and give you back a `Headers` object.

```python
from requests import get
from kiss_headers import parse_it

response = get('https://httpbin.org/get')
headers = parse_it(response.headers)

'Content-Type' in headers  # output: True
'Content_type' in headers  # output: True

headers.content_type  # output : application/json
'application/json' in headers.content_type  # output: True

headers.content_type.charset  # output : utf-8
```

## 👤 Contributing

Contributions, issues and feature requests are very much welcome.<br />
Feel free to check [issues page](https://github.com/Ousret/kiss-headers/issues) if you want to contribute.

## 📝 License

Copyright © 2020 [Ahmed TAHRI @Ousret](https://github.com/Ousret).<br />
This project is [MIT](https://github.com/Ousret/kiss-headers/blob/master/LICENSE) licensed.
