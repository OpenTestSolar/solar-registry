import os
from pathlib import Path

import yaml

from ..model.test_tool import TestTool


def get_testtool(tool_name: str, workdir: str | None) -> TestTool:
    workdir = workdir or os.getcwd()
    with open(Path(workdir) / tool_name / "testtool.yaml") as f:
        testtool = TestTool.model_validate(yaml.safe_load(f))
        return testtool
