from typing import Literal

from pydantic import BaseModel, Field


class MetaExtraField(BaseModel):
    cli: str | None = None


class LegacySpec(BaseModel):
    testcase_runner: MetaExtraField = Field(alias="testcaseRunner")
    testcase_loader: MetaExtraField = Field(alias="testcaseLoader")
    testcase_analyzer: MetaExtraField = Field(alias="testcaseAnalyzer")
    scaffolding_tool: MetaExtraField = Field(alias="scaffoldingTool")
    node_setup: MetaExtraField = Field(alias="nodeSetup")
    node_cleanup: MetaExtraField = Field(alias="nodeCleanup")
    global_setup: MetaExtraField = Field(alias="globalSetup")
    global_cleanup: MetaExtraField = Field(alias="globalCleanup")
    report_type: Literal["qta", "junit"] = Field(alias="reportType")
    res_pkg_url: str = Field(alias="resPkgUrl")
    doc_url: str = Field(alias="docUrl")
    logo_img_url: str = Field(alias="logoImgUrl")
    enable_code_coverage: bool = Field(alias="enableCodeCoverage")
    maintainers: list[str] = Field(alias="maintainers")
