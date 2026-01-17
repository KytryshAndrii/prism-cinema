FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/db_backend
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=127.0.0.1

CMD ["flask", "run", "--port=5000"]
