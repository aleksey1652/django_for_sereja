FROM python:3.8

WORKDIR /usr/src/sereja

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat -y

RUN pip install --upgrade pip

COPY ./req.txt .
RUN pip install -r req.txt

#COPY ./entrypoint.sh .
COPY . .

#ENTRYPOINT ["/usr/src/sereja/entrypoint.sh"]

#EXPOSE 8000
#CMD ["python3", "manage.py","runserver","0.0.0.0:8000"]
