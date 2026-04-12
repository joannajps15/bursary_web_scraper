# Gunicorn

# Start from python base image (with pip)
FROM python:3.11-slim

# Install all dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy into /app
COPY . .

# run guincorn on port 5000, with gunicorn socket
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]