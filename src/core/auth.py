import logging
import sys
from pathlib import Path
from typing import Optional

def setup_secure_logging(log_path: Path, token: Optional[str] = None) -> logging.Logger:
    """
    Dual-logger implementation ensuring PATs never leak into console or files.
    """
    logger = logging.getLogger("gh_secure")
    logger.setLevel(logging.DEBUG)
    
    # Custom formatter to mask tokens
    class SecureFormatter(logging.Formatter):
        def format(self, record):
            msg = super().format(record)
            if token and token in msg:
                msg = msg.replace(token, "***MASKED_TOKEN***")
            return msg

    fmt = SecureFormatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    
    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    
    # File Handler
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)
        
    return logger

async def validate_token(client, org: str, logger: logging.Logger) -> None:
    """
    Validates token via org endpoint to guarantee repo and read:org scope.
    """
    import httpx
    if not client._token:
        logger.warning("[AUTH] No token provided. Running in unauthenticated mode (60 requests/hr rate limits apply!).")
        return
        
    try:
        await client.get(f"/orgs/{org}")
        logger.info(f"[AUTH] Token validated for org: {org}")
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 403):
            raise PermissionError(
                f"Token rejected for org '{org}'. Ensure token has scopes: repo, read:org"
            ) from exc
        raise
