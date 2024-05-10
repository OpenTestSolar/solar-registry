import typer

from .commands.meta_merger import MetaMerger

app = typer.Typer()


@app.command()
def merge_index(tool_name: str, working_dir: str | None = None) -> None:
    """
    合并stable索引数据

    :param tool_name: 工具名称
    :param working_dir: 可选工作目录
    """
    merger = MetaMerger(tool_name=tool_name, workdir=working_dir)
    merger.merge_stable_index()


@app.command()
def merge(tool_name: str, working_dir: str | None = None) -> None:
    """
    合并工具版本元数据

    :param tool_name: 工具名称
    :param working_dir: 可选工作目录
    """
    merger = MetaMerger(tool_name=tool_name, workdir=working_dir)
    merger.merge_index_and_history()


if __name__ == "__main__":
    app()
