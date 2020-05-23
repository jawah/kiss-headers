<h1 align="center">Welcome to Headers for Humans 👋 <a href="https://twitter.com/intent/tweet?text=Python%20library%20for%20oriented%20object%20HTTP%20or%20IMAP%20headers.&url=https://www.github.com/Ousret/kiss-headers&hashtags=python,headers"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"/></a></h1>

<p align="center">
  <sup>Object oriented headers, parser and builder. HTTP/1.1 Style.</sup><br>
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
    <img alt="Checked with mypy" src="https://camo.githubusercontent.com/34b3a249cd6502d0a521ab2f42c8830b7cfd03fa/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667"/>
  </a>
  <a href="https://pepy.tech/project/kiss-headers/">
     <img alt="Download Count Total" src="https://pepy.tech/badge/kiss-headers" />
  </a>
</p>

*kiss-headers* stand for, headers, keep it sweet and simple. [Principle KISS](https://fr.wikipedia.org/wiki/Principe_KISS).
It's a basic library, small and concise to help you get things done regarding headers in a better way.

## 🔪 Features

`kiss-headers` is a basic library that allows you to handle headers as objects.

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

!!! note
    Even if this library offers wide support to handle headers as they were objects you should know that headers are not obligated to follow any syntax.
    But we are pretty confident that this library cover at least 99 % of the use cases you could encounter. Feel free to address any issue you may encounter.

## ✨ Installation

Whatever you like, use `pipenv` or `pip`, it simply works. Requires Python 3.6+ installed.
```sh 
pip install kiss-headers
```

## 📝 License

Copyright © 2020 [Ahmed TAHRI @Ousret](https://github.com/Ousret).<br />
This project is [MIT](https://github.com/Ousret/kiss-headers/blob/master/LICENSE) licensed.
