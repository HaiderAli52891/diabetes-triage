
FROM python:3.11-slim
LABEL org.opencontainers.image.source="https://github.com/HaiderAli52891/diabetes-triage"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY artifacts ./artifacts

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:80/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
