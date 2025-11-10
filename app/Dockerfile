# Use official Python slim image
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_VERSION=${APP_VERSION:-v1.0}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ACEest_fitness_app.py .

# Use non-root user for better practice
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "ACEest_fitness_app:create_app()"]
