FROM python:3.12-slim AS builder
WORKDIR /app
COPY app/requirement.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirement.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app/ .
RUN addgroup --system --gid 1000 app && \
    adduser --system --uid 1000 --gid 1000 app && \
    chown -R app:app /app
USER app
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
