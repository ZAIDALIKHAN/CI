FROM python:3.12-slim

WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

