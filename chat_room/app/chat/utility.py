from typing import List


def encode_access_key(value: List[str]) -> str:
    return "|".join(value)


def decode_access_key(value: str) -> List[str]:
    return value.split("|")
