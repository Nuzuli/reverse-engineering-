# Changelog

All notable changes to this project are documented in this file.
The format follows Keep a Changelog.

## [0.1.0] - 2026-10-24

### Added
- `analyze_file()` returns file name, size, SHA-256 hash, and first 16 bytes in hex.
- Command-line interface: `python src/analyzer.py <file>`.
- `AnalysisError` for missing, non-regular, or unreadable files.
- Unit tests with coverage gate (80 percent) running in GitHub Actions.
- Pinned test dependencies in `requirements.txt`.
- `CONTRIBUTING.md` and analysis report template in `docs/`.