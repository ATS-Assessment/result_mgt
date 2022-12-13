FROM python:3.8
ENV PYTHONUNBUFFERED  1


RUN pip install --upgrade pip
RUN pip install --upgrade setuptools


RUN apt update \
    && apt install -y postgresql-client libmariadb-dev \
        gcc\
        python3-dev \
        libcogl-pango-dev \
        libcairo2-dev \
        libtool \
        linux-headers-amd64 \
        musl-dev \
        libffi-dev \
        libssl-dev \
        libjpeg-dev \
        zlib1g-dev
# RUN apt add --update --no-cache postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps gcc musl-dev libc-dev linux-headers postgresql-dev  freetype-dev libpng-dev libxml2-dev libxslt-dev zlib-dev

# RUN apk update
# RUN apk add --update --no-cache postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps gcc musl-dev libc-dev linux-headers postgresql-dev  freetype-dev libpng-dev libxml2-dev libxslt-dev zlib-dev

# RUN apk del .tmp-build-deps

RUN mkdir /app
COPY . /app
COPY manage.py /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt


ADD . /app

WORKDIR /app



CMD python /app/manage.py runserver 0.0.0.0:8000

