from pathlib import Path

import pytest
from pydantic import ValidationError

from solar_registry.service.testtool import get_testtool, _parse_testtool
from solar_registry.model.test_tool import OsType, ArchType, ParamWidget


def test_validate_correct_pytest_tool() -> None:
    workdir = str((Path(__file__).parent / "testdata").resolve())

    tool = get_testtool("pytest", workdir)

    assert tool.name == "pytest"
    assert tool.version == "0.1.6"
    assert tool.name_zh == "pytest自动化测试"
    assert tool.git_pkg_url == "github.com/OpenTestSolar/testtool-python@main:pytest"

    assert tool.support_os
    assert tool.support_os[0] == OsType.Windows
    assert tool.support_os[1] == OsType.Linux
    assert tool.support_os[2] == OsType.Darwin

    assert tool.support_arch
    assert tool.support_arch[0] == ArchType.Amd64
    assert tool.support_arch[1] == ArchType.Arm64


def test_validate_loose() -> None:
    _parse_testtool(Path(__file__).parent / "testdata" / "error_meta_files" / "error_yaml_with_loose.yaml", strict=False)


def test_validate_strict_with_errors() -> None:
    with pytest.raises(ValidationError) as ve:
        _parse_testtool(Path(__file__).parent / "testdata" / "error_meta_files" / "error_yaml_with_strict.yaml", strict=True)

    print(ve.value)

    assert r"String should match pattern '^[a-zA-Z-0-9_]+$'" in str(ve.value)
    assert r"Input should be 'COMPILED' or 'INTERPRETED'" in str(ve.value)
    assert r"Input should be 'python', 'golang', 'javascript', 'java' or 'cpp'" in str(ve.value)
    assert r"String should match pattern '^(\d+\.\d+\.\d+|stable)$'" in str(ve.value)
    assert r"Input should be 'linux', 'windows', 'darwin' or 'android'" in str(ve.value)
    assert r"Input should be 'amd64' or 'arm64'" in str(ve.value)


def test_validate_strict_with_no_os() -> None:
    with pytest.raises(ValidationError) as ve:
        _parse_testtool(Path(__file__).parent / "testdata" / "error_meta_files" / "error_yaml_with_strict_no_os.yaml", strict=True)

    print(ve.value)
    assert r"Value error, supportOS must be set" in str(ve.value)


def test_validate_strict_with_no_arch() -> None:
    with pytest.raises(ValidationError) as ve:
        _parse_testtool(Path(__file__).parent / "testdata" / "error_meta_files" / "error_yaml_with_strict_no_arch.yaml", strict=True)

    print(ve.value)
    assert r" Value error, need at least 1 support arch" in str(ve.value)


def test_parse_legacy_tool() -> None:
    tool = _parse_testtool(Path(__file__).parent / "testdata" / "legacy" / "testtool.yaml", strict=True)

    assert tool.name == "qt4s_pot-line"
    assert not tool.git_pkg_url
    assert tool.param_defs
    param1 = tool.param_defs[0]
    assert param1.name == "setup_cmdline"
    assert param1.value == "初始化命令"
    assert param1.desc == "加载/执行用例前的初始化命令"
    assert param1.default == "# place your extra init command here"
    assert param1.lang == "bash"
    assert param1.input_widget == ParamWidget.Code

    assert tool.legacy_spec
    assert tool.legacy_name == "qt4s"
    assert tool.legacy_spec.report_type == "junit"
    assert tool.legacy_spec.maintainers == ["aa", "bb"]
    assert tool.legacy_spec.testcase_runner.cli == "test"
    assert tool.legacy_spec.testcase_loader.cli == "test"
    assert tool.legacy_spec.testcase_analyzer.cli == "test"
    assert tool.legacy_spec.scaffolding_tool.cli == "test"
    assert tool.legacy_spec.node_setup.cli == "test"
    assert tool.legacy_spec.node_cleanup.cli == "test"
    assert tool.legacy_spec.global_setup.cli == "test"
    assert tool.legacy_spec.global_cleanup.cli == "test"
    assert tool.legacy_spec.res_pkg_url == "https://sample.com/pkg"
    assert tool.legacy_spec.doc_url == "https://sample.com/doc"
    assert tool.legacy_spec.logo_img_url == "https://sample.com/logo"
    assert not tool.legacy_spec.enable_code_coverage
