FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /main

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /main/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /main/

CMD ["python", "main/manage.py", "runserver", "0.0.0.0:8000"]