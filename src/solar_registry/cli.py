from pathlib import Path

import typer

from .commands.meta_merger import MetaMerger
from .service.pr_generator import PullRequestGenerator
from .service.testtool import get_testtool

app = typer.Typer()


@app.command()
def merge(tool_name: str, output: str, working_dir: str | None = None) -> None:
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
def merge_and_pull_request(tool_name: str, working_dir: str | None = None) -> None:
    """
    合并元数据之后，向项目提PR进行合并操作
    :param tool_name: 工具名称
    :param working_dir: 可选工作目录
    """
    testtool = get_testtool(tool_name, working_dir)
    pr_gen = PullRequestGenerator(testtool)
    pr_gen.merge_and_create_pull_request()


if __name__ == "__main__":
    app()
