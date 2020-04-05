from typing import List


def normalize_str(string: str) -> str:
    """
    Normalize a string by applying on it lowercase and replacing '-' to '_'.
    """
    return string.lower().replace("-", "_")


def flat_split(delimiter: str) -> List[str]:
    """
    Take a string and split it according to the passed delimiter.
    It will ignore delimiter if inside between double quote.
    """
    return
