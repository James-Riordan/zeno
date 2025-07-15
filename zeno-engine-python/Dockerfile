FROM python:3.13.5-slim

# Install system deps and pipenv
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip pipenv

WORKDIR /app

# Copy Pipfile and lock file first (cache layer)
COPY zeno-engine-python/Pipfile zeno-engine-python/Pipfile.lock ./

# Install dependencies via Pipenv (system-wide)
RUN pipenv install --deploy --system

# Copy the actual source code
COPY zeno-engine-python/ .

CMD ["python", "entry.py"]
