import shutil
from pathlib import Path

import pytest

from solar_registry.commands.generator import Generator


@pytest.fixture
def clean_generated_files():
    try:
        yield
    finally:
        shutil.rmtree("/tmp/testsolar/generate/")


def test_generate_meta_file(clean_generated_files):
    workdir = str(Path(__file__).parent.joinpath("testdata").resolve())
    gen = Generator(tool_name="pytest", workdir=workdir)
    gen.generate_meta_file()

    path = gen.generate_metafile_path()

    assert Path(path).exists()

    with open(path) as f:
        print(f.read())
