from typing import Optional


class CosUploader:
    def __init__(self, workdir: Optional[str] = None) -> None:
        self.workdir = workdir

    def upload_meta_files_to_cos(self) -> None:
        pass
