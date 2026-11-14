# Headless Shell / Agent Execution Rules

When executing commands or diagnosing environment issues via `run_command` in this workspace, note the following constraints:

## 1. Node.js & npm (fnm)
The host system uses `fnm` (Fast Node Manager) to provide Node v22.
**Constraint**: `fnm` only initializes in *interactive* shells (via `.bashrc`). Antigravity's `run_command` runs a *non-interactive* shell, so `node` and `npm` will not be in the `$PATH` by default.
**Resolution**: 
- Option 1: Explicitly source profile bindings: `source ~/.bashrc && fnm use 22 && npm run dev`.
- Option 2: Rely on the USER to run `npm` commands interactively. Do not get stuck in a loop trying to "fix" npm installations.

## 2. Python Virtual Environment (.venv)
All Python code runs in the virtual environment located at the project root (`/.venv`).
**Constraint**: The `.venv` must be explicitly activated or the binary path fully qualified. 
**Resolution**: Always jump to the project root and `source .venv/bin/activate` before invoking python scripts, e.g.:
```bash
cd /path/to/project
source .venv/bin/activate
python3 scripts/generate-report-stubs.py
```

## 3. Creating Files with MDX/Astro Extensions
**Constraint**: Creating `.mdx` or `.md` files via the direct `write_to_file` tool can sometimes hang the IDE backend indefinitely due to Astro/Starlight Language Server file-lock loops taking precedence. 
**Resolution**: If `write_to_file` hangs or gets cancelled by the user when creating Astro/React/MDX files, use an internal python script to bypass the IDE Virtual File System API and write directly to the OS disk:
```bash
python3 -c "import pathlib; pathlib.Path('path/to/file.mdx').write_text('content')"
```
