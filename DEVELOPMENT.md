# 开发者文档

1、依赖包

| 包            | 说明         |
| ------------- | ------------ |
| logging       | 日志         |
| python-dotenv | 获取环境变量 |

2、pyproject.toml

pyproject.toml 是一个配置文件，用于定义 Python 项目的构建工具、依赖项和元数据。

(1)如何生成 pyproject.toml

```python
# 安装Poetry
pip install poetry

# 初始化项目
poetry init

# 项目中添加依赖
poetry add requests

# 添加开发依赖
poetry add --dev black

# 更新所有依赖到最新版本
poetry update

# 移除依赖
poetry remove requests

# 安装依赖
poetry install
```

(2)根据 pyproject.toml 生成 requirements.txt

```
# 使用命令同步
poetry export -f requirements.txt --output requirements.txt
```

```
# 使用工具同步，pip-compile 是 pip-tools 提供的一个命令，用于生成和管理 Python 项目的依赖文件requirements.txt
poetry add --dev pip-tools
poetry shell
pip-compile pyproject.toml
```
