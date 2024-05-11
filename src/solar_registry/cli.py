from pathlib import Path

import typer

from .commands.meta_merger import MetaMerger

app = typer.Typer()


@app.command()
def merge(tool_name: str, output: str, working_dir: str | None = None) -> None:
    """
    合并工具版本元数据

    :param tool_name: 工具名称
    :param output: registry仓库本地目录
    :param working_dir: 可选工作目录
    """
    merger = MetaMerger(tool_name=tool_name, workdir=working_dir)
    merger.merge_index_and_history(Path(output))


if __name__ == "__main__":
    app()
