FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y git && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir streamlit transformers torch fuzzywuzzy python-Levenshtein pandas && \
    python3 -c "from transformers import pipeline; pipeline('text-generation', model='distilgpt2')"

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
