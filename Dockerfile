FROM python:3.10-slim

WORKDIR /code

# Copy packages.txt and install system dependencies
COPY packages.txt /root/packages.txt
RUN apt-get update && \
    xargs -r -a /root/packages.txt apt-get install -y && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Install llama-cpp-python separately to handle potential issues
RUN pip install --no-cache-dir llama-cpp-python

# Copy application code
COPY . .

# Ensure correct permissions for the working directory
RUN chmod -R 777 /code

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]