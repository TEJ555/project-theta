FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/project-theta
COPY . .
RUN python -m pip install --no-cache-dir ".[providers]" \
    && useradd --create-home --uid 10001 theta \
    && mkdir -p /data \
    && chown -R theta:theta /opt/project-theta /data

USER theta
VOLUME ["/data"]
HEALTHCHECK --interval=60s --timeout=10s --retries=3 CMD ["python", "-m", "project_theta", "list"]
CMD ["theta", "worker", "--spec", "configs/server-worker.json"]
