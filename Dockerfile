FROM python:3.9-slim

# prevents pyc files from being copied to the container
ENV PYTHONDONTWRITEBYTECODE 1

# Ensures that python output is logged in the container's terminal
ENV PYTHONUNBUFFERED 1

EXPOSE 8001

WORKDIR /app

# Install dependencies
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            curl \
            dirmngr \
            git \
            libpq-dev \
            gcc-aarch64-linux-gnu \
            g++ \
            locales \
            postgresql-client

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Grant excutable permissions
RUN chmod +x /app/wait-for-it.sh /app/start.sh
