from pathlib import Path


def directories(path: Path) -> None:
    if path.is_dir():
        return
    else:
        path.mkdir()
        return
