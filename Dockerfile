# Dockerfile for FastAPI backend
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gemini CLI (as requested in tech stack)
# Assuming it can be installed via npm or is available as a binary.
# The user already has it on their system, but for docker we need to install it.
# Wait, how is Gemini CLI installed usually?
# Let's check how it's installed on the current system.
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @google/gemini-cli

# Copy the rest of the code
COPY . .

# Create necessary directories
RUN mkdir -p backend/storage/files

# Expose the port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app

# Start the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
