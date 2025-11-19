FROM python:3.11-slim
# 安裝 OS 層依賴
RUN apt-get update && apt-get install -y \
    cron \
    build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 myuser \
    && mkdir -p /app \
    && chown -R myuser:myuser /app

USER myuser
WORKDIR /app

# 複製 Python 需求
COPY requirements.txt .

# 安裝 Python 套件
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# 切換到 myuser
USER myuser

# 複製專案原始碼
COPY . .

RUN mkdir -p /app/logs \
    && touch /app/logs/django.log \
    && chmod 666 /app/logs/django.log

# 開放 Port
EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "blog_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-file", "/app/logs/django.log"]

