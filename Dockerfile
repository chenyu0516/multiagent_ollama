FROM python:3.11-slim

COPY . /

# Environment setup
RUN apt-get update && apt-get install git -y && apt-get install curl -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000