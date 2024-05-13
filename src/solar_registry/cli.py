from pathlib import Path

import typer
from loguru import logger

from typing import Optional
from typing_extensions import Annotated

from .commands.meta_merger import MetaMerger
from .service.pr_generator import PullRequestGenerator
from .service.testtool import get_testtool

app = typer.Typer()


@app.command()
def merge(tool_name: str, output: str, working_dir: Optional[str] = None) -> None:
    """
    合并工具版本元数据

    :param tool_name: 工具名称
    :param output: registry仓库本地目录
    :param working_dir: 可选工作目录
    """
    testtool = get_testtool(tool_name, working_dir)
    merger = MetaMerger(testtool)
    merger.merge_index_and_history(Path(output))


@app.command()
def pull_request(
        tool_name: Annotated[str, typer.Argument(help="工具名称")],
        working_dir: Annotated[Optional[str], typer.Argument(help="可选工作目录")] = None,
) -> None:
    """
    合并元数据之后，向项目提PR进行合并操作
    """
    testtool = get_testtool(tool_name, working_dir)
    pr_gen = PullRequestGenerator(testtool)
    pr_gen.merge_and_create_pull_request()


@app.command()
def validate(tool_name: str, working_dir: Optional[str] = None) -> None:
    testtool = get_testtool(tool_name, working_dir)
    logger.info(f"测试工具 {testtool.name} 有效性校验通过")


def cli_entry() -> None:
    app()


if __name__ == "__main__":
    app()
