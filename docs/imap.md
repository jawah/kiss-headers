### Usage with email, message (IMAP4)

Usage of `kiss-headers` is pretty much the same. You can do the following :

```python
from kiss_headers import parse_it

raw_content = open('my-email.eml', 'rb').read()
headers = parse_it(raw_content)
```

!!! hint
    As seen previously, the library tend to separate "squashed" content into multiple entries. This behaviour has been restricted for the "Subject" header as its human written.
