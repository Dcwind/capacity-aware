import secrets
import string

def new_request_id(prefix: str = "req") -> str:
    alphabet = string.ascii_lowercase + string.digits
    suffix = ''.join(secrets.choice(alphabet) for _ in range(8))
    return f"{prefix}_{suffix}"
