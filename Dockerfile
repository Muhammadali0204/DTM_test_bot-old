FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

COPY . .

CMD ["python3", "app.py"]
