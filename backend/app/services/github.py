from __future__ import annotations

from typing import Any

import httpx


async def fetch_github_profile(username: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        data = response.json()

    return {
        "username": data.get("login"),
        "name": data.get("name"),
        "public_repos": data.get("public_repos", 0),
        "followers": data.get("followers", 0),
        "following": data.get("following", 0),
        "profile_created_at": data.get("created_at"),
    }
