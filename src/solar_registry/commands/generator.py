import hashlib
import os
from pathlib import Path

import requests
import yaml

from ..model.test_tool import TestTool, TestToolMetadata, TestToolTarget, OsType, ArchType


class Generator:
    def __init__(self, tool_name: str, workdir: str | None):
        self.tool_name = tool_name
        self.workdir = workdir

    def generate_meta_file(self) -> None:
        """
        生成元数据文件，包含工具信息和最新的版本信息

        生成的文件位于 /tmp/testsolar/generate/{tool_lang}/{tool_name}/metadata.json
        """
        testtool = self.get_testtool()

        sha256 = self.compute_asset_sha256(testtool)

        metadata = TestToolMetadata(
            meta=testtool,
            target=self.generate_targets(testtool, sha256)
        )

        metafile = self.generate_metafile_path(testtool)

        with open(metafile, 'w') as m:
            m.write(metadata.model_dump_json(by_alias=True, indent=2))

    def get_testtool(self) -> TestTool:
        workdir = self.workdir or os.getcwd()
        with open(Path(workdir) / self.tool_name / 'testtool.yaml') as f:
            testtool = TestTool.model_validate(yaml.safe_load(f))
            return testtool

    def generate_metafile_path(self, testtool: TestTool | None = None) -> Path:
        if not testtool:
            testtool = self.get_testtool()

        metafile = Path("/tmp/testsolar/generate") / testtool.lang / testtool.name / "metadata.json"
        metafile.parent.mkdir(exist_ok=True, parents=True)
        return metafile

    def generate_targets(self, testtool: TestTool, sha256: str) -> list[TestToolTarget]:
        re: list[TestToolTarget] = []
        for _os in [OsType.Linux, OsType.Windows, OsType.Darwin]:
            for arch in [ArchType.Amd64, ArchType.Arm64]:
                re.append(TestToolTarget(
                    os=_os,
                    arch=arch,
                    downloadUrl=self.generate_asset_url(testtool),
                    sha256=sha256,
                ))
        return re

    @staticmethod
    def generate_asset_url(testtool: TestTool) -> str:
        return f"https://github.com/OpenTestSolar/testtool-{testtool.lang}-{testtool.name}/archive/refs/tags/{testtool.version}.tar.gz"

    def compute_asset_sha256(self, testtool: TestTool) -> str:
        # 读取本次发布的产物信息，并计算sha256值
        output_file = Path("/tmp/testsolar/generate") / testtool.lang / testtool.name / 'output.tar.gz'
        output_file.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(self.generate_asset_url(testtool), stream=True)
        response.raise_for_status()

        with open(output_file, 'wb') as f:
            # 逐块写入文件内容
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:  # 过滤掉保持连接活动的新块
                    f.write(chunk)

        sha256_hash = hashlib.sha256()
        with open(output_file, 'rb') as file:
            while True:
                data = file.read(65536)  # 一次读取64KB
                if not data:
                    break
                sha256_hash.update(data)

        return sha256_hash.hexdigest()
