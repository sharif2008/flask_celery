# pull official base image
FROM python:3.9.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

#PORT
EXPOSE 5000

## Run Server
# ENV FLASK_APP=app.py
# ENTRYPOINT [ "flask"]
# CMD [ "run", "--host", "0.0.0.0" ]