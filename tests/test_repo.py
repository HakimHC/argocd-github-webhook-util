from src.repo import Repo
import pytest
import random


@pytest.mark.parametrize(
    "repo,expected",
    [
        ("git@github.com:HakimHC/homelab.git", "HakimHC/homelab"),
        ("git@github.com:HakimHC/fract-ol.git", "HakimHC/fract-ol"),
        ("https://github.com/HakimHC/homelab.git", "HakimHC/homelab"),
        ("https://git.example.com/owner/repo.git", "owner/repo"),
        ("git@git.example.com:owner/repo.git", "owner/repo"),
        ("git@github.com:HakimHC/fail", None),
    ]
)
def test_repo_name(repo, expected):
    repository = Repo(repo)
    assert expected == repository.full_name
