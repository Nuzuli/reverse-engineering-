# DataFactor — Reverse Engineering 🛡️



![Python Tests](https://github.com/Nuzuli/reverse-engineering-/actions/workflows/python-tests.yml/badge.svg)



A learning project focused on basic file inspection, reverse engineering methodology, and reproducible analysis documentation.

## Features

- Calculate a file's SHA-256 hash.
- Report file size and filename.
- Display the first 16 bytes of a file as hexadecimal.
- Provide a reusable analysis report template.
- Automated unit tests with GitHub Actions (CI).

## Project Structure

```
.
├── .github/workflows/python-tests.yml
├── docs/
│   └── TEMPLATE_ANALYSIS.md
├── src/
│   └── analyzer.py
├── tests/
│   └── test_analyze_file.py
├── requirements.txt
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Requirements

- Python 3.8 or newer
- `pytest` and `pytest-cov` (for running tests)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Use the analyzer from Python, run from the repository root:

```python
from src.analyzer import analyze_file

result = analyze_file("path/to/sample.bin")
print(result)
```

## Run Tests

From the repository root:

```bash
python -m pytest tests/ -v
```

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