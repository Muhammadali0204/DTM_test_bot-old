FROM python:3.10-slim

WORKDIR /home/DTMtestbot

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
