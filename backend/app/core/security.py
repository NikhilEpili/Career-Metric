from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _safe_truncate_password(password: str) -> str:
    """
    Aggressively truncate password to ensure it's ALWAYS <= 72 bytes,
    even after multiple encode/decode cycles.
    
    This function uses a conservative approach: truncate to 70 bytes
    to leave a 2-byte safety margin for encoding edge cases.
    """
    if not password:
        return password
    
    # Convert to bytes
    try:
        password_bytes = password.encode("utf-8")
    except (UnicodeEncodeError, AttributeError):
        password_bytes = password.encode("utf-8", errors="replace")
    
    # Truncate to 70 bytes (safety margin)
    if len(password_bytes) > 70:
        password_bytes = password_bytes[:70]
    
    # Decode and verify it's still <= 70 bytes when re-encoded
    truncated = password_bytes.decode("utf-8", errors="replace")
    
    # Iteratively truncate until re-encoding is <= 70 bytes
    max_iterations = 10
    iteration = 0
    while iteration < max_iterations:
        re_encoded = truncated.encode("utf-8")
        if len(re_encoded) <= 70:
            break
        # Truncate one more byte
        password_bytes = password_bytes[:max(0, len(password_bytes) - 1)]
        if not password_bytes:
            return ""
        truncated = password_bytes.decode("utf-8", errors="replace")
        iteration += 1
    
    return truncated




def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"exp": expire, "sub": subject}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Note: Password is truncated to 70 bytes before verification to comply with bcrypt limits.
    """
    if not plain_password:
        return False
    
    # Use safe truncation (70 bytes with safety margin)
    truncated = _safe_truncate_password(plain_password)
    
    try:
        return pwd_context.verify(truncated, hashed_password)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # Last resort: force truncate to 70 bytes
            final_password = plain_password.encode("utf-8")[:70].decode("utf-8", errors="replace")
            return pwd_context.verify(final_password, hashed_password)
        raise


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Note: bcrypt has a 72-byte limit. Passwords longer than 70 bytes will be truncated
    (70 bytes provides a safety margin for encoding edge cases).
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Use safe truncation (70 bytes with safety margin)
    truncated = _safe_truncate_password(password)
    
    # Final verification: ensure it's <= 70 bytes
    final_bytes = truncated.encode("utf-8")
    if len(final_bytes) > 70:
        truncated = final_bytes[:70].decode("utf-8", errors="replace")
    
    try:
        return pwd_context.hash(truncated)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # Last resort: force truncate to 70 bytes
            final_password = password.encode("utf-8")[:70].decode("utf-8", errors="replace")
            return pwd_context.hash(final_password)
        raise
