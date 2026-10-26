# DataFactor — Reverse Engineering 🛡️



![Python Tests](https://github.com/Nuzuli/reverse-engineering-/actions/workflows/python-tests.yml/badge.svg)



A learning project focused on basic file inspection, reverse engineering methodology, and reproducible analysis documentation.

## Features

- Calculate a file's SHA-256 hash.
- Report file size and filename.
- Display the first 16 bytes of a file as hexadecimal.
- Provide a reusable analysis report template.
- Automated tests, linting, type checking, and a dependency audit in GitHub Actions.

## Project Structure

- `src/analyzer.py`: file analysis and the command-line entry point
- `src/report.py`: plain-text report formatting
- `tests/`: unit tests
- `docs/TEMPLATE_ANALYSIS.md`: analysis report template
- `.github/workflows/`: CI and the manual lockfile workflow
- `requirements.txt` and `requirements-lock.txt`: test tools and their pinned lockfile
- `Dockerfile`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`

## Quick Start (fresh clone)

Python 3.8 or newer is required. The analyzer itself has no dependencies; the tools below are only for testing.

```
git clone https://github.com/Nuzuli/reverse-engineering-.git
cd reverse-engineering-
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

On Windows, activate the environment with `.venv\Scripts\activate`.

For an exact, reproducible toolchain, install from the lockfile instead: `pip install -r requirements-lock.txt`. After changing `requirements.txt`, regenerate it by running the manual "Update lockfile" workflow in the Actions tab.

## Usage

Run from the repository root:

`python -m src.analyzer path/to/sample.bin`

Example output:

```
=== File Analysis Report ===
File name : sample.bin
Size      : 5 bytes
SHA-256   : 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
Header    : 68 65 6c 6c 6f
```

An empty file is reported as `(empty file)`.

As a Python module:

`from src.analyzer import analyze_file`

`analyze_file("path/to/sample.bin")` returns a dictionary with the keys `name`, `size_bytes`, `sha256`, and `header_hex`. Use `src.report.format_report` to render it as text.

## Docker

Run the analyzer in an isolated container:

```
docker build -t reverse-engineering .
docker run --rm -v "$(pwd)/sample.bin:/data/sample.bin:ro" reverse-engineering /data/sample.bin
```

## Error Handling

`analyze_file` raises `AnalysisError` when the path does not exist, is not a regular file (for example a directory), or cannot be read.

Command-line exit codes:

- `0`: analysis succeeded
- `2`: analysis failed, with the error message printed to stderr

## Logging

The analyzer uses the standard `logging` module under the logger name `src.analyzer`. Enable it in your own code, for example with `logging.basicConfig(level=logging.INFO)`.

## Development

Run the checks locally:

```
ruff check src tests
mypy src
python -m pytest tests/ -v --cov=src --cov-fail-under=80
```

The same checks run on every push through GitHub Actions.

## Analysis Workflow

1. Record sample information using `docs/TEMPLATE_ANALYSIS.md`.
2. Inspect basic file properties using the analyzer.
3. Perform further static or dynamic analysis only in an appropriate, isolated environment.
4. Document observations, evidence, limitations, and conclusions.

## Safety and Legal Notice

Analyze only files you are authorized to examine. Do not execute untrusted samples on your primary device. Use an isolated environment for dynamic analysis and follow applicable laws and policies.

## Project Status

This project currently provides basic file metadata inspection and a starting point for structured reverse engineering documentation. It does not yet perform binary disassembly or decompilation.

## License

MIT License. See `LICENSE`.