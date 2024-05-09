# solar-registry
命令行工具`solar-registry`，提供以下功能：

- 根据测试工具的`testtool.yaml`生成对应的元数据信息
- 读取最新的元数据文件并合并
- 下载指定的发布包，并计算sha256值


## 生成元数据

将当前仓库的指定测试工具元数据，生成到指定位置。

- 包含工具Spec
- 包含最新工具Target

```shell
solar-registry generate pytest --output ./output/pytest.metadata.json
```

## 合并stable索引

```shell
solar-registry merge-index https://raw.githubusercontent.com/OpenTestSolar/testtool-registry/main/testools/stable.index.json \
  --output /tmp/xadga/testools/stable.index.json
```

## 合并工具元数据

```shell
solar-registry merge-meta https://raw.githubusercontent.com/OpenTestSolar/testtool-registry/main/testools/python/pytest/metadata.json \ 
  --output /tmp/xadga/testools/python/pytest/metadata.json
```


## 推送合并后文件到registry仓库

- 推送合并之后的变更到registry仓库的特定分支
- 使用gh命令行创建PR

```shell
solar-registry publish pytest /tmp/xadga
```