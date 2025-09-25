# === ЭТАП 1: Сборка зависимостей ===
FROM python:3.11.13-alpine AS builder

WORKDIR /app

# Устанавливаем только необходимые для сборки зависимости
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    && pip install --no-cache-dir uv

COPY pyproject.toml /app/
COPY src/base_async/pyproject.toml /app/src/base_async/
COPY src/base_async/src/base_module/pyproject.toml /app/src/base_async/src/base_module/

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN uv pip install --no-cache -e .


# === ЭТАП 2: Финальный образ ===
FROM python:3.11.13-alpine AS runtime

# Устанавливаем только рантайм зависимости
RUN apk add --no-cache \
    bash \
    musl-locales \
    musl-locales-lang \
    && rm -rf /var/cache/apk/*

# Настройка локали
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8

# Копируем виртуальное окружение из builder этапа
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


WORKDIR /app

# Копируем код приложения
COPY . .

WORKDIR /app/src


# Команда запуска с uvloop
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "uvloop", "--workers", "1"]