from pathlib import Path

import git

from automate_git import create_local_git_repo, is_git_repo


def test_is_git_repo(tmpdir):
    tmpdir = Path(tmpdir)
    assert not is_git_repo(tmpdir)

    repo = tmpdir / "repo1"
    repo.mkdir()
    git.Repo.init(repo)
    assert is_git_repo(repo)


def test_create_local_git_repo(tmpdir):
    tmpdir = Path(tmpdir)

    # Create repo that doesn't exist
    repo = tmpdir / "repo2"
    create_local_git_repo(repo)
    assert repo.exists()
    assert Path(git.Repo(repo).git_dir).stem == ".git"
