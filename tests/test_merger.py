import tempfile
from pathlib import Path

from solar_registry.commands.meta_merger import MetaMerger
from solar_registry.service.testtool import get_testtool


def test_merge_meta_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        workdir = str(Path(__file__).parent.joinpath("testdata").resolve())
        testtool = get_testtool(tool_name="pytest", workdir=workdir)
        gen = MetaMerger(testtool)
        gen.merge_index_and_history(Path(tmpdir))

        index_file = Path(tmpdir) / "testtools/stable.index.json"
        meta_file = Path(tmpdir) / "testtools/python/pytest/metadata.json"

        assert index_file.exists()
        assert meta_file.exists()
