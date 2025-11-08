import asyncio
from sqlalchemy import select

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import async_session_factory
from app.models.user import User


async def init_superuser() -> None:
    try:
        # Validate password length before processing
        password = settings.FIRST_SUPERUSER_PASSWORD
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            print(
                f"WARNING: Password for {settings.FIRST_SUPERUSER_EMAIL} is "
                f"{len(password_bytes)} bytes. It will be truncated to 72 bytes."
            )

        async with async_session_factory() as session:
            result = await session.execute(
                select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
            )
            user = result.scalar_one_or_none()
            if user:
                print(f"Superuser {settings.FIRST_SUPERUSER_EMAIL} already exists")
                return

            superuser = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=get_password_hash(password),
                full_name="Administrator",
                is_superuser=True,
            )
            session.add(superuser)
            await session.commit()
            print(f"Created superuser: {settings.FIRST_SUPERUSER_EMAIL}")
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            print(
                f"ERROR: Password is too long. Please set FIRST_SUPERUSER_PASSWORD "
                f"to a password shorter than 72 bytes in your .env file."
            )
        raise
    except Exception as e:
        print(f"Error initializing superuser: {e}")
        raise


def main() -> None:
    """Entry point for script execution."""
    asyncio.run(init_superuser())


if __name__ == "__main__":
    main()
