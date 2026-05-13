FROM python:3.12-alpine AS builder
WORKDIR /app
COPY app/requirement.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirement.txt

FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app/ .
RUN addgroup -S -g 1000 app && \
    adduser -S -u 1000 -G app app && \
    chown -R app:app /app
USER app
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
