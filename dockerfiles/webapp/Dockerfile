FROM python:3.9-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC0
  # Install required packages
  # For psycopg2 and Git
  RUN apk update && \
      apk --no-cache add --virtual build-deps-alpine build-base && \
      apk --no-cache add --virtual postgresql-deps libpq-dev && \
      apk --no-cache add git
  # Install requirements
  RUN pip install --upgrade pip
  RUN pip install Django psycopg2==2.9.3
  # Create directories  
  RUN mkdir -p /root/workspace/src
  COPY ./  /root/kinderneutron
  RUN pip install -r requirements.txt
  # Switch to project directory
  WORKDIR /root/kinderneutron
