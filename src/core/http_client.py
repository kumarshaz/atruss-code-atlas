import asyncio
import logging
import time
from typing import Any, Optional
import httpx

GH_API_BASE = "https://api.github.com"
GH_API_VERSION = "2022-11-28"
RATE_LIMIT_THRESHOLD = 50

class GitHubClient:
    """
    Async HTTP client for GitHub REST API.
    Handles:
      - Bearer token auth
      - Link-header pagination
      - Proactive rate-limit inspection
      - Secondary rate-limit (403/429) backoff
    """

    def __init__(
        self,
        token: Optional[str] = None,
        max_concurrent: int = 10,
        rate_limit_threshold: int = RATE_LIMIT_THRESHOLD,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._token = token
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._threshold = rate_limit_threshold
        self._log = logger or logging.getLogger("gh_discovery")
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "GitHubClient":
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GH_API_VERSION,
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
            
        self._client = httpx.AsyncClient(
            base_url=GH_API_BASE,
            headers=headers,
            timeout=30.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._client:
            await self._client.aclose()

    async def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        assert self._client is not None
        for attempt in range(5):
            async with self._semaphore:
                resp = await self._client.request(method, url, **kwargs)

            await self._check_rate_limit(resp)

            if resp.status_code == 429:
                wait = int(resp.headers.get("retry-after", 60))
                self._log.warning(f"429 - sleeping {wait}s (attempt {attempt + 1})")
                await asyncio.sleep(wait)
                continue

            if resp.status_code == 403:
                body = resp.text
                if "rate limit" in body.lower() or "secondary" in body.lower():
                    retry_after = int(resp.headers.get("retry-after", 60))
                    self._log.warning(f"Secondary rate limit - sleeping {retry_after}s (attempt {attempt + 1})")
                    await asyncio.sleep(retry_after)
                    continue
                resp.raise_for_status()

            resp.raise_for_status()
            return resp

        raise RuntimeError(f"Exhausted retries for {url}")

    async def _check_rate_limit(self, response: httpx.Response) -> None:
        remaining_str = response.headers.get("x-ratelimit-remaining")
        reset_str = response.headers.get("x-ratelimit-reset")
        if remaining_str is None:
            return
        remaining = int(remaining_str)
        if remaining < self._threshold and reset_str:
            wait = max(0, int(reset_str) - int(time.time())) + 1
            self._log.warning(f"Rate limit low ({remaining} remaining) - sleeping {wait}s until reset")
            await asyncio.sleep(wait)

    @staticmethod
    def _next_page_url(response: httpx.Response) -> Optional[str]:
        link = response.headers.get("link", "")
        for part in link.split(","):
            if 'rel="next"' in part:
                return part.split(";")[0].strip().strip("<>")
        return None

    async def get_paginated(self, path: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        url: Optional[str] = path
        while url:
            resp = await self._request("GET", url, params=params)
            data = resp.json()
            if isinstance(data, list):
                results.extend(data)
            elif isinstance(data, dict) and "items" in data:
                results.extend(data["items"])
            else:
                results.append(data)
            url = self._next_page_url(resp)
            params = None
        return results

    async def get(self, path: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        resp = await self._request("GET", path, params=params)
        return resp.json()
