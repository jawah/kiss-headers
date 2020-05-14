### The theory

Headers are *kind* of complicated, so many RFCs to study, so many forms to comprehend. This package offers the possibility to 
handle most of the forms you could encounter.

So, after my researches on Mozilla MDN and IETF websites, I have elaborated a new way to handle them.

#### Roots concepts

What you should know before, before getting started :

Content-Type: *text/html*; **charset**=UTF-8

Here `text/html` is a member of `Content-Type`, also `charset` is an attribute and its associated with the value `UTF-8`.

!!! note "TL;DR"
    Provided models, `Headers` and `Header` does not inherit from `Mapping` nor does it from `List`. Some package prefers to inherit from them, we do not. 
