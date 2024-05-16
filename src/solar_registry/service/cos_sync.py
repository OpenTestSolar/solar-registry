import hashlib
import os
import tempfile

from loguru import logger

from pathlib import Path

from qcloud_cos import CosS3Client, CosConfig  # type: ignore[import-untyped]


class CosSyncService:
    def __init__(self, workdir: str | None = None) -> None:
        self.workdir = workdir or os.getcwd()
        if "COS_SECRET_ID" not in os.environ:
            raise ValueError("Environment COS_SECRET_ID variables not set")
        if "COS_SECRET_KEY" not in os.environ:
            raise ValueError("Environment COS_SECRET_KEY variables not set")
        if "COS_REGION" not in os.environ:
            raise ValueError("Environment COS_REGION variables not set")
        self.cos_region = os.environ["COS_REGION"]
        if "COS_BUCKET" not in os.environ:
            raise ValueError("Environment COS_BUCKET variables not set")
        self.cos_bucket = os.environ["COS_BUCKET"]

        self.cos_client = CosS3Client(
            CosConfig(
                Region=os.environ["COS_REGION"],
                SecretId=os.environ["COS_SECRET_ID"],
                SecretKey=os.environ["COS_SECRET_KEY"],
            )
        )

    def sync_meta_data(self, force: bool) -> None:
        for dir_path, _, filenames in os.walk(Path(self.workdir) / "testtools"):
            for filename in filenames:
                full_path = Path(dir_path, filename)
                logger.info(f"Syncing {full_path}")
                relative_path = os.path.relpath(full_path, self.workdir)
                logger.info(f"Relative path = {relative_path}")

                # 上传本地文件，相同文件跳过不上传
                self.upload_relative_file(relative_path, force)

    def upload_relative_file(self, relative_file: str, force: bool) -> None:
        full_path = Path(self.workdir, relative_file)

        if force:
            logger.info(f"Overwriting {relative_file}...")
            self.upload_file_to_cos(
                relative_file=relative_file, full_path=str(full_path)
            )
        else:
            if self.cos_client.object_exists(Bucket=self.cos_bucket, Key=relative_file):
                with tempfile.TemporaryDirectory() as temp:
                    output_path = Path(temp) / relative_file
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    logger.info(f"Download {relative_file} to {output_path}...")
                    self.cos_client.download_file(
                        Bucket=self.cos_bucket,
                        Key=relative_file,
                        DestFilePath=str(output_path),
                    )

                    logger.info("Compare MD5...")
                    if calculate_md5(full_path) == calculate_md5(output_path):
                        logger.info(
                            f"✨ relative_file {relative_file} not changed, skip upload"
                        )
                    else:
                        self.upload_file_to_cos(
                            relative_file=relative_file, full_path=str(full_path)
                        )
            else:
                logger.info(
                    f"File {relative_file} does not exist on cos, start upload..."
                )
                self.upload_file_to_cos(
                    relative_file=relative_file, full_path=str(full_path)
                )

    def upload_file_to_cos(self, relative_file: str, full_path: str) -> None:
        response = self.cos_client.upload_file(
            Bucket=self.cos_bucket,
            Key=relative_file,
            LocalFilePath=full_path,
            EnableMD5=True,
            ACL="public-read",
            progress_callback=None,
        )
        logger.info(
            f"✅ relative_file {relative_file} uploaded, ETag: {response['ETag']}"
        )


def calculate_md5(file_path: Path) -> str:
    """
    计算文件的 MD5 码。

    Args:
        file_path: 文件路径。

    Returns:
        文件的 MD5 码。
    """

    with open(file_path, "rb") as f:
        file_content = f.read()
        md5_hash = hashlib.md5()
        md5_hash.update(file_content)
        return md5_hash.hexdigest()
