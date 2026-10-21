Reverse Engineering Workflow

1. Authorization and Safety

- Confirm that the sample is authorized for analysis.
- Use an isolated environment for untrusted files.
- Never execute unknown samples on a primary device.

2. Record File Information

- Record the filename and file size.
- Calculate the SHA-256 hash.
- Record the source and purpose of the analysis.

3. Initial Inspection

Run the basic analyzer:

python scripts/analyze_file.py path/to/sample.bin

Review the reported file metadata and hexadecimal header.

4. Further Analysis

If authorized and necessary, use appropriate static analysis tools to inspect file formats, strings, and program structure. Perform dynamic analysis only in a properly isolated environment.

5. Document Findings

Use "TEMPLATE_ANALYSIS.md" to record:

- Methods and tools used
- Observations and supporting evidence
- Conclusions and confidence levels
- Limitations and reproducibility steps

6. Testing

Run automated tests from the repository root:

python -m unittest discover -s tests -v

7. Reporting

Summarize findings clearly. Separate observed facts from assumptions and include enough detail for another analyst to reproduce the work.