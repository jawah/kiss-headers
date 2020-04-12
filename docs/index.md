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
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-purple.svg" target="_blank" />
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
  <img alt="Download Count Total" src="https://pepy.tech/badge/kiss-headers" />
</p>

## 🔪 Features

`kiss-headers` is a library on steroids that allow you to handle headers with great care. 

* A backwards-compatible syntax using bracket style.
* Capability to alter headers using simple, human-readable operator notation `+` and `-`.
* Flexibility if headers are from IMAP4 or HTTP, use as you need with one library.
* Ability to parse any object and extract recognized headers from it.
* Fully type-annotated.
* Provide great auto-completion in Python interpreter or any capable IDE.
* Absolutely no dependencies.
* 90% test coverage.

Plus all the features that you would expect from handling headers...

* Properties syntax for headers and attribute in header.
* Supports headers and attributes OneToOne, OneToMany and ManySquashedIntoOne.
* Capable of parsing `bytes`, `fp`, `str`, `dict`, `email.Message`, `requests.Response` and `httpx._models.Response`.
* Automatically unquote value of an attribute when retrieving it.
* Case insensitive with header name and attribute key.
* Character `-` equal `_` in addition of above feature.
* Any syntax you like, we like.

!!! note
    Even if this library offer a wide support to handle headers as they were objects you should know that headers are not obligated to follow any syntax.
    But we are pretty confident that this library cover at least 99 % of the use cases you could encounter. Feel free to address any issue you may encounter.

## ✨ Installation

Whatever you like, use `pipenv` or `pip`, it simply works. Requires Python 3.6+ installed.
```sh 
pip install kiss-headers
```

## 📝 License

Copyright © 2020 [Ahmed TAHRI @Ousret](https://github.com/Ousret).<br />
This project is [MIT](https://github.com/Ousret/kiss-headers/blob/master/LICENSE) licensed.
