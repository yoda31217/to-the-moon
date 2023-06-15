import datetime
from git.repo import Repo


def get_version() -> str:
    repository = get_repository()
    return (
        f"hash: 0x{get_head_commit_hash(repository)[0:8]}..."
        + f" from {get_head_commit_datetime(repository)}"
    )


def get_head_commit_datetime(repository: Repo) -> datetime.datetime:
    return repository.head.commit.committed_datetime


def get_head_commit_hash(repository: Repo) -> str:
    return repository.head.commit.hexsha


def get_repository() -> Repo:
    return Repo(search_parent_directories=True)
