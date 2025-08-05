# energy_ia_api_COPY/Dockerfile
# 🏢 DOCKERFILE EMPRESARIAL NIVEL 2025 - ENERGY IA API COPY

# === FASE 1: BUILDER EMPRESARIAL ===
FROM python:3.11-slim as builder

# Etiquetas empresariales
LABEL maintainer="SmarWatt Enterprise Team"
LABEL version="2025.1.0"
LABEL description="Energy IA API Copy - Enterprise Container"
LABEL environment="production"
LABEL service="energy_ia_api_copy"

# Configuración del entorno empresarial
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_TIMEOUT=100 \
    PYTHONHASHSEED=random

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario y directorio de trabajo
RUN groupadd --system appgroup && useradd --system --create-home --gid appgroup appuser

WORKDIR /usr/src/app

# Crear entorno virtual empresarial
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Actualizar pip y herramientas empresariales
RUN pip install --upgrade pip setuptools wheel cython

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias adicionales de ML
RUN pip install --no-cache-dir \
    scikit-learn-extra \
    imbalanced-learn \
    optuna \
    hyperopt \
    shap \
    lime

# Verificar instalación
RUN pip check

# === FASE 2: IMAGEN FINAL EMPRESARIAL ===
FROM python:3.11-slim

# Etiquetas empresariales
LABEL maintainer="SmarWatt Enterprise Team"
LABEL version="2025.1.0"
LABEL description="Energy IA API Copy - Enterprise Runtime"
LABEL environment="production"
LABEL service="energy_ia_api_copy"

# Configuración del entorno empresarial
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/home/app \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    FLASK_CONFIG=production \
    GUNICORN_WORKERS=4 \
    GUNICORN_WORKER_CLASS=sync \
    GUNICORN_WORKER_CONNECTIONS=1000 \
    GUNICORN_MAX_REQUESTS=1000 \
    GUNICORN_MAX_REQUESTS_JITTER=50 \
    GUNICORN_TIMEOUT=30 \
    GUNICORN_KEEPALIVE=5 \
    GUNICORN_PRELOAD=true \
    PYTHONHASHSEED=random \
    ENTERPRISE_MODE=true \
    API_VERSION=2025.1.0

# Instalar dependencias del sistema runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    dumb-init \
    libpq5 \
    libxml2 \
    libxslt1.1 \
    zlib1g \
    libjpeg62-turbo \
    libpng16-16 \
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
RUN mkdir -p /home/app/logs /home/app/tmp /home/app/cache /home/app/data /home/app/models && \
    chown -R appuser:appgroup /home/app

# Configurar permisos de seguridad
RUN chmod 755 /home/app && \
    chmod 644 /home/app/*.py && \
    chmod 755 /home/app/app && \
    chmod 755 /home/app/utils && \
    chmod 700 /home/app/logs

# Cambiar a usuario no privilegiado
USER appuser

# Verificar instalación empresarial
RUN python -c "import flask; print('Flask:', flask.__version__)"
RUN python -c "import firebase_admin; print('Firebase Admin SDK instalado')"
RUN python -c "import google.cloud.bigquery; print('BigQuery SDK instalado')"
RUN python -c "import google.cloud.aiplatform; print('AI Platform SDK instalado')"
RUN python -c "import google.generativeai; print('Generative AI SDK instalado')"
RUN python -c "import sklearn; print('Scikit-learn instalado')"
RUN python -c "import pandas; print('Pandas instalado')"
RUN python -c "import numpy; print('NumPy instalado')"

# Healthcheck empresarial avanzado
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Exponer puerto
EXPOSE $PORT

# Señales para graceful shutdown
STOPSIGNAL SIGTERM

# Comando empresarial con dumb-init
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Comando de producción empresarial optimizado
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
     --worker-tmp-dir /tmp \
     --max-requests-jitter 50 \
     run:app"]

# Metadata empresarial adicional
LABEL com.smarwatt.energy-ia-api.version="2025.1.0" \
      com.smarwatt.energy-ia-api.build-date="2025-07-16" \
      com.smarwatt.energy-ia-api.vcs-url="https://github.com/smarwatt/energy-ia-api" \
      com.smarwatt.energy-ia-api.vendor="SmarWatt Enterprise" \
      com.smarwatt.energy-ia-api.license="Proprietary" \
      com.smarwatt.energy-ia-api.title="Energy IA API Copy" \
      com.smarwatt.energy-ia-api.description="API empresarial para IA de recomendaciones de tarifas energéticas" \
      com.smarwatt.energy-ia-api.service-type="machine-learning" \
      com.smarwatt.energy-ia-api.features="tariff-recommendations,ml-integration,enterprise-security"
