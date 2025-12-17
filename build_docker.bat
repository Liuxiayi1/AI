@echo off
echo 正在检查 Docker 是否运行...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Docker。请先安装 Docker Desktop 并启动。
    echo 下载地址: https://www.docker.com/products/docker-desktop/
    pause
    exit /b
)

echo 正在构建 Docker 镜像 (pdf-extractor)...
docker build -t pdf-extractor .

if %errorlevel% neq 0 (
    echo [错误] 构建失败。
    pause
    exit /b
)

echo.
echo 构建成功！
echo 正在启动容器...
echo 访问 http://localhost:8501 使用应用
echo.

docker run -d -p 8501:8501 --name my-pdf-tool pdf-extractor

if %errorlevel% neq 0 (
    echo [提示] 容器启动可能遇到问题（或者容器名已存在）。
    echo 您可以尝试手动运行: docker run -d -p 8501:8501 pdf-extractor
)

pause
