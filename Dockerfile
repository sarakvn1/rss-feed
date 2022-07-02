FROM ubuntu:20.04

# Install System requirnment pakcages
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN usermod -u 1000 www-data && groupmod -g 1000 www-data && \
        apt-get update
RUN DEBIAN_FRONTEND="noninteractive" TZ="Etc/GMT" apt-get -y install tzdata
RUN apt-get install -y python3 python3-pip python3-dev uwsgi uwsgi-plugin-python3 \
        ca-certificates build-essential vim curl libffi-dev libssl-dev libxml2-dev \
        libxslt1-dev  && mkdir /var/www && rm -rf /var/cache/apt/*

RUN apt-get install -y --no-install-recommends gcc libc-dev python3-dev default-libmysqlclient-dev
# Copy requirenments
COPY ["entrypoint.sh", "requirements.txt", "/"]

# Install python packages
RUN pip install -r requirements.txt

RUN touch settings.env
# Copy project files
COPY [".", "/var/www"]

RUN apt-get autoremove --purge -y python3-dev gcc && \
        chmod +x /entrypoint.sh && chown -R www-data. /var/www


WORKDIR "/var/www"

ENTRYPOINT ["/entrypoint.sh"]
