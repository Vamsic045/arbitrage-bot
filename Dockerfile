# Use official Python image
FROM python:3.10-slim

# Install ffmpeg and system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot source code
COPY . .

# Expose default port (optional)
EXPOSE 10000

# Start the bot
CMD ["python", "main.py"]
