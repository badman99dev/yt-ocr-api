FROM python:3.10-slim

# Tesseract और बाकी dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-hin \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Working dir
WORKDIR /app

# Copy code
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start app
CMD ["python", "app.py"]
