# Use an official Python runtime as a base image
FROM python:3.11-slim as builder

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Final stage
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# Expose the port the app runs on
EXPOSE 5050

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]