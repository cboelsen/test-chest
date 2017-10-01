FROM python:3.5-alpine as build

RUN apk update && \
    apk add git postgresql-dev build-base && \
    rm /var/cache/* -rf

RUN pip install -U pip setuptools virtualenv tox pbr && \
    rm /root/.cache/pip/wheels/* -rf

RUN virtualenv /var/lib/test-chest-env

COPY requirements.txt /tmp/
RUN /var/lib/test-chest-env/bin/pip install -r /tmp/requirements.txt && \
    rm /root/.cache/pip/wheels/* -rf

COPY . /tmp/test-chest-install-files
WORKDIR /tmp/test-chest-install-files
RUN tox && rm .tox -rf
RUN python setup.py sdist && /var/lib/test-chest-env/bin/pip install dist/*

FROM python:3.5-alpine

RUN apk update && \
    apk add postgresql-dev supervisor nginx && \
    rm /var/cache/* -rf

COPY --from=build /var/lib/test-chest-env /var/lib/test-chest-env

COPY files/ /tmp/files
RUN cp -af /tmp/files/supervisor /etc/ && \
    cp /tmp/files/nginx.conf /etc/nginx/ && \
    cp /tmp/files/run_server_dev.py /var/lib/test-chest-env/bin/

RUN /var/lib/test-chest-env/bin/test-chest collectstatic \
    --noinput \
    --clear \
    --settings test_chest_project.test_chest_project.settings.dev

ENTRYPOINT ["/var/lib/test-chest-env/bin/python", "/var/lib/test-chest-env/bin/run_server_dev.py"]
