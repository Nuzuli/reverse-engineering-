from pathlib import Path

import pytest

from src import analyzer


def test_main_prints_report(tmp_path, capsys):
    sample = tmp_path / "a.bin"
    sample.write_bytes(b"\x00\x01\x02")
    assert analyzer.main([str(sample)]) == 0
    out = capsys.readouterr().out
    assert "a.bin" in out and "00 01 02" in out


def test_main_empty_file_message(tmp_path, capsys):
    sample = tmp_path / "empty.bin"
    sample.write_bytes(b"")
    analyzer.main([str(sample)])
    assert "(empty file)" in capsys.readouterr().out


def test_main_missing_file_exits_2(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        analyzer.main([str(tmp_path / "tidak-ada.bin")])
    assert exc.value.code == 2
    assert "File not found" in capsys.readouterr().err


def test_read_error_becomes_analysis_error(tmp_path, monkeypatch):
    sample = tmp_path / "a.bin"
    sample.write_bytes(b"x")

    def boom(*args, **kwargs):
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "open", boom)
    with pytest.raises(analyzer.AnalysisError):
        analyzer.analyze_file(sample)


def test_unexpected_exception_propagates(monkeypatch):
    def boom(_path):
        raise RuntimeError("bug")

    monkeypatch.setattr(analyzer, "analyze_file", boom)
    with pytest.raises(RuntimeError):
        analyzer.main(["apa-saja.bin"])