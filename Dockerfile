FROM ubuntu:latest

RUN apt-get update && apt-key update && apt-get install -y \
    python3 \
    python3-pip \
    supervisor \
    nginx \
    git \
    && rm -rf /var/cache/apt/*

COPY requirements.txt /tmp/

RUN pip3 install -U pip setuptools pbr && \
    pip3 install -r /tmp/requirements.txt && \
    rm /root/.cache/pip/wheels/* -rf

COPY . /tmp/test-chest-install-files
WORKDIR /tmp/test-chest-install-files
RUN pip3 install .

RUN cp -af files/supervisor /etc/ && cp files/nginx.conf /etc/nginx/ && cp files/run_server_dev.sh /usr/local/bin/
RUN test-chest collectstatic --noinput --clear --settings test_chest_project.test_chest_project.settings.dev

ENTRYPOINT ["/usr/local/bin/run_server_dev.sh"]
