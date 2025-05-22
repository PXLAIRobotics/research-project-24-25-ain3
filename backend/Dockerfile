# Use a slim Python image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --cache-dir=/tmp/pip-cache -r requirements.txt

# Set the Hugging Face cache directory (this is where models will be cached)
ENV HF_HOME=/app/.cache/huggingface
ENV NLTK_DATA=/usr/share/nltk_data

# Download NLTK data during build
RUN pip install nltk
RUN python -m nltk.downloader punkt punkt_tab stopwords && mkdir -p /usr/share/nltk_data && cp -r /root/nltk_data/* /usr/share/nltk_data

# Download Hugging Face model during the build process to cache it
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment'); AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')"


COPY . .

# Expose port for the backend app
EXPOSE 8000

# Command to run the app using Uvicorn
CMD ["python", "-u", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
