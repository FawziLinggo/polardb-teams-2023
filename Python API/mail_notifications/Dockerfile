# Docker python 3.10
# Version 0.0.1
FROM python:3.10
# Author
LABEL author="StcoksWizard"
# Update
RUN apt-get update -y
# Install
RUN apt-get install -y python3-pip python3-dev build-essential

# Copy
COPY . /app
RUN ls -la /app


# Working directory
WORKDIR /app

# Install
RUN pip install -r requirements.txt
# Expose
EXPOSE 5000
# Run
CMD ["python", "app.py"]

