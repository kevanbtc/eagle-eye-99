FROM python:3.11-slim

RUN pip install --no-cache-dir \
    flask==3.0.0 \
    requests==2.31.0 \
    xmlrpc==1.0.1

WORKDIR /app

COPY odoo_connector.py .

EXPOSE 5002

CMD ["python", "odoo_connector.py"]
