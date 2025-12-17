<img width="1796" height="987" alt="image" src="https://github.com/user-attachments/assets/7df22bec-47ab-4d27-ad7d-d2523f95f71b" />

# PDF 表格与图片提取工具

这是一个基于 Python 和 Streamlit 开发的 Web 应用程序，旨在帮助用户轻松从 PDF 文件中提取表格和图片。

## 功能特点

1.  **PDF 上传**: 支持拖拽或点击上传 PDF 文件。
2.  **表格提取**:
    *   自动识别 PDF 中的表格。
    *   在页面上预览提取的表格数据。
    *   **导出 Excel**: 将所有提取的表格导出为 `.xlsx` 文件，每个表格对应一个 Sheet。
3.  **图片提取**:
    *   自动识别并提取 PDF 中的所有图片。
    *   在页面上预览图片。
    *   支持单张图片下载。

## 技术栈

*   [Streamlit](https://streamlit.io/): 用于构建 Web 界面。
*   [pdfplumber](https://github.com/jsvine/pdfplumber): 用于高精度的表格提取。
*   [PyMuPDF (fitz)](https://github.com/pymupdf/PyMuPDF): 用于高效的图片提取。
*   [Pandas](https://pandas.pydata.org/): 用于数据处理和 Excel 导出。
*   [OpenPyXL](https://openpyxl.readthedocs.io/): 用于 Pandas 写入 Excel 文件。

## 安装与运行

### 1. 克隆或下载项目

确保您已下载本项目代码。

### 2. 安装依赖

建议使用 Python 虚拟环境。在项目根目录下运行以下命令安装所需库：

```bash
pip install -r requirements.txt
```

### 3. 运行应用

在终端中运行以下命令启动 Streamlit 应用：

```bash
streamlit run app.py
```

应用启动后，会自动在浏览器中打开（通常是 `http://localhost:8501`）。

## 使用说明

1.  运行应用后，在侧边栏或主界面点击“Browse files”上传您的 PDF 文件。
2.  上传成功后，选择 **“表格提取”** 或 **“图片提取”** 标签页。
3.  点击 **“开始提取表格”** 或 **“开始提取图片”** 按钮。
4.  提取完成后，您可以查看结果并点击相应的下载按钮保存数据。

## 注意事项

*   表格提取的效果取决于 PDF 的排版质量。扫描版 PDF（图片型 PDF）无法直接提取表格，需要 OCR 技术（本项目暂未包含 OCR）。
*   图片提取会获取 PDF 中的原生图像对象。


---
---

# 部署与打包指南

本文档介绍将本应用部署到服务器或打包为可执行文件（exe）的几种常见方法。

## 1. 部署到 Streamlit Community Cloud (最简单，适合公开项目)

如果你的代码托管在 GitHub 上，这是最快的方式。

1.  将代码推送到 GitHub 仓库。
2.  访问 [share.streamlit.io](https://share.streamlit.io/) 并登录。
3.  点击 "New app"。
4.  选择你的仓库、分支和主文件 (`app.py`)。
5.  点击 "Deploy"。

## 2. 使用 Docker 部署 (推荐，适合服务器)

本项目已包含 `Dockerfile`，可以直接构建镜像。

### 构建镜像
在项目根目录下运行：
```bash
docker build -t pdf-extractor .
```

### 运行容器
```bash
docker run -d -p 8501:8501 --name my-pdf-tool pdf-extractor
```
访问 `http://localhost:8501` 即可使用。

## 3. 打包为 Windows 可执行文件 (.exe)

如果你想发给没有安装 Python 的同事使用，可以使用 `PyInstaller` 打包。

### 准备工作
由于 Streamlit 的运行机制特殊，我们需要创建一个启动脚本。

1.  在项目根目录创建一个新文件 `run.py`：
    ```python
    import streamlit.web.cli as stcli
    import os, sys
    
    def resolve_path(path):
        if getattr(sys, "frozen", False):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)
        return os.path.join(basedir, path)
    
    if __name__ == "__main__":
        sys.argv = [
            "streamlit",
            "run",
            resolve_path("app.py"),
            "--global.developmentMode=false",
        ]
        sys.exit(stcli.main())
    ```

2.  创建一个 `hook-streamlit.py` 文件（用于告诉 PyInstaller 包含 Streamlit 的依赖）：
    此步骤通常较复杂，更简单的做法是创建一个 `pyinstaller.spec` 配置文件。

### 简易打包步骤 (推荐)

我们可以直接使用简单的命令行尝试打包（注意：Streamlit 打包 exe 体积较大且容易遇到路径问题，建议优先使用 Web 部署）。

1.  安装 PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  创建 `run.py` (如上所示)。

3.  执行打包命令：
    ```bash
    pyinstaller --onefile --additional-hooks-dir=. --copy-metadata streamlit --copy-metadata pdfplumber --add-data "app.py;." run.py
    ```
    *注意：`--add-data "app.py;."` 中的分号 `;` 是 Windows 的分隔符，Linux/Mac 请使用冒号 `:`。*

4.  在 `dist` 文件夹中找到 `run.exe`。

## 4. 传统服务器部署 (Linux/Windows Server)

### Linux (Ubuntu/CentOS)
1.  上传代码到服务器。
2.  安装 Python 3.9+。
3.  创建虚拟环境并安装依赖：
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4.  后台运行 (使用 nohup):
    ```bash
    nohup streamlit run app.py --server.port 80 > streamlit.log 2>&1 &
    ```

### Windows Server
1.  安装 Python。
2.  安装依赖。
3.  使用 PowerShell 运行：
    ```powershell
    streamlit run app.py --server.port 80
    ```
