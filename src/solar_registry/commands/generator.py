import hashlib
from pathlib import Path

from ..model.test_tool import (
    TestTool,
    TestToolMetadata,
    TestToolTarget,
    OsType,
    ArchType,
)
from ..service.path import generate_metafile_path
from ..service.testtool import get_testtool
from ..util.file import download_file_to


class Generator:
    def __init__(self, tool_name: str, workdir: str | None):
        self.tool_name = tool_name
        self.workdir = workdir

    def generate_meta_file(self) -> None:
        """
        生成元数据文件，包含工具信息和最新的版本信息

        生成的文件位于 /tmp/testsolar/generate/{tool_lang}/{tool_name}/metadata.json
        """
        testtool = get_testtool(self.tool_name, self.workdir)

        sha256 = self.compute_asset_sha256(testtool)

        metadata = TestToolMetadata(
            meta=testtool, target=self.generate_targets(testtool, sha256)
        )

        metafile = generate_metafile_path(
            tool_name=self.tool_name, workdir=self.workdir, testtool=testtool
        )

        with open(metafile, "w") as m:
            m.write(metadata.model_dump_json(by_alias=True, indent=2))

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

        return sha256_hash.hexdigest()
