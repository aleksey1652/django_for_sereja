FROM python:3.8

ENV HOME=/usr/src
ENV APP_HOME=/usr/src/sereja
RUN mkdir $APP_HOME
#RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

WORKDIR /usr/src/sereja

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat -y

RUN python -m pip install --upgrade pip

COPY ./req.txt .
RUN python -m pip install -r req.txt

#COPY ./entrypoint.sh .
COPY . .


#ENTRYPOINT ["/usr/src/sereja/entrypoint.sh"]

#EXPOSE 8000
#CMD ["python3", "manage.py","runserver","0.0.0.0:8000"]
