FROM python:3.11.9-slim

# Install essentials
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip pipenv uvicorn

WORKDIR /app

# Install deps
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

# Add actual app
COPY . .

EXPOSE 9000

# Launch FastAPI server (prod)
CMD ["uvicorn", "zenoengine.api.main:app", "--host", "0.0.0.0", "--port", "9000"]
