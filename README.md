DataFactor — Reverse Engineering 🛡️

A learning project focused on basic file inspection, reverse engineering methodology, and reproducible analysis documentation.

Features

- Calculate a file's SHA-256 hash.
- Report file size and filename.
- Display the first 16 bytes of a file as hexadecimal.
- Provide a reusable analysis report template.
- Include automated unit tests for basic file inspection.

Project Structure

.
├── README.md
├── docs/
│   └── TEMPLATE_ANALYSIS.md
├── scripts/
│   ├── __init__.py
│   └── analyze_file.py
└── tests/
    └── test_analyze_file.py

Requirements

- Python 3.8 or newer
- No third-party Python packages required

Usage

Run the analyzer with a file path:

python scripts/analyze_file.py path/to/sample.bin

The script reports the filename, size in bytes, SHA-256 hash, and first 16 bytes in hexadecimal.

Run Tests

From the repository root, run:

python -m unittest discover -s tests -v

Analysis Workflow

1. Record sample information using "docs/TEMPLATE_ANALYSIS.md".
2. Inspect basic file properties using the analysis script.
3. Perform further static or dynamic analysis only in an appropriate, isolated environment.
4. Document observations, evidence, limitations, and conclusions.

Safety and Legal Notice

Analyze only files you are authorized to examine. Do not execute untrusted samples on your primary device. Use an isolated environment for dynamic analysis and follow applicable laws and policies.

Project Status

This project currently provides basic file metadata inspection and a starting point for structured reverse engineering documentation. It does not yet perform binary disassembly or decompilation.