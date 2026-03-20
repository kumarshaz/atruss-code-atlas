import os
import shutil
import tempfile
import subprocess
import uuid
import logging
from typing import Iterator
from contextlib import contextmanager

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
    @contextmanager
    def clone_temporarily(clone_url: str, token: str | None = None) -> Iterator[str | None]:
        """
        Clones a repository into a temporary directory and yields the path.
        The repository is NOT explicitly deleted by default, allowing OS temp garbage collection,
        but we can optionally wipe it if required later. For now, it stays.
        """
        temp_base = tempfile.gettempdir()
        run_id = str(uuid.uuid4())
        repo_dir = os.path.join(temp_base, "atruss_code_atlas", run_id)
        
        os.makedirs(repo_dir, exist_ok=True)
        secure_url = GitCloner._inject_credentials(clone_url, token)
        
        try:
            logger.info(f"Cloning {clone_url} into {repo_dir}...")
            # Use subprocess to run the git clone command
            result = subprocess.run(
                ["git", "clone", "--depth", "1", secure_url, "."],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True
            )
            yield repo_dir
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone repository: {e.stderr}")
            yield None
        # No explicit cleanup inside finally block based on spec decisions.
