# The theory

Headers are *kind* of complicated, so many RFCs to study, so many forms to comprehend. This package offers the possibility to 
handle most of the forms you could encounter.

So, after my researches on Mozilla MDN and IETF websites, I have elaborated a new way to handle them.

## Roots concepts

### Bases

What you should know before getting started :

Content-Type: *text/html*; **charset**=UTF-8

Here `text/html` is a member of `Content-Type`, also `charset` is an attribute and its associated with the value `UTF-8`.

!!! note "TL;DR"
    Provided models, `Headers` and `Header` does not inherit from `Mapping` nor does it from `List`. Some package prefers to inherit from them, we do not. 

In most headers, the semi-colon `;` character is used as a separator. But you can also see some headers using a single comma `,` as a separator.

Here's how I understand those two separators.

- The single comma indicate that their is multiple entries for the same headers.
- The semi-colon separate members inside the same entry and therefor cannot be interpreted separately.

Writing `Accept: text/html, application/json;q=0.8` is another way to write :

```
Accept: text/html
Accept: application/json;q=0.8
```

### Cases

In this project case insensitive mean no distinction between lower and upper letters plus the character `-` eq `_`.

- The header name is case insensitive.
- Every member of an header is case insensitive except the value associated with an attribute.
