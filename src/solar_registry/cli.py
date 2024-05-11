import subprocess
import tempfile
from pathlib import Path

import typer

from .commands.meta_merger import MetaMerger
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
    merger = MetaMerger(tool_name=tool_name, workdir=working_dir)
    merger.merge_index_and_history(Path(output))


@app.command()
def merge_and_pull_request(tool_name: str, working_dir: str | None = None) -> None:
    """
    合并元数据之后，向项目提PR进行合并操作
    :param tool_name: 工具名称
    :param working_dir: 可选工作目录
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        tool = get_testtool(tool_name=tool_name, workdir=working_dir)
        subprocess.run(
            ["gh", "repo", "clone", "OpenTestSolar/testtool-registry", temp_dir],
            check=True,
            shell=True,
        )
        git_dir = Path(temp_dir) / "testtool-registry"
        branch_name = f"testtools/{tool.lang}/{tool.name}/{tool.version}"
        subprocess.run(
            [
                "git",
                "branch",
                branch_name,
            ],
            cwd=git_dir,
            check=True,
            shell=True,
        )

        merge(tool_name, str(git_dir), working_dir)

        subprocess.run(["git", "add", "."], cwd=git_dir, check=True, shell=True)
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"release {branch_name}",
            ],
            cwd=git_dir,
            check=True,
            shell=True,
        )
        subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch_name],
            cwd=git_dir,
            check=True,
            shell=True,
        )
        subprocess.run(
            [
                "gh",
                "pr",
                "create",
                "--title",
                f"Release {branch_name}",
                "--base",
                "main",
            ],
            cwd=git_dir,
            check=True,
            shell=True,
        )


if __name__ == "__main__":
    app()
