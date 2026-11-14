import asyncio
import base64
import logging
import time
from typing import Any

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
      - Optional httpx.AsyncBaseTransport injection for offline testing
    """

    def __init__(
        self,
        token: str | None = None,
        max_concurrent: int = 10,
        rate_limit_threshold: int = RATE_LIMIT_THRESHOLD,
        logger: logging.Logger | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._token = token
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._threshold = rate_limit_threshold
        self._log = logger or logging.getLogger("gh_discovery")
        self._transport = transport
        self._client: httpx.AsyncClient | None = None
        self.last_tree_truncated: bool = False

    async def __aenter__(self) -> "GitHubClient":
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GH_API_VERSION,
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        client_kwargs: dict[str, Any] = {
            "base_url": GH_API_BASE,
            "headers": headers,
            "timeout": 30.0,
        }
        if self._transport is not None:
            client_kwargs["transport"] = self._transport

        self._client = httpx.AsyncClient(**client_kwargs)
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
                    self._log.warning(
                        f"Secondary rate limit - sleeping {retry_after}s (attempt {attempt + 1})"
                    )
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
        limit_str = response.headers.get("x-ratelimit-limit")
        threshold = self._threshold
        if limit_str is not None and limit_str.isdigit():
            limit = int(limit_str)
            # Scale threshold for low-quota endpoints (e.g., Search API 10/min unauthenticated)
            threshold = 1 if limit <= 10 else min(self._threshold, max(1, limit // 5))
        if remaining < threshold and reset_str:
            wait = max(0, int(reset_str) - int(time.time())) + 1
            self._log.warning(
                f"Rate limit low ({remaining} remaining) - sleeping {wait}s until reset"
            )
            await asyncio.sleep(wait)

    @staticmethod
    def _next_page_url(response: httpx.Response) -> str | None:
        link = response.headers.get("link", "")
        for part in link.split(","):
            if 'rel="next"' in part:
                return part.split(";")[0].strip().strip("<>")
        return None

    async def get_paginated(
        self, path: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        url: str | None = path
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

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        resp = await self._request("GET", path, params=params)
        return resp.json()

    async def get_repo_tree_with_status(
        self, owner: str, repo: str, ref: str = "main"
    ) -> tuple[list[str], str, bool]:
        """Fetch recursive repo paths, resolved tree SHA, and GitHub truncated status."""
        try:
            data = await self.get(
                f"/repos/{owner}/{repo}/git/trees/{ref}",
                params={"recursive": "1"},
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (404, 409):
                if exc.response.status_code == 404 and ref == "main":
                    return await self.get_repo_tree_with_status(owner, repo, ref="master")
                self.last_tree_truncated = False
                return [], "unknown", False
            raise

        truncated = bool(data.get("truncated", False))
        self.last_tree_truncated = truncated
        tree_sha = data.get("sha", "unknown")
        paths = [
            item["path"]
            for item in data.get("tree", [])
            if item.get("type") == "blob" and item.get("path")
        ]
        if truncated:
            self._log.warning(
                f"Git tree truncated by GitHub API for {owner}/{repo}@{ref}; "
                f"continuing with {len(paths)} partial paths and metadata fallback."
            )
        return paths, tree_sha, truncated

    async def get_repo_tree(
        self, owner: str, repo: str, ref: str = "main"
    ) -> tuple[list[str], str]:
        """Fetch recursive repository file paths and resolved tree SHA."""
        paths, tree_sha, _ = await self.get_repo_tree_with_status(owner, repo, ref=ref)
        return paths, tree_sha

    async def get_file_text(
        self, owner: str, repo: str, path: str, ref: str | None = None
    ) -> str | None:
        """Fetch and decode UTF-8 file contents via GitHub Contents API."""
        params = {"ref": ref} if ref else None
        try:
            data = await self.get(f"/repos/{owner}/{repo}/contents/{path}", params=params)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

        if isinstance(data, dict) and data.get("encoding") == "base64" and data.get("content"):
            raw = base64.b64decode(data["content"])
            return raw.decode("utf-8", errors="replace")
        if isinstance(data, dict) and isinstance(data.get("content"), str):
            return data["content"]
        return None
