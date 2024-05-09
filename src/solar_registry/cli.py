import typer

from .commands.generator import Generator

app = typer.Typer()


@app.command()
def generate(tool_name: str, working_dir: str | None = None):
    """
    生成工具元数据文件，并检测对应发布包地址，生成sha256值

    :param tool_name: 工具名称
    :param working_dir: 可选工作目录
    """
    gen = Generator(tool_name, working_dir)
    gen.generate_meta_file()


@app.command()
def merge_index(stable_file: str):
    pass


@app.command()
def merge_meta(stable_file: str):
    pass


if __name__ == '__main__':
    app()
