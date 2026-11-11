# syntax=docker/dockerfile:1
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
      markdown==3.7 \
      pymdown-extensions==10.12 \
      pygments==2.18.0 \
      defusedxml==0.7.1

WORKDIR /app

# JetBrains Mono (OFL) — bundled, the page has no external dependencies.
# --checksum: the build fails if a file at the source changes (supply chain protection).
ARG JBM=https://raw.githubusercontent.com/JetBrains/JetBrainsMono/v2.304/fonts/webfonts
ADD --chmod=644 --checksum=sha256:a9cb1cd82332b23a47e3a1239d25d13c86d16c4220695e34b243effa999f45f2 ${JBM}/JetBrainsMono-Regular.woff2 /app/static/fonts/
ADD --chmod=644 --checksum=sha256:c503cc5ec5f8b2c7666b7ecda1adf44bd45f2e6579b2eba0fc292150416588a2 ${JBM}/JetBrainsMono-Bold.woff2 /app/static/fonts/
ADD --chmod=644 --checksum=sha256:cb6a1b246318ed3885d7dffa14a2609297fe80e9b8e500bea33b52fa312a36a4 ${JBM}/JetBrainsMono-Italic.woff2 /app/static/fonts/
ADD --chmod=644 --checksum=sha256:3a013466c0eee979fb9d42c2d7a8887cd3645dc8b897cfc5b71781cf982efc5a ${JBM}/JetBrainsMono-BoldItalic.woff2 /app/static/fonts/

COPY app/ /app/

# code is read-only; runs as an unprivileged user (compose overrides it with the UID from .env)
RUN chmod -R a+rX,go-w /app && adduser -D -H -u 10001 app
USER app

EXPOSE 8080
HEALTHCHECK --interval=60s --timeout=3s CMD wget -qO- http://127.0.0.1:8080/healthz >/dev/null || exit 1

CMD ["python", "/app/server.py"]
