import pytest
from click.testing import CliRunner

import within_reach
from within_reach.cli import main


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_the_package_has_a_version() -> None:
    """Any release version: Cut Release rewrites ``__version__`` on the release branch, and this test runs there too."""
    import re

    assert re.fullmatch(r"\d+\.\d+\.\d+", within_reach.__version__)


def test_help_lists_the_commands(runner: CliRunner) -> None:
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0 and "hot-reload" in result.output and "grab" in result.output


@pytest.mark.parametrize("command", ["hot-reload", "grab"])
def test_unwritten_commands_say_so_and_exit_2(runner: CliRunner, command: str) -> None:
    result = runner.invoke(main, [command])

    assert result.exit_code == 2 and "not implemented yet" in result.output
