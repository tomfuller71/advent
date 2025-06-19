# .gitignore Configuration for Advent of Code Repository

This .gitignore file is specifically designed for an Advent of Code repository containing Python solutions.

## What's Being Ignored

### Python-specific files:
- `__pycache__/` - Python bytecode cache directories
- `*.pyc`, `*.pyo`, `*.pyd` - Compiled Python files
- `build/`, `dist/`, `*.egg-info/` - Package build artifacts
- `.coverage`, `htmlcov/` - Test coverage reports
- `.pytest_cache/` - Pytest cache files

### Development environments:
- `.env*` - Environment variable files (may contain sensitive data)
- `.venv/`, `venv/`, `env/` - Virtual environment directories
- `.python-version` - pyenv Python version files

### IDE and Editor files:
- `.vscode/`, `.idea/` - IDE configuration
- `*.swp`, `*.swo` - Vim temporary files
- `.sublime-*` - Sublime Text settings

### Operating System files:
- `.DS_Store` - macOS file metadata
- `Thumbs.db` - Windows thumbnail cache
- `*~` - Linux backup files

### Temporary and backup files:
- `*.tmp`, `*.temp` - Temporary files
- `*.bak`, `*.backup` - Backup files
- `*.log` - Log files

## Files NOT ignored (tracked in repository):
- `input.txt` - Puzzle input files (commented option to ignore)
- `example.txt` - Example input files
- Solution source code (`.py` files)
- `README.md` files
- `requirements.txt` files

## Recently cleaned up:
- Removed `.DS_Store` files that were previously tracked
- Removed `.env` file that was previously tracked
- Python cache files are now properly ignored

## Usage:
The .gitignore is automatically applied. Files matching these patterns will not be tracked by git, keeping your repository clean and preventing sensitive or generated files from being committed.
