from typing import List, Type


def normalize_str(string: str) -> str:
    """
    Normalize a string by applying on it lowercase and replacing '-' to '_'.
    """
    return string.lower().replace("-", "_")


def flat_split(string: str, delimiter: str) -> List[str]:
    """
    Take a string and split it according to the passed delimiter.
    It will ignore delimiter if inside between double quote.
    The input string is considered perfect.
    """
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError(
            "Delimiter cannot be a double quote nor it can be longer than 1 char."
        )

    in_double_quote: bool = False
    result: List[str] = [""]

    for letter in string + "\x00":
        if letter == '"':
            in_double_quote = not in_double_quote
        if in_double_quote:
            continue
        if letter == delimiter or letter == "\x00":
            result[-1] = result[-1].lstrip().rstrip()
            result.append("")
            continue

        result[-1] += letter

    return result[:-1]


def class_to_header_name(type_: Type) -> str:
    """
    Take a type and infer its header name.
    """
    class_raw_name: str = str(type_).split("'")[-2].split(".")[-1]

    if class_raw_name.endswith('_'):
        class_raw_name = class_raw_name[:-1]

    if class_raw_name.startswith('_'):
        class_raw_name = class_raw_name[1:]

    header_name: str = str()

    for letter in class_raw_name:
        if letter.isupper() and header_name != "":
            header_name += "-" + letter
            continue
        header_name += letter

    return header_name


def header_name_to_class(name: str, root_type: Type) -> Type:
    """
    Do the opposite of class_to_header_name function. Will raise TypeError if no corresponding entry is found.
    """

    normalized_name = normalize_str(name).replace('_', '')

    for subclass in root_type.__subclasses__():
        if normalize_str(extract_class_name(subclass).split('.')[-1]) == normalized_name:
            return subclass

    raise TypeError("Cannot find a class matching header named '{name}'.".format(name=name))
