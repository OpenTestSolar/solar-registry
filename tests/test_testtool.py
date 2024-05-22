from pathlib import Path

import pytest
from pydantic import ValidationError

from solar_registry.service.testtool import get_testtool
from solar_registry.model.test_tool import OsType, ArchType


def test_validate_correct_pytest_tool() -> None:
    workdir = str((Path(__file__).parent / "testdata").resolve())

    tool = get_testtool("pytest", workdir)

    assert tool.name == "pytest"
    assert tool.version == "0.1.6"
    assert tool.git_pkg_url == "github.com/OpenTestSolar/testtool-python@main:pytest"

    assert tool.support_os[0] == OsType.Windows
    assert tool.support_os[1] == OsType.Linux
    assert tool.support_os[2] == OsType.Darwin

    assert tool.support_arch[0] == ArchType.Amd64
    assert tool.support_arch[1] == ArchType.Arm64


def test_validate_name_error() -> None:
    workdir = str((Path(__file__).parent / "testdata" / "error_meta_file").resolve())

    with pytest.raises(ValidationError) as ve:
        get_testtool("pytest", workdir)

    assert r"String should match pattern '^[a-z]+$'" in str(ve.value)


def test_validate_version_error() -> None:
    workdir = str((Path(__file__).parent / "testdata" / "error_version_file").resolve())

    with pytest.raises(ValidationError) as ve:
        get_testtool("pytest", workdir)

    assert r"String should match pattern '^(\d+\.\d+\.\d+|stable)$'" in str(ve.value)


def test_validate_os_type_error() -> None:
    workdir = str((Path(__file__).parent / "testdata" / "error_os_and_arch").resolve())

    with pytest.raises(ValidationError) as ve:
        get_testtool("pytest", workdir)

    print(ve)

    assert r"Input should be 'linux', 'windows', 'darwin' or 'android'" in str(ve.value)


def test_validate_arch_type_error() -> None:
    workdir = str((Path(__file__).parent / "testdata" / "error_os_and_arch").resolve())

    with pytest.raises(ValidationError) as ve:
        get_testtool("pytest1", workdir)

    print(ve)

    assert r"Input should be 'amd64' or 'arm64'" in str(ve.value)
