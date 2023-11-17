FROM python:3.9.17-bullseye

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt .
RUN pip install --no-cache-dir  -r requirements.txt

## set working directory
WORKDIR /usr/src/app

RUN python3 -m spacy download en_core_web_md

## add user
RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app
RUN mkdir /home/user && chown -R user:user /home/user

## switch to non-root user
USER user

## add app
COPY ./ /usr/src/app

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

## run server
CMD python server.py run -h 0.0.0.0
