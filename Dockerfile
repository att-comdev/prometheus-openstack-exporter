FROM          ubuntu:16.04
MAINTAINER    Rakesh Patnaik (patsrakesh@gmail.com)

RUN           apt-get -y update \
              && apt-get -y install curl python-dateutil python-requests python-simplejson python-yaml python-prometheus-client\
              && apt-get clean \
              && rm -rf /var/lib/apt/lists/*

RUN           mkdir /usr/local/bin/exporter
COPY          exporter /usr/local/bin/exporter
RUN           chmod +x /usr/local/bin/exporter/main.py

EXPOSE        9103

CMD           ["/usr/local/bin/exporter/main.py"]
