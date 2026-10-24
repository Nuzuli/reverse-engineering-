# DataFactor — Reverse Engineering 🛡️



![Python Tests](https://github.com/Nuzuli/reverse-engineering-/actions/workflows/python-tests.yml/badge.svg)



A learning project focused on basic file inspection, reverse engineering methodology, and reproducible analysis documentation.

## Features

- Calculate a file's SHA-256 hash.
- Report file size and filename.
- Display the first 16 bytes of a file as hexadecimal.
- Provide a reusable analysis report template.
- Automated unit tests with coverage gate in GitHub Actions.

## Project Structure

- `src/analyzer.py`: file analyzer and command-line entry point
- `tests/test_analyze_file.py`: unit tests
- `docs/TEMPLATE_ANALYSIS.md`: analysis report template
- `.github/workflows/python-tests.yml`: CI workflow
- `requirements.txt`: pinned test dependencies
- `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`

## Requirements

- Python 3.8 or newer
- `pytest` and `pytest-cov` (test only; the analyzer itself has no dependencies)

Install test dependencies with `pip install -r requirements.txt`.

## Usage

Command line, from the repository root:

`python src/analyzer.py path/to/sample.bin`

The report shows the file name, size in bytes, SHA-256 hash, and first 16 bytes in hexadecimal. An empty file is reported as `(empty file)`.

As a Python module:

`from src.analyzer import analyze_file`

`analyze_file("path/to/sample.bin")` returns a dictionary with the keys `name`, `size_bytes`, `sha256`, and `header_hex`.

## Error Handling

`analyze_file` raises `AnalysisError` when the path does not exist, is not a regular file (for example a directory), or cannot be read.

Command-line exit codes:

- `0`: analysis succeeded
- `2`: analysis failed, with the error message printed to stderr

## Run Tests

From the repository root:

`python -m pytest tests/ -v --cov=src --cov-fail-under=80`

Tests also run automatically on every push through GitHub Actions.

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