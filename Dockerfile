FROM python:3.11.13-alpine


WORKDIR /app

# Устанавливаем системные зависимости и uv
RUN apk add --no-cache \
    bash \
    musl-locales \
    musl-locales-lang \
    gcc \
    musl-dev \
    libffi-dev \
    && pip install uv --no-cache-dir

ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8

COPY pyproject.toml /app/
COPY src/base_async/pyproject.toml /app/src/base_async/
COPY src/base_async/src/base_module/pyproject.toml /app/src/base_async/src/base_module/

# Устанавливаем зависимости в системное окружение
RUN uv pip install --no-cache --system -e .

# Копируем остальной код
COPY . .
WORKDIR /app/src

WORKDIR /app/src
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]