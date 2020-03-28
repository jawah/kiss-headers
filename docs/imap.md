### Usage with email / IMAP

Usage of `kiss-headers` is pretty much the same. You can do the following :

```python
from kiss_headers import parse_it

raw_content = open('my-email.eml', 'rb').read()
headers = parse_it(raw_content)
```
