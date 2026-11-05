"""
analyzer.py
Alat analisis file sederhana: hash SHA-256, ukuran file, dan byte header.
Hanya menggunakan pustaka standar Python.

Penulis: Nuzuli
Versi: 0.4.0
Lisensi: MIT
"""

import sys
import os
import hashlib
import logging


class AnalysisError(Exception):
    """Khusus untuk error saat proses analisis file."""
    pass


def resolve_log_level():
    """Baca tingkat log dari variabel lingkungan LOG_LEVEL."""
    level_name = os.environ.get("LOG_LEVEL", "").upper()
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return levels.get(level_name, logging.WARNING)


logging.basicConfig(level=resolve_log_level(), format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def validate_path(path):
    """Validasi jalur file sebelum diproses."""
    if not path:
        raise AnalysisError("Path tidak boleh kosong")
    if "\x00" in path:
        raise AnalysisError("Path mengandung karakter yang tidak diperbolehkan")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    if not os.path.isfile(path):
        raise AnalysisError(f"Bukan file biasa: {path}")
    return path


def calculate_sha256(file_path):
    """Hitung hash SHA-256 dari sebuah file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def get_header_bytes(file_path, num_bytes=16):
    """Ambil byte pertama dari sebuah file."""
    with open(file_path, "rb") as f:
        header = f.read(num_bytes)
    return " ".join(f"{b:02x}" for b in header)


def analyze_file(file_path):
    """Lakukan analisis lengkap pada satu file."""
    validate_path(file_path)

    return {
        "name": os.path.basename(file_path),
        "size_bytes": os.path.getsize(file_path),
        "sha256": calculate_sha256(file_path),
        "header_hex": get_header_bytes(file_path)
    }


def format_report(result):
    """Format hasil analisis sebagai teks."""
    if result.get("size_bytes", 0) == 0:
        return "File kosong."

    return (
        f"=== LAPORAN ANALISIS FILE ===\n"
        f"Nama file : {result['name']}\n"
        f"Ukuran    : {result['size_bytes']} byte\n"
        f"SHA-256   : {result['sha256']}\n"
        f"Header    : {result['header_hex']}\n"
    )


def format_json(result):
    """Format hasil analisis sebagai JSON sederhana."""
    import json
    return json.dumps(result, indent=2)


def main():
    """Fungsi utama untuk menjalankan dari baris perintah."""
    args = sys.argv[1:]

    if not args or "-h" in args or "--help" in args:
        print("Penggunaan: python analyzer.py <path_file> [--json]")
        print("Opsi:")
        print("  --json    Tampilkan hasil dalam format JSON")
        sys.exit(0)

    use_json = "--json" in args
    file_paths = [a for a in args if a != "--json"]

    for path in file_paths:
        try:
            result = analyze_file(path)
            if use_json:
                print(format_json(result))
            else:
                print(format_report(result))

        except AnalysisError as e:
            logger.error(f"Analysis error: {e}")
            sys.exit(2)

        except OSError as e:
            logger.error(f"File system error: cannot access '{e.filename}': {e.strerror}")
            sys.exit(2)

        except KeyboardInterrupt:
            logger.info("Operation cancelled by user")
            sys.exit(1)


if __name__ == "__main__":
    main()
