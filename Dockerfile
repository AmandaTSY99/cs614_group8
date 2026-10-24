FROM python:3.12-slim

# Keep Python output unbuffered and skip writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

# Install CPU-only PyTorch first so sentence-transformers doesn't pull the multi-GB CUDA build
RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install project dependencies (copied alone so this layer is cached until requirements change)
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.root_dir=/workspace"]
