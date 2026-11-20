FROM python:3.15.1-slim@sha256:533b0b2f9b5d46fd097091cf826f27902f1d6c3bca714b6dc74551356aa97a51 AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE MANIFEST.in ./
COPY nwau_py ./nwau_py
COPY excel_calculator/src ./excel_calculator/src
COPY excel_calculator/scripts ./excel_calculator/scripts

RUN python -m pip install --no-cache-dir --no-deps .

ENTRYPOINT ["mchs-mcp"]
