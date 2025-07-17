FROM python:3.13.5-slim

# Install system deps and pipenv
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip pipenv uvicorn

WORKDIR /app

# Copy only Pipfiles for caching
COPY Pipfile Pipfile.lock ./

# Install all deps system-wide
RUN pipenv install --deploy --system

# Copy source code
COPY . /app

# Expose FastAPI port
EXPOSE 9000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "9000"]
