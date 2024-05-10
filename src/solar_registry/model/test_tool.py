"""
测试工具模型定义

这里面的模型都是对外体现的
"""

from pydantic import BaseModel, Field

from typing import Literal

from enum import Enum


class ParamChoice(BaseModel):
    value: str
    desc: str


class ParamDef(BaseModel):
    name: str
    value: str
    default: str
    choices: list[ParamChoice] | None = None


class TestTool(BaseModel):
    """
    测试工具模型定义
    """

    schema_version: float = Field(alias="schemaVersion")
    name: str
    description: str
    version: str
    lang: Literal["python", "golang", "javascript", "java"]
    base_image: str = Field(alias="defaultBaseImage")
    lang_type: Literal["COMPILED", "INTERPRETED"] = Field(alias="langType")
    param_defs: list[ParamDef] = Field(alias="parameterDefs")
    home_page: str = Field(alias="homePage")
    version_file: str = Field(alias="versionFile")
    index_file: str = Field(alias="indexFile")
    scaffold_repo: str = Field(alias="scaffoldRepo")


class OsType(str, Enum):
    Linux = "linux"
    Windows = "windows"
    Darwin = "darwin"


class ArchType(str, Enum):
    Amd64 = "amd64"
    Arm64 = "arm64"


class TestToolTarget(BaseModel):
    """
    发布包模型定义
    """

    os: OsType
    arch: ArchType
    download_url: str = Field(alias="downloadUrl")
    sha256: str


class StableIndexMetaData(BaseModel):
    """
    稳定版本索引文件
    """

    meta_version: str = Field("1", alias="metaVersion")
    tools: list[TestTool]


class TestToolMetadata(BaseModel):
    """
    通过solar-registry生成的最新版本发布元数据

    包含元数据信息和target信息
    """

    meta: TestTool
    target: list[TestToolTarget]


class MetaDataHistory(BaseModel):
    """
    工具元数据版本文件
    """

    meta_version: str = Field("1", alias="metaVersion")
    versions: list[TestToolMetadata]
