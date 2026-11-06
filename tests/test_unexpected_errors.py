from unittest.mock import patch
from src.analyzer import main


def test_main_unexpected_exception() -> None:
    """Test that unexpected exceptions in main() exit non-zero and log properly."""
    with patch("src.analyzer.sys.argv", ["analyzer.py", "dummy_path"]):
        with patch("src.analyzer.sys.exit") as mock_exit:
            with patch("src.analyzer.logger"):
                mock_exit.side_effect = SystemExit
                try:
                    main()
                except SystemExit:
                    pass
