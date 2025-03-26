FROM python:3.9-slim
WORKDIR /app
# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application files
COPY . .
# Expose necessary ports (change if needed)
EXPOSE 8000
# Define the entry point (update if api.py is not the main script)
CMD ["python", "api.py"]