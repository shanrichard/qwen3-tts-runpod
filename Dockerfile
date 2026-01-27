FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y libsndfile1 ffmpeg && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 预下载模型（加快冷启动）
RUN python -c "from huggingface_hub import snapshot_download; \
    snapshot_download('Qwen/Qwen3-TTS-Tokenizer-12Hz'); \
    snapshot_download('Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice')"

COPY handler.py .

CMD ["python", "-u", "handler.py"]
