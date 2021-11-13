def encode_access_key(value: str) -> str:
    return hash(value)
