from pathlib import Path

from repopg.__main__ import (
    get_file_structure,
    file_structure_to_string,
    get_files,
    FileStructure,
)

# The list of file extensions for testing
ext = [".py", ".txt"]


def test_get_file_structure(tmp_path: Path) -> None:
    """
    Test if the get_file_structure function can correctly gather all files with certain extensions in a directory.

    Args:
        tmp_path (Path): Temporary Path object provided by pytest

    Raises:
        AssertionError: If test fails
    """
    d = tmp_path / "directory"
    d.mkdir()
    f1 = d / "test.py"
    f1.write_text("content")
    f2 = d / "test.txt"
    f2.write_text("content")

    file_structure: FileStructure = get_file_structure(d, ext)

    assert f1.as_posix() in file_structure
    assert f2.as_posix() in file_structure


def test_file_structure_to_string(tmp_path: Path) -> None:
    """
    Test if the file_structure_to_string function can correctly convert a file structure to a string.

    Args:
        tmp_path (Path): Temporary Path object provided by pytest

    Raises:
        AssertionError: If test fails
    """
    d = tmp_path / "directory"
    d.mkdir()
    f1 = d / "test.py"
    f1.write_text("content")

    file_structure: FileStructure = {f1.as_posix(): None}

    structure_str: str = file_structure_to_string(file_structure)

    assert f1.name in structure_str


def test_get_files(tmp_path: Path) -> None:
    """
    Test if the get_files function can correctly extract all file paths from a file structure.

    Args:
        tmp_path (Path): Temporary Path object provided by pytest

    Raises:
        AssertionError: If test fails
    """
    d = tmp_path / "directory"
    d.mkdir()
    f1 = d / "test.py"
    f1.write_text("content")

    file_structure: FileStructure = {f1.as_posix(): None}

    files: list[str] = get_files(file_structure)

    assert f1.as_posix() in files
