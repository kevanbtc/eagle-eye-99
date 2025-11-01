FROM python:3.11-slim

# Install IfcOpenShell and dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    ifcopenshell==0.7.0 \
    flask==3.0.0 \
    requests==2.31.0

WORKDIR /app

COPY qto_service.py .

EXPOSE 5001

CMD ["python", "qto_service.py"]
