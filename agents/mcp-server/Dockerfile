FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir requests

# Copy server code
COPY . .

# Run MCP server
CMD ["python", "server.py"]
