FROM python:3.10


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY worker.py /app/
COPY server.py /app/
COPY minio_serv.py /app/

CMD ["python", "worker.py", "server.py"]
