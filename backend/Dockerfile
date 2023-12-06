FROM python:3.9

ARG PINECONE_ENVIRONMENT
ARG SOPHIA_PROMPT

ENV PYTHONBUFFERED=1
ENV PINECONE_ENVIRONMENT=$PINECONE_ENVIRONMENT
ENV SOPHIA_PROMPT=$SOPHIA_PROMPT

WORKDIR /chatase

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8080
