from pathlib import Path

from solar_registry.service.pr_generator import PullRequestGenerator
from solar_registry.service.testtool import get_testtool


def test_merge_and_create_pull_request():
    workdir = str(Path(__file__).parent.joinpath("testdata").resolve())
    testtool = get_testtool(tool_name="pytest", workdir=workdir)

    gen = PullRequestGenerator(testtool)
    gen.merge_and_create_pull_request()
