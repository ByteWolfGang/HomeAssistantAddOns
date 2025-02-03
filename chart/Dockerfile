# Use the official Python image as the base
FROM python:3.10-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1

# Create a user for the addon
RUN adduser --disabled-password --gecos "" app

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY chart.py .

# Change ownership to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port Flask app runs on
EXPOSE 5000

# Define the default command to run the Flask app
CMD ["python", "chart.py"] 