import tempfile
from pathlib import Path

from requests import HTTPError

from .generator import Generator
from ..model.test_tool import (
    StableIndexMetaData,
    MetaDataHistory,
)
from ..service.testtool import get_testtool
from ..util.file import download_file_to


class MetaMerger:
    def __init__(self, tool_name: str, workdir: str | None):
        self.testtool = get_testtool(tool_name, workdir)

        gen = Generator(self.testtool)
        self.metadata = gen.generate_meta_data()

    def merge_index_and_history(self, output_dir: Path):
        """
        合并新的索引文件和版本文件
        :param output_dir:  registry目录
        :return:
        """
        new_index = self._download_and_merge_stable_index()
        new_history = self._download_and_merge_meta_history()

        with open(
            Path(output_dir) / "testtools" / "stable.index.json", "w", encoding="utf-8"
        ) as f:
            f.write(new_index.model_dump_json(by_alias=True, indent=2))

        with open(
            Path(output_dir)
            / "testtools"
            / self.testtool.lang
            / self.testtool.name
            / "metadata.json",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(new_history.model_dump_json(by_alias=True, indent=2))

    def _download_and_merge_stable_index(self) -> StableIndexMetaData:
        """
        合并稳定索引文件内容

        一般用于新版本发布后索引文件的更新
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            stable_index_file = Path(tmpdir) / "stable_index.json"

            try:
                # 正常下载就进行合并操作
                download_file_to(
                    url=self.testtool.index_file, to_file=stable_index_file
                )
                return self._merge_stable_index(stable_index_file)
            except HTTPError as e:
                if e.response.status_code == 404:
                    # 没有索引文件，直接新建一个索引，不合并
                    return self._create_new_stable_index()
                else:
                    raise

    def _download_and_merge_meta_history(self) -> MetaDataHistory:
        """
        合并工具元数据的版本历史
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            metadata = Path(tmpdir) / "metadata.json"

            try:
                download_file_to(url=self.testtool.version_file, to_file=metadata)

                with open(metadata, "r", encoding="utf-8") as f:
                    old_history = MetaDataHistory.model_validate_json(f.read())
                    return self._merge_meta_history(old_history)
            except HTTPError as e:
                if e.response.status_code == 404:
                    return self._create_new_metadata_history()
                else:
                    raise

    def _create_new_stable_index(self) -> StableIndexMetaData:
        meta = StableIndexMetaData(tools=[self.testtool])

        return meta

    def _merge_stable_index(self, stable_index: Path) -> StableIndexMetaData:
        with open(stable_index, "r") as f:
            meta = StableIndexMetaData.model_validate_json(f.read())

            if meta.tools:
                for index, tool in enumerate(meta.tools):
                    if tool.name == self.testtool.name:
                        meta.tools[index] = tool
                        break
                else:
                    meta.tools.append(self.testtool)

            return meta

    def _merge_meta_history(self, history: MetaDataHistory) -> MetaDataHistory:
        if not history.versions:
            history.versions = []

        for index, version in enumerate(history.versions):
            if version.meta.version == self.metadata.meta.version:
                history.versions[index] = self.metadata
        else:
            history.versions.append(self.metadata)

        return history

    def _create_new_metadata_history(self) -> MetaDataHistory:
        # 读取本地生成好的metadata文件
        history = MetaDataHistory(versions=[self.metadata])
        return history
