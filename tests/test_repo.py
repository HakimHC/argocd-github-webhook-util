from __future__ import annotations

import pytest

from src.repo import Repo


@pytest.mark.parametrize(
    "repo,expected",
    [
        ("git@github.com:HakimHC/homelab.git", "HakimHC/homelab"),
        ("git@github.com:HakimHC/fract-ol.git", "HakimHC/fract-ol"),
        ("https://github.com/HakimHC/homelab.git", "HakimHC/homelab"),
        ("https://git.example.com/owner/repo.git", "owner/repo"),
        ("http://git.example.com/owner/repo.git", "owner/repo"),
        ("git@git.example.com:owner/repo.git", "owner/repo"),
        ("git@github.com:HakimHC/fail", None),
        ("https://bit.bucket.com///.git", None),
    ],
)
def test_repo_name(repo, expected):
    repository = Repo(repo)
    assert expected == repository.full_name
