# Docker python 3.10
# Version 0.0.1
FROM python:3.10
# Author
LABEL author="StcoksWizard"
# Update
RUN apt-get update -y
# Install
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade wheel
RUN pip install --upgrade pipen
RUN pip install confluent-kafka
RUN pip install websockets
RUN pip install asyncio

# Copy
COPY . /app

# Working directory
WORKDIR /app

# Install
RUN pip install -r requirements.txt
# Expose
EXPOSE 8765
# Run
CMD ["python", "websocket_kafka.py"]