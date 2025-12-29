# Use a Python 3.9 base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all the files from the current directory to /app inside the container
COPY . /app

# Install system dependencies required for PyTorch and FastAPI
RUN apt-get update && apt-get install -y \
    libglvnd0 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

