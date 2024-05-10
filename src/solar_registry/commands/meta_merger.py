import tempfile
from pathlib import Path

from requests import HTTPError

from ..model.test_tool import StableIndexMetaData
from ..service.path import generate_stable_index_path
from ..service.testtool import get_testtool
from ..util.file import download_file_to


class MetaMerger:
    def __init__(self, tool_name: str, workdir: str | None):
        self.testtool = get_testtool(tool_name, workdir)

    def merge_stable_index(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            stable_index_file = Path(tmpdir) / "stable_index.json"

            try:
                # 正常下载就进行合并操作
                download_file_to(
                    url=self.testtool.index_file, to_file=stable_index_file
                )
                self._merge_stable_index_file(stable_index_file)
            except HTTPError as e:
                if e.response.status_code == 404:
                    # 没有索引文件，直接新建一个索引，不合并
                    self._create_new_stable_index_file()
                else:
                    raise

    def _create_new_stable_index_file(self):
        meta = StableIndexMetaData(tools=[self.testtool])

        local_path = generate_stable_index_path(self.testtool)

        with open(local_path, "w") as f:
            f.write(meta.model_dump_json(by_alias=True, indent=2))

    def _merge_stable_index_file(self, stable_index: Path):
        with open(stable_index, "r") as f:
            meta = StableIndexMetaData.model_validate_json(f.read())

            if meta.tools:
                for index, tool in enumerate(meta.tools):
                    if tool.name == self.testtool.name:
                        meta.tools[index] = tool
                        break
                else:
                    meta.tools.append(self.testtool)

            with open(generate_stable_index_path(self.testtool), "w") as si:
                si.write(meta.model_dump_json(by_alias=True, indent=2))
