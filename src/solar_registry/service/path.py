from pathlib import Path

from .testtool import get_testtool
from ..model.test_tool import TestTool


def generate_metafile_path(
    tool_name: str, workdir: str | None = None, testtool: TestTool | None = None
) -> Path:
    if not testtool:
        testtool = get_testtool(tool_name=tool_name, workdir=workdir)

    metafile = (
        Path("/tmp/testsolar/generate")
        / testtool.lang
        / testtool.name
        / "metadata.json"
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
