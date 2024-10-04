# Pull official base Python Docker image
FROM python:3.12.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside the container
WORKDIR /app

# Copy requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django app code to the container
COPY . /app/

# Expose the port that Django will run on (default 8000)
EXPOSE 8000

CMD ["manage.py", "runserver", "0.0.0.0:8000"]