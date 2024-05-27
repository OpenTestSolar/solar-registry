import os
from pathlib import Path

import yaml
from loguru import logger

from ..model.test_tool import TestTool


def get_testtool(tool_name: str, workdir: str | None) -> TestTool:
    logger.debug(f"querying testtool for {tool_name}")
    workdir = workdir or os.getcwd()
    return _parse_testtool(Path(workdir) / tool_name / "testtool.yaml", strict=True)


def _parse_testtool(yaml_file: Path, strict: bool) -> TestTool:
    with open(yaml_file) as f:
        context = {}
        if strict:
            context["strict"] = True

        testtool = TestTool.model_validate(yaml.safe_load(f), context=context)
        logger.debug(
            f"loaded testtool: {testtool.model_dump_json(by_alias=True, indent=2, exclude_none=True)}"
        )
        return testtool


def github_asset_gen(testtool: TestTool) -> str:
    return f"https://github.com/OpenTestSolar/testtool-{testtool.lang}-{testtool.name}/archive/refs/tags/{testtool.version}.tar.gz"
