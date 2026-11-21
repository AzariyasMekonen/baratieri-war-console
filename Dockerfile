FROM python:3.12-slim

WORKDIR /app

# Install dependencies from vendored wheels for deterministic offline builds
COPY wheels/ /app/wheels/
RUN pip install --no-cache-dir --no-index --find-links=/app/wheels flask && \
    rm -rf /app/wheels

COPY src/ /app/src/
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENV PORT=5001

EXPOSE 5001

ENTRYPOINT ["/app/entrypoint.sh"]
