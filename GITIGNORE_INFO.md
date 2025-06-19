# .gitignore Configuration for Advent of Code Repository

This repository now uses a **two-tier gitignore system**:

1. **Global gitignore** (`~/.gitignore_global`) - handles universal patterns
2. **Local gitignore** (`.gitignore`) - handles project-specific patterns

## Global Patterns (handled by ~/.gitignore_global)

These are automatically ignored in **ALL** repositories on your system:

- **OS files**: `.DS_Store`, `Thumbs.db`, `*~`
- **Editor files**: `.vscode/`, `.idea/`, `*.swp`
- **Environment files**: `.env*`, credentials, secrets
- **Cache files**: `__pycache__/`, `*.pyc`, `.pytest_cache/`
- **Temporary files**: `*.tmp`, `*.log`, `*.bak`

## Local Project-Specific Patterns

This repository's `.gitignore` only handles Advent of Code specific patterns:

### Python build artifacts:

- `build/`, `dist/`, `*.egg-info/` - Package distribution files
- `.tox/`, `.nox/` - Testing environment directories
- `htmlcov/` - Coverage report directories

### Optional AoC files:

- `session.txt`, `personal_input.txt` - Personal session data
- Commented options for `input.txt` and `solution.txt`

### Project tools:

- `.ipynb_checkpoints` - Jupyter notebook checkpoints
- `Pipfile.lock` - Pipenv lock files
- Tool-specific configurations

## What's NOT ignored (tracked in repository):

- Solution source code (`.py` files)
- `example.txt` - Example input files
- `input.txt` - Puzzle input files (by default)
- `README.md` files
- `requirements.txt` files
- Test files

## Benefits of This Setup:

- ✅ **Cleaner repositories**: No OS or editor files ever get committed
- ✅ **Less maintenance**: Universal patterns handled globally
- ✅ **Project focus**: Local .gitignore only has relevant patterns
- ✅ **Consistent**: Same global rules across all projects
- ✅ **Secure**: Environment files protected everywhere
