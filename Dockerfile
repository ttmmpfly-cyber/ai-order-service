FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

# 先安装 CPU 版 PyTorch
RUN pip install \
    --default-timeout=1000 \
    --retries=10 \
    --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch

# 再安装项目其他依赖
RUN pip install \
    --default-timeout=1000 \
    --retries=10 \
    --no-cache-dir \
    -r requirements.txt

COPY . .

EXPOSE 8000