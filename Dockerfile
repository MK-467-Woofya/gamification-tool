# my python version
FROM python:3.11.4-slim

# work dir
WORKDIR /app

# install Django
RUN pip install django==5.1

# requirements and python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# set Django environment
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONUNBUFFERED=1

# run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
