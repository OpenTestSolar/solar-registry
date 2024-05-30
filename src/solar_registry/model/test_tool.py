"""
测试工具模型定义

这里面的模型都是对外体现的
"""

from enum import Enum
from typing import Literal, Self

from pydantic import BaseModel, Field, ValidationInfo, model_validator

from .legacy import LegacySpec


class ParamChoice(BaseModel):
    value: str
    desc: str


class ParamWidget(str, Enum):
    Code = "code"
    Text = "text"
    Number = "number"
    Choices = "choices"


class ParamDef(BaseModel):
    name: str
    value: str
    desc: str = ""

    default: str
    choices: list[ParamChoice] | None = None

    # 兼容历史工具
    lang: str | None = None
    input_widget: ParamWidget | None = Field(None, alias="inputWidget")

    @model_validator(mode="after")
    def check_valid(self, info: ValidationInfo) -> Self:
        context = info.context
        if context and context.get("strict"):
            if not self.desc:
                raise ValueError("ParamDef desc must be set")
            if not self.input_widget:
                raise ValueError("ParamDef inputWidget must be set")

        return self


class Entry(BaseModel):
    load: str
    run: str


class OsType(str, Enum):
    Linux = "linux"
    Windows = "windows"
    Darwin = "darwin"
    Android = "android"


class ArchType(str, Enum):
    Amd64 = "amd64"
    Arm64 = "arm64"


class TestTool(BaseModel):
    __test__ = False

    """
    测试工具模型定义
    """

    schema_version: float = Field(alias="schemaVersion")
    name: str = Field(pattern=r"^[a-zA-Z-0-9]+$")
    legacy_name: str = Field("", alias="legacyName")
    description: str = Field(min_length=10, max_length=1000)

    # x.x.x 格式版本
    version: str = Field(pattern=r"^(\d+\.\d+\.\d+|stable)$")
    lang: Literal["python", "golang", "javascript", "java"]
    base_image: str = Field(alias="defaultBaseImage")
    lang_type: Literal["COMPILED", "INTERPRETED"] = Field(alias="langType")
    param_defs: list[ParamDef] | None = Field(None, alias="parameterDefs")
    home_page: str = Field(alias="homePage")
    version_file: str = Field(alias="versionFile")
    index_file: str = Field(alias="indexFile")
    scaffold_repo: str = Field("", alias="scaffoldRepo")
    support_os: list[OsType] | None = Field(None, alias="supportOS")
    support_arch: list[ArchType] | None = Field(None, alias="supportArch")
    entry: Entry | None = Field(None, alias="entry")
    git_pkg_url: str = Field("", alias="gitPkgUrl")
    name_zh: str = Field("", alias="nameZh")
    legacy_spec: LegacySpec | None = Field(None, alias="legacySpec")

    @model_validator(mode="after")
    def check_valid(self, info: ValidationInfo) -> Self:
        """
        检查测试工具定义是否合法

        直接在模型中增加非None检查会导致旧版本的测试工具元数据解析报错，所以单独提取一个函数用于校验，需要的时候再调用
        """
        context = info.context
        if context and context.get("strict"):
            if not self.support_os:
                raise ValueError("supportOS must be set")
            if not len(self.support_os) > 0:
                raise ValueError("need at least 1 support OS")

            if not self.support_arch:
                raise ValueError("need at least 1 support arch")
            if not len(self.support_arch) > 0:
                raise ValueError("need at least 1 support arch")

            if not self.legacy_spec:
                if not self.git_pkg_url:
                    raise ValueError("gitPkgUrl must be set")
                if not self.version_file:
                    raise ValueError("versionFile must be set")
                if not self.index_file:
                    raise ValueError("indexFile must be set")
                if not self.scaffold_repo:
                    raise ValueError("scaffoldRepo must be set")
            else:
                if not self.legacy_name:
                    raise ValueError("legacyName must be set")

            if not self.name_zh:
                raise ValueError("name_zh must be set")

        return self


class TestToolTarget(BaseModel):
    __test__ = False

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
    __test__ = False

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
