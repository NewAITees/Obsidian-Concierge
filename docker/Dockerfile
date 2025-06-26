# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# uvのインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 依存関係のコピーとインストール
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# アプリケーションコードのコピー
COPY . .

# ポート設定
EXPOSE 8000

CMD ["uv", "run", "python", "-m", "obsidian_concierge"]