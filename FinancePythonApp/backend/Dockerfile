FROM python:3.12-slim AS test

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-flask

COPY . .

RUN pytest tests/ -v --tb=short

FROM python:3.12-slim AS production

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY run.py .

EXPOSE 5000
# CMD ["python", "run.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
