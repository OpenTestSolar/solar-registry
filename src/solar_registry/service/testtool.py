import os
from pathlib import Path

import yaml
from loguru import logger

from ..model.test_tool import TestTool


def get_testtool(tool_name: str, workdir: str | None) -> TestTool:
    logger.debug(f"querying testtool for {tool_name}")
    workdir = workdir or os.getcwd()
    with open(Path(workdir) / tool_name / "testtool.yaml") as f:
        testtool = TestTool.model_validate(yaml.safe_load(f))
        logger.debug(f"loaded testtool: {testtool.model_dump_json(indent=2)}")
        return testtool
