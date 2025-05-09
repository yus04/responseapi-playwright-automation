# Use official Python runtime as a parent image
FROM python:3.11-slim

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system packages and Japanese fonts (per README)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgtk-4-1 \
      libgraphene-1.0-0 \
      libxslt1.1 \
      libwoff1 \
      libvpx7 \
      libopus0 \
      libgstreamer-plugins-base1.0-0 \
      libgstreamer-plugins-good1.0-0 \
      libgstreamer-gl1.0-0 \
      libgstreamer-plugins-bad1.0-0 \
      libflite1 \
      libwebpdemux2 \
      libavif13 \
      libharfbuzz-icu0 \
      libwebpmux3 \
      libenchant-2-2 \
      libhyphen0 \
      libmanette-0.2-0 \
      libgles2-mesa \
      libx264-dev \
      fonts-noto-cjk \
      curl && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies first (leveraging Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install --with-deps

# Copy application code
COPY . .

# Expose display size environment variables (optional)
ENV DISPLAY_WIDTH=1024
ENV DISPLAY_HEIGHT=768

# Default command
CMD ["python", "main.py"]
