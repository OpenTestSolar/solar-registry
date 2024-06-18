from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class TestType(str, Enum):
    AutoTest = "auto-test"  # 一般自动化测试
    LoadTest = "load-test"  # 压力测试


class ResourceType(str, Enum):
    Node = "node"
    Android = "android"
    IOS = "ios"


class MetaExtraField(BaseModel):
    cli: str | None = None


class ResourceDefaultConfig(BaseModel):
    name: str
    remark: str
    type: str
    group: str
    max_cnt: str = Field(alias="maxCnt")
    min_cnt: str = Field(alias="minCnt")
    condition: str
    parallel: str
    image: str


class PropertySpec(BaseModel):
    widget: str
    description: str
    name: str
    default: str | None = None
    display_name: str = Field(alias="displayName")
    type: str
    choices: dict[str, str] | None = None


class TestProfile(BaseModel):
    name: str
    description: str
    resource_types: list[ResourceType] = Field(alias="resourceTypes")
    resource_default_configs: list[ResourceDefaultConfig] = Field(
        alias="resourceDefaultConfigs"
    )
    property_specs: list[PropertySpec] = Field(alias="propertySpecs")
    job_template_xml: str | None = Field(None, alias="jobTemplateXml")
    job_template_yaml: str | None = Field(None, alias="jobTemplateYaml")


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
    test_type: TestType = Field(TestType.AutoTest, alias="testType")
    test_profiles: list[TestProfile] | None = Field(None, alias="testProfiles")
