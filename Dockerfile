# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Avoid .pyc files
ENV PYTHONUNBUFFERED 1         # Ensure logs are shown in real-time

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies --no-cache-dir
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN pip install  -r requirements.txt

# Copy the project files
COPY . /app/

# Add the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
