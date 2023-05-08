from git import Repo


def get_version():
    repo = Repo(search_parent_directories=True)
    return (
        f"hash: 0x{repo.head.commit.hexsha[0:8]}..."
        + f" from {repo.head.commit.committed_datetime}"
    )
