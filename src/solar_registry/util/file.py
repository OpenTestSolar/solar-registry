from pathlib import Path
from typing import Union

import httpx
from loguru import logger
from opnieuw import retry


@retry(retry_on_exceptions=httpx.HTTPError)
def download_file_to(url: str, to_file: Union[str, Path]) -> None:
    logger.info(f"Downloading {url} to {to_file}")

    response = httpx.get(url, follow_redirects=True)
    response.raise_for_status()

    with open(to_file, "wb") as f:
        f.write(response.content)
