# Oasisic Muse — 多阶段构建
# Stage 1: 前端构建
FROM node:22-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/ ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Python 后端
FROM python:3.12-slim
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 复制前端构建产物
COPY --from=frontend-builder /app/../backend/static ./static

# 数据目录
RUN mkdir -p /data
VOLUME ["/data"]

ENV OASISIC_DATA=/data
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]