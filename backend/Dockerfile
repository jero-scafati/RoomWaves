# 1. Start from an official, slim Python base image
FROM python:3.11-slim

# 2. Set environment variables for best practices
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Set a working directory inside the container
WORKDIR /app

# 4. Copy and install dependencies (this layer is cached)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Expose the port the app will run on
# Cloud Run will supply the correct port via the PORT env variable at runtime.
# We'll default to 8080.
EXPOSE 8080

# 7. Define the command to run your app
# Uvicorn is instructed to listen on all interfaces (0.0.0.0).
# The port will be dynamically set by Cloud Run.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]