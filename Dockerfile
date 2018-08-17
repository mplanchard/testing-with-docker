FROM python:3.6-alpine

WORKDIR /code

COPY an_app /code/an_app
COPY Pipfile.lock /code/Pipfile.lock
COPY Pipfile /code/Pipfile

RUN apk add build-base && \
    pip3 install pipenv && \
    pipenv install && \
    rm -f Pipfile* && \
    apk del build-base

CMD ["pipenv", "run", "python", "-m", "an_app"]
