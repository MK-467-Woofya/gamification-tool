# my python version
FROM python:3.11.4-slim

# work dir
WORKDIR /usr/src/app

# install Django
RUN pip install django==5.1

# set Django environment
ENV DJANGO_SETTINGS_MODULE=gamification_tool.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# requirements and python
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]