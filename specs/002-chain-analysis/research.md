# Phase 0: Research & Decisions

## Decision 1: Git Cloning Methodology

- **Decision**: Use Python's built-in `subprocess.run(["git", "clone", ...])` standard library over installing `GitPython`.
- **Rationale**: Adding `GitPython` introduces C-bindings and heavy tree dependencies that complicate cross-platform (Windows) pip environments and adds runtime surface area just for a shallow clone. `subprocess` is native, fast, and secure.
- **Alternatives considered**: `GitPython`, `pygit2`.

## Decision 2: OS Temporary Directory Management

- **Decision**: Use `tempfile.gettempdir()` mapped to UUID folders (e.g. `/tmp/atruss-code-atlas/<uuid>/repo`).
- **Rationale**: Isolates parallel runs and ensures OS garbage collection automatically removes old repositories when space is needed or reboots occur.
- **Alternatives considered**: AppData/roaming profiles, `./workspaces/`.

## Decision 3: Auth Credential Injections

- **Decision**: Use `https://x-access-token:{GITHUB_TOKEN}@github.com/...` dynamically injected into the clone URL *during subprocess call only*, keeping it out of the JSON manifest entirely.
- **Rationale**: Aligns with Constitution III (Security & Privacy First) preventing credential leakages inside saved JSON artifacts.
- **Alternatives considered**: SSH Keys (hard to manage universally on CI runners).
