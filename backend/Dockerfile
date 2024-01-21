FROM python:3.9

ARG PINECONE_ENVIRONMENT
ARG PINECONE_INDEX_NAME

ENV PYTHONBUFFERED=1
ENV PINECONE_ENVIRONMENT=$PINECONE_ENVIRONMENT
ENV PINECONE_INDEX_NAME=$PINECONE_INDEX_NAME

WORKDIR /chatase

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn backend.wsgi:application --bind "0.0.0.0:$PORT" --access-logfile "-"
