import os
from pathlib import Path
from loguru import logger

from ..model.test_tool import StableIndexMetaData, MetaDataHistory


class ToolValidator:
    def __init__(self, workdir: str | None) -> None:
        if workdir:
            self.workdir = Path(workdir)
        else:
            self.workdir = Path.cwd()

    def validate(self) -> None:
        """
        检查json文件是否符合要求
        """

        self.validate_stable_index()
        self.validate_tool_meta_json()

    def validate_stable_index(self) -> None:
        stable_index_file = Path(self.workdir) / "testtools" / "stable.index.json"
        logger.info(f"Validating stable index file [{stable_index_file}]")

        with open(stable_index_file) as f:
            sim = StableIndexMetaData.model_validate_json(f.read())
            logger.info(f"✅ Validated stable index file [{stable_index_file}] OK.")
            logger.info(f"✅ It has {len(sim.tools)} tools.")

    def validate_tool_meta_json(self) -> None:
        for dir_path, _, filenames in os.walk(self.workdir / "testtools"):
            for filename in filenames:
                if filename != "stable.index.json":
                    metafile = Path(dir_path) / filename
                    logger.info(f"Validating tool meta file [{metafile}]")
                    with open(metafile) as f:
                        re = MetaDataHistory.model_validate_json(f.read())
                        if re.versions:
                            logger.info(
                                f"✅ Validated tool [{re.versions[0].meta.name}] OK."
                            )
