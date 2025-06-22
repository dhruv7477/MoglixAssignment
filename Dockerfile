# Builder stage
FROM python:3.10-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Install supervisord and additional requirements
RUN apt-get update && apt-get install -y supervisor
RUN pip install --user streamlit

# Configure supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000
EXPOSE 8501

# Health check for FastAPI
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run with verbose logging
ENV API_URL=http://localhost:8000/api/v1
ENV PYTHONPATH=/app

# Verify installation before running
RUN python -c "import sys; print(sys.path); from src.main import app; print('FastAPI import successful')"

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
