# Contributing

Thanks for your interest in improving this project!

## Getting Started

1. Fork the repository and clone it.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the tests from the repository root with `python -m pytest tests/ -v --cov=src --cov-fail-under=80`.

## Guidelines

- Keep each change small and focused: one feature or fix per commit.
- Add or update tests together with every code change.
- Make sure all tests pass before opening a pull request.
- Only analyze files you are authorized to examine.

## Reporting Issues

Open an issue describing the problem, the expected behavior, and steps to reproduce it.

## Review process

Pull requests are reviewed by the maintainer. A change is merged when CI is green (ruff, mypy, and pytest with coverage), it includes tests for the behavior it adds or fixes, and each commit describes one logical change. Larger changes should start as an issue so the approach can be discussed first.