# Docker python 3.10
# Version 0.0.1
FROM python:3.10
# Author
LABEL author="StcoksWizard"
# Update
RUN apt-get update -y
# Install
RUN apt-get install -y python-pip python-dev build-essential

# Copy
COPY . /app
COPY ../../All-Config/config.properties /app/config.properties
RUN ls -la /app


# Working directory
WORKDIR /app

# Install
RUN pip install -r requirements.txt
# Expose
EXPOSE 5000/http
# Run
CMD ["python", "app.py"]

