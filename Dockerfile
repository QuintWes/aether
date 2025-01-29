# Use Python slim image
FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 5001

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
