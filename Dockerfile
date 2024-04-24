# 使用する基本イメージ
FROM python:3.10-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pythonライブラリのインストール
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# アプリケーションのソースをコピー
COPY . /app

# コンテナの起動時に実行するコマンド
CMD ["python", "app.py"]
