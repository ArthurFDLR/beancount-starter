ARG BEANCOUNT_VERSION=2.3.6
ARG FAVA_VERSION=v1.26.2

ARG NODE_BUILD_IMAGE=16-bullseye
FROM node:${NODE_BUILD_IMAGE} as node_build_env
ARG FAVA_VERSION

WORKDIR /tmp/build

RUN apt-get update && \
    apt-get install -y python3-babel

RUN git clone --depth 1 --branch ${FAVA_VERSION} https://github.com/beancount/fava &&\
    make -C ./fava

RUN cd ./fava && \
    rm -rf .*cache && \
    rm -rf .eggs && \
    rm -rf .tox && \
    rm -rf build && \
    rm -rf dist && \
    rm -rf frontend/node_modules && \
    find . -type f -name '*.py[c0]' -delete && \
    find . -type d -name "__pycache__" -delete

FROM debian:bullseye as build_env
ARG BEANCOUNT_VERSION

RUN apt-get update &&\ 
    apt-get install -y \ 
    build-essential libxml2-dev libxslt-dev curl python3 libpython3-dev python3-pip git python3-venv

ENV PATH "/app/bin:$PATH"
RUN python3 -m venv /app
COPY --from=node_build_env /tmp/build/fava /tmp/build/fava

WORKDIR /tmp/build
RUN git clone --depth 1 --branch ${BEANCOUNT_VERSION} https://github.com/beancount/beancount

# WORKDIR /tmp/build/beancount
# RUN git checkout ${BEANCOUNT_VERSION}
COPY ./requirements.txt /tmp/build/requirements.txt

RUN CFLAGS=-s pip3 install -U /tmp/build/beancount && \
    pip3 install -U /tmp/build/fava && \
    pip3 install -U -r /tmp/build/requirements.txt && \
    pip3 uninstall -y pip

RUN find /app -name __pycache__ -exec rm -rf -v {} +

# FROM gcr.io/distroless/python3-debian11
FROM python:3-bullseye
COPY --from=build_env /app /app

# Default fava port number
EXPOSE 5000

ENV BEANCOUNT_FILE ""

ENV FAVA_HOST "0.0.0.0"
ENV PATH "/app/bin:$PATH"

ENTRYPOINT ["fava"]