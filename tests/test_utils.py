import pytest
from pathlib import Path
import shutil
from src.utils import get_files_in_directory
import random
import os


def generate_files_in_directory(directory: Path, files: list[str]) -> None:
    for file in files:
        (directory / file).touch()


@pytest.mark.parametrize(
    "files",
    [
        ["a", "b", "c"],
        ["file1", "file2", ".hidden", ".gitignore"],
        []
    ]
)
def test_get_files_in_directory(files: list[str]):
    directory = Path("/tmp/%032x" % random.getrandbits(128))
    os.makedirs(directory)
    generate_files_in_directory(directory, files)
    try:
        assert sorted(get_files_in_directory(directory)) == sorted(files)
    except AssertionError:
        raise
    finally:
        shutil.rmtree(directory)

