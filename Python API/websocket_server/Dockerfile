# Docker python 3.10
# Version 0.0.1
FROM python:3.10
# Author
LABEL author="StcoksWizard"
# Update
RUN apt-get update -y && apt-get install -y librdkafka-dev
# Install pip
RUN apt-get install -y python3-pip
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

# Expose
EXPOSE 8765
# Run
CMD ["python3", "websocket_kafka.py"]