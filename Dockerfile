# Use the official Python 3.11.8 image as the base image
FROM python:3.11.8

# Set environment variables to avoid writing .pyc files and set Python unbuffered
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Expose the port the app runs on (default 8000 for Django)
EXPOSE 8000