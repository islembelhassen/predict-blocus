import hashlib


def create_external_id(
    source_name: str,
    text: str,
    published_at: str,
) -> str:
    payload = (
        f"{source_name}"
        f"{text}"
        f"{published_at}"
    )

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()