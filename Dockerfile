# /bin/bash
FROM python:3-buster

# Copy python file to /app
COPY . /app

# Set /app as default workdir
WORKDIR /app

# Install PYTHON3 and PIP
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Do everything
CMD ["python", "./ultrawod_notifier.py"]