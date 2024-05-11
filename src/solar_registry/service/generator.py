import hashlib
from pathlib import Path

from loguru import logger

from ..model.test_tool import (
    TestTool,
    TestToolTarget,
    OsType,
    ArchType,
    TestToolMetadata,
)
from ..util.file import download_file_to


class Generator:
    def __init__(self, testtool: TestTool):
        self.testtool = testtool

    def generate_meta_data(self) -> TestToolMetadata:
        """
        生成测试工具元数据，包含工具信息和最新的版本信息
        """
        logger.info(
            f"Generating meta data for {self.testtool.model_dump_json(by_alias=True, indent=2)}"
        )
        sha256 = self.compute_asset_sha256(self.testtool)

        metadata = TestToolMetadata(
            meta=self.testtool, target=self.generate_targets(self.testtool, sha256)
        )

        logger.info(
            f"Generated metadata: {metadata.model_dump_json(indent=2, by_alias=True)}"
        )

        return metadata

    def generate_targets(self, testtool: TestTool, sha256: str) -> list[TestToolTarget]:
        re: list[TestToolTarget] = []
        for _os in [OsType.Linux, OsType.Windows, OsType.Darwin]:
            for arch in [ArchType.Amd64, ArchType.Arm64]:
                re.append(
                    TestToolTarget(
                        os=_os,
                        arch=arch,
                        downloadUrl=self.generate_asset_url(testtool),
                        sha256=sha256,
                    )
                )
        return re

    @staticmethod
    def generate_asset_url(testtool: TestTool) -> str:
        return f"https://github.com/OpenTestSolar/testtool-{testtool.lang}-{testtool.name}/archive/refs/tags/{testtool.version}.tar.gz"

    def compute_asset_sha256(self, testtool: TestTool) -> str:
        # 读取本次发布的产物信息，并计算sha256值
        output_file = (
            Path("/tmp/testsolar/generate")
            / testtool.lang
            / testtool.name
            / "output.tar.gz"
        )
        output_file.parent.mkdir(parents=True, exist_ok=True)

        download_file_to(url=self.generate_asset_url(testtool), to_file=output_file)

        sha256_hash = hashlib.sha256()
        with open(output_file, "rb") as file:
            while True:
                data = file.read(65536)  # 一次读取64KB
                if not data:
                    break
                sha256_hash.update(data)

        sha256 = sha256_hash.hexdigest()

        logger.info(f"sha256: {sha256}")

        return sha256
