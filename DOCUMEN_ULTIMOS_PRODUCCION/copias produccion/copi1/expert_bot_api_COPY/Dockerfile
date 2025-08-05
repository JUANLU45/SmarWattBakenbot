# expert_bot_api_COPY/Dockerfile
# 🏢 DOCKERFILE EMPRESARIAL NIVEL 2025 - EXPERT BOT API COPY

# === FASE 1: BUILDER EMPRESARIAL ===
FROM python:3.11-slim as builder

# Etiquetas empresariales
LABEL maintainer="SmarWatt Enterprise Team"
LABEL version="2025.1.0"
LABEL description="Expert Bot API Copy - Enterprise Container"
LABEL environment="production"

# Configuración del entorno empresarial
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_TIMEOUT=100

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario y directorio de trabajo
RUN groupadd --system appgroup && useradd --system --create-home --gid appgroup appuser

WORKDIR /usr/src/app

# Crear entorno virtual empresarial
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Actualizar pip empresarial
RUN pip install --upgrade pip setuptools wheel

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Verificar instalación
RUN pip check

# === FASE 2: IMAGEN FINAL EMPRESARIAL ===
FROM python:3.11-slim

# Etiquetas empresariales
LABEL maintainer="SmarWatt Enterprise Team"
LABEL version="2025.1.0"
LABEL description="Expert Bot API Copy - Enterprise Runtime"
LABEL environment="production"

# Configuración del entorno empresarial
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/home/app \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8081 \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    GUNICORN_WORKERS=4 \
    GUNICORN_MAX_REQUESTS=1000 \
    GUNICORN_MAX_REQUESTS_JITTER=50 \
    GUNICORN_TIMEOUT=30 \
    GUNICORN_KEEPALIVE=5

# Instalar dependencias del sistema runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    dumb-init \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario y grupo empresarial
RUN groupadd --system --gid 1000 appgroup && \
    useradd --system --uid 1000 --gid appgroup --create-home --shell /bin/bash appuser

# Crear directorio de trabajo
WORKDIR /home/app

# Copiar entorno virtual desde builder
COPY --from=builder /opt/venv /opt/venv

# Copiar código fuente
COPY --chown=appuser:appgroup . .

# Crear directorios necesarios
RUN mkdir -p /home/app/logs /home/app/tmp /home/app/cache && \
    chown -R appuser:appgroup /home/app

# Cambiar a usuario no privilegiado
USER appuser

# Verificar instalación
RUN python -c "import flask; print('Flask:', flask.__version__)"
RUN python -c "import firebase_admin; print('Firebase Admin SDK instalado')"
RUN python -c "import google.cloud.bigquery; print('BigQuery SDK instalado')"

# Healthcheck empresarial
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Exponer puerto
EXPOSE $PORT

# Señales para graceful shutdown
STOPSIGNAL SIGTERM

# Comando empresarial con dumb-init
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Comando de producción empresarial
CMD ["sh", "-c", "gunicorn \
     --workers 4 \
     --worker-class sync \
     --worker-connections 1000 \
     --max-requests 1000 \
     --max-requests-jitter 50 \
     --timeout 30 \
     --keep-alive 5 \
     --bind 0.0.0.0:$PORT \
     --access-logfile - \
     --error-logfile - \
     --log-level info \
     --preload \
     --enable-stdio-inheritance \
     run:app"]

# Metadata empresarial adicional
LABEL com.smarwatt.expert-bot-api.version="2025.1.0" \
      com.smarwatt.expert-bot-api.build-date="2025-07-16" \
      com.smarwatt.expert-bot-api.vcs-url="https://github.com/smarwatt/expert-bot-api" \
      com.smarwatt.expert-bot-api.vendor="SmarWatt Enterprise" \
      com.smarwatt.expert-bot-api.license="Proprietary" \
      com.smarwatt.expert-bot-api.title="Expert Bot API Copy" \
      com.smarwatt.expert-bot-api.description="API empresarial para chatbot experto en energía"
