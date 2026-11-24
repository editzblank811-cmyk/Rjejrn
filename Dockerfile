FROM python:3.11-slim

# ffmpeg/ffprobe are required for merging, splitting and speed/pitch changes
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY tts_bot_fixed.py render_entry.py ./

CMD ["python", "render_entry.py"]
