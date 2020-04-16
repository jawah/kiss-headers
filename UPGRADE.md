Migrate from v1 to v2
------------------------

The API remain stable, the biggest change is :

  - Header that contain multiple entries (usually separated with a coma) are now exploded into multiple header object.

Before :
```python
headers = parse_it(
        """Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br""")

print(
    headers.accept.content
) # Would output : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
```
Now :

```python
headers = parse_it(
        """Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br""")

for accept in headers.accept:
    print(accept.content, "has qualifier", accept.has("q"))

# Would output :
# text/html has qualifier False
# application/xhtml+xml has qualifier False
# application/xml;q=0.9 has qualifier True
# */*;q=0.8 has qualifier True
```

Sometime a single header can contain multiple entries, usually separated by a coma. Now kiss-headers always separate them to create 
multiple object.
