# 使用官方 Python 轻量级镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
# 增加 --no-cache-dir 减小镜像体积
# 安装系统依赖 (如 fitz/pymupdf 可能需要的一些基础库，虽然 wheel 通常包含了)
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 设置健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 启动命令
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
