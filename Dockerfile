FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir openenv-core>=0.2.0

CMD ["python", "server/app.py"]
