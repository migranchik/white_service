import re

_EMAIL_RE = re.compile(
    r"^(?=.{1,254}$)(?=.{1,64}@)"
    r"[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$"
)


def validate_email(email: str) -> bool:
    if not email:
        return False

    email = email.strip().lower()

    if not _EMAIL_RE.match(email):
        return False

    # защита от abc..def@gmail.com
    local_part = email.split("@", 1)[0]
    if ".." in local_part:
        return False

    return True