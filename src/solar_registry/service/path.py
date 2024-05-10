from pathlib import Path

from ..model.test_tool import TestTool


def generate_metafile_path(testtool: TestTool) -> Path:
    metafile = (
        Path("/tmp/testsolar/generate")
        / testtool.lang
        / testtool.name
        / "metadata.json"
    )
    metafile.parent.mkdir(exist_ok=True, parents=True)
    return metafile


def generate_merged_metafile_path(testtool: TestTool) -> Path:
    metafile = (
        Path("/tmp/testsolar/merged") / testtool.lang / testtool.name / "metadata.json"
    )
    metafile.parent.mkdir(exist_ok=True, parents=True)
    return metafile


def generate_stable_index_path(testtool: TestTool) -> Path:
    metafile = (
        Path("/tmp/testsolar/generate")
        / testtool.lang
        / testtool.name
        / "stable.index.json"
    )
    metafile.parent.mkdir(exist_ok=True, parents=True)
    return metafile
