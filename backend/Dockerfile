FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data during build
RUN python -m nltk.downloader punkt punkt_tab stopwords && mkdir -p /usr/share/nltk_data && cp -r /root/nltk_data/* /usr/share/nltk_data
ENV NLTK_DATA=/usr/share/nltk_data

RUN python -c "import os; from transformers import AutoModelForSequenceClassification, AutoTokenizer; os.environ['TRANSFORMERS_CACHE'] = '/app/.cache/huggingface'; AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment'); AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment');"

COPY .env .
COPY . .

EXPOSE 8000

CMD ["python", "-u", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

