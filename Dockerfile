FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Ensure handlers folder exists and is readable
RUN ls -la /app/handlers/ || echo "Handlers folder not found"

# Run the application
CMD ["python", "main.py"]
