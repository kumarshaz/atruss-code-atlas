import asyncio
import logging
import os
import shutil
import subprocess
import tempfile
import uuid
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager

logger = logging.getLogger(__name__)


class GitCloner:
    """Orchestrates secure local cloning of remote git repositories into OS-temp bounds."""

    @staticmethod
    def _inject_credentials(clone_url: str, token: str | None) -> str:
        """Injects GitHub token into the HTTPS URL securely without persisting logs."""
        if not token:
            return clone_url
        if clone_url.startswith("https://") and "@" not in clone_url:
            return clone_url.replace("https://", f"https://x-access-token:{token}@", 1)
        return clone_url

    @staticmethod
    def _build_clone_cmd(clone_url: str, token: str | None, branch: str | None) -> list[str]:
        secure_url = GitCloner._inject_credentials(clone_url, token)
        cmd = [
            "git",
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            "--single-branch",
        ]
        if branch and branch != "HEAD":
            cmd.extend(["--branch", branch])
        cmd.extend([secure_url, "."])
        return cmd

    @staticmethod
    @contextmanager
    def clone_temporarily(
        clone_url: str,
        token: str | None = None,
        branch: str | None = None,
        sha: str | None = None,
        timeout: float | None = 180.0,
    ) -> Iterator[str | None]:
        """
        Shallow-clone a repository (`--depth 1 --filter=blob:none --single-branch`)
        into an isolated temporary directory and guarantee immediate disk cleanup on exit.
        """
        temp_base = tempfile.gettempdir()
        run_id = str(uuid.uuid4())
        repo_dir = os.path.join(temp_base, "atruss_code_atlas", run_id)

        os.makedirs(repo_dir, exist_ok=True)
        git_env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        cmd = GitCloner._build_clone_cmd(clone_url, token, branch)

        try:
            logger.info("Cloning %s into %s...", clone_url, repo_dir)
            subprocess.run(
                cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True,
                timeout=timeout,
                env=git_env,
            )
            if sha and sha not in ("unknown", "HEAD"):
                head_res = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=repo_dir,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=15.0,
                    env=git_env,
                )
                current_sha = (head_res.stdout or "").strip() if head_res else ""
                if current_sha and current_sha != sha:
                    subprocess.run(
                        ["git", "fetch", "--depth", "1", "--filter=blob:none", "origin", sha],
                        cwd=repo_dir,
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=timeout,
                        env=git_env,
                    )
                    subprocess.run(
                        ["git", "checkout", "--detach", sha],
                        cwd=repo_dir,
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=15.0,
                        env=git_env,
                    )
            yield repo_dir
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            err_detail = getattr(exc, "stderr", "") or str(exc)
            logger.error("Failed to clone repository %s: %s", clone_url, err_detail)
            yield None
        finally:
            shutil.rmtree(repo_dir, ignore_errors=True)

    @staticmethod
    @asynccontextmanager
    async def clone_async(
        clone_url: str,
        token: str | None = None,
        branch: str | None = None,
        sha: str | None = None,
        timeout: float = 180.0,
    ) -> AsyncIterator[str]:
        """
        Async shallow blobless clone that terminates its git subprocess immediately
        upon timeout/cancellation and removes the temp directory before returning.
        """
        temp_base = tempfile.gettempdir()
        run_id = str(uuid.uuid4())
        repo_dir = os.path.join(temp_base, "atruss_code_atlas", run_id)
        os.makedirs(repo_dir, exist_ok=True)
        git_env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        cmd = GitCloner._build_clone_cmd(clone_url, token, branch)

        proc: asyncio.subprocess.Process | None = None
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=repo_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=git_env,
            )
            _, stderr_bytes = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            if proc.returncode != 0:
                err_msg = stderr_bytes.decode("utf-8", errors="replace").strip()
                raise RuntimeError(f"git clone failed ({proc.returncode}): {err_msg}")

            if sha and sha not in ("unknown", "HEAD"):
                head_proc = await asyncio.create_subprocess_exec(
                    "git",
                    "rev-parse",
                    "HEAD",
                    cwd=repo_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=git_env,
                )
                head_out, _ = await asyncio.wait_for(head_proc.communicate(), timeout=15.0)
                current_sha = head_out.decode("utf-8", errors="replace").strip()
                if current_sha and current_sha != sha:
                    fetch_proc = await asyncio.create_subprocess_exec(
                        "git",
                        "fetch",
                        "--depth",
                        "1",
                        "--filter=blob:none",
                        "origin",
                        sha,
                        cwd=repo_dir,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        env=git_env,
                    )
                    await asyncio.wait_for(fetch_proc.communicate(), timeout=timeout)
                    co_proc = await asyncio.create_subprocess_exec(
                        "git",
                        "checkout",
                        "--detach",
                        sha,
                        cwd=repo_dir,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        env=git_env,
                    )
                    await asyncio.wait_for(co_proc.communicate(), timeout=15.0)

            yield repo_dir
        except BaseException:
            if proc is not None and proc.returncode is None:
                proc.kill()
                await proc.wait()
            raise
        finally:
            shutil.rmtree(repo_dir, ignore_errors=True)
