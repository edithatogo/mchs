FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip

COPY pyproject.toml LICENSE ./
COPY nwau_py ./nwau_py
COPY excel_calculator ./excel_calculator

RUN python -m pip install --no-cache-dir .

ENTRYPOINT ["mchs-mcp"]
