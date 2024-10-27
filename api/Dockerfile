# Python image
FROM python:3.11.4-slim

# Working directory
WORKDIR /usr/src/app

# Install Django
RUN pip install django==5.1

# Set Django environment
ENV DJANGO_SETTINGS_MODULE=gamification_tool.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# Requirements and python
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy whole project
COPY . /usr/src/app

# Run entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]