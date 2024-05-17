from pathlib import Path

import pytest
from pydantic import ValidationError

from solar_registry.service.testtool import get_testtool


def test_validate_correct_pytest_tool():
    workdir = str((Path(__file__).parent / "testdata").resolve())

    tool = get_testtool("pytest", workdir)

    assert tool.name == "pytest"
    assert tool.version == "0.1.6"


def test_validate_name_error():
    workdir = str((Path(__file__).parent / "testdata" / "error_meta_file").resolve())

    with pytest.raises(ValidationError) as ve:
        get_testtool("pytest", workdir)

    assert r"String should match pattern '^[a-z]+$'" in str(ve.value)


def test_validate_version_error():
    workdir = str((Path(__file__).parent / "testdata" / "error_version_file").resolve())

    with pytest.raises(ValidationError) as ve:
        get_testtool("pytest", workdir)

    assert r"String should match pattern '^(\d+\.\d+\.\d+|stable)$'" in str(ve.value)
