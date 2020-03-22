from collections import MutableMapping, OrderedDict, Mapping
from typing import Any, NoReturn, Iterator, Tuple, Optional

"""
Disclaimer : CaseInsensitiveDict has been borrowed from `psf/requests`.
Minors changes has been made.
"""


class CaseInsensitiveDict(MutableMapping):
    """A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive::

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.
    """

    def __init__(self, data: Optional[Mapping] = None, **kwargs):
        self._store: OrderedDict = OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key: str, value: Any) -> NoReturn:
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower().replace("-", "_")] = (key, value)

    def __getitem__(self, key: str) -> Any:
        return self._store[key.lower().replace("-", "_")][1]

    def __delitem__(self, key: str) -> NoReturn:
        del self._store[key.lower().replace("-", "_")]

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self) -> int:
        return len(self._store)

    def lower_items(self) -> Iterator[Tuple[str, Any]]:
        """Like iteritems(), but with all lowercase keys."""
        return ((lowerkey, keyval[1]) for (lowerkey, keyval) in self._store.items())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self) -> "CaseInsensitiveDict":
        return CaseInsensitiveDict(dict(self._store.values()))

    def __repr__(self) -> str:
        return str(dict(self.items()))
