import shutil
from pathlib import Path

import pytest

from solar_registry.commands.meta_merger import MetaMerger


@pytest.fixture
def clean_generated_files():
    try:
        yield
    finally:
        shutil.rmtree("/tmp/testsolar/generate/")


def test_merge_meta_file(clean_generated_files):
    workdir = str(Path(__file__).parent.joinpath("testdata").resolve())
    gen = MetaMerger(tool_name="pytest", workdir=workdir)
    gen.merge_index_and_history(Path("/tmp/testsolar/generate/"))

    index_file = Path("/tmp/testsolar/generate/testtools/stable.index.json")
    meta_file = Path("/tmp/testsolar/generate/testtools/python/pytest/metadata.json")

    assert index_file.exists()
    assert meta_file.exists()
