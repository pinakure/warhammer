#FROM python:3.9-slim
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y almacene en búfer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Crear el usuario y grupo 'melodify'
RUN groupadd -r warhammer && useradd -r -g warhammer warhammer

WORKDIR /src/warhammer

# Instalar dependencias como root
COPY requirements.txt /src/warhammer

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /src/warhammer/requirements.txt

# Crear estructura necesaria
RUN mkdir -p \
    /static/warhammer \
    /media/warhammer

# Copiar proyecto directamente con ownership correcto
COPY --chown=warhammer:warhammer . /src/warhammer

# Cambiar a usuario no-root
#USER warhammer

# Ejecutar migraciones, recopilar estáticos y arrancar Gunicorn
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py makemigrations dmscreen && python manage.py migrate && python manage.py migrate dmscreen && python manage.py collectstatic --noinput && gunicorn dmscreen.wsgi:application --bind 0.0.0.0:8000"]
