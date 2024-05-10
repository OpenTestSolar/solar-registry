from pathlib import Path

import requests
from retry import retry


@retry(tries=5, delay=1, backoff=2)
def download_file_to(url: str, to_file: str | Path) -> None:
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(to_file, "wb") as f:
        # 逐块写入文件内容
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:  # 过滤掉保持连接活动的新块
                f.write(chunk)
