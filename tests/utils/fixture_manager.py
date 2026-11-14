import os
import shutil
import tempfile
import subprocess
from contextlib import contextmanager
from typing import Iterator

class FixtureManager:
    """Orchestrates test harness isolation targeting mapped public SHAs."""
    
    @staticmethod
    @contextmanager
    def clone_pinned_fixture(repo_url: str, pinned_sha: str) -> Iterator[str]:
        """Clones a repository to a temp directory and checkouts a specific pinned SHA."""
        temp_dir = tempfile.mkdtemp(prefix="atruss_fixture_")
        target_dir = os.path.join(temp_dir, "repo")
        
        try:
            # Clone with no checkout, then explicitly checkout the SHA
            subprocess.run(
                ["git", "clone", "--no-checkout", repo_url, target_dir], 
                check=True, 
                capture_output=True,
                text=True
            )
            subprocess.run(
                ["git", "checkout", pinned_sha], 
                cwd=target_dir, 
                check=True, 
                capture_output=True,
                text=True
            )
            yield target_dir
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
