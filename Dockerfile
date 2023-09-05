#FROM jsavargas/telethon_downloader:ffmpeg AS basetelethon
FROM python:3.9-slim-bullseye AS basetelethon

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get -q update && \
    apt-get -qy dist-upgrade && \
    apt-get install -qy ffmpeg \
    python3-pip && \
    python3 -m pip install --upgrade pip  && \
    pip3 install -r requirements.txt --upgrade && \
    apt-get remove --purge -y build-essential  && \
    apt-get autoclean -y && apt-get autoremove -y  && \
    rm -rf /default /etc/default /tmp/* /etc/cont-init.d/* /var/lib/apt/lists/* /var/tmp/*



FROM basetelethon

COPY telethon-downloader /app
#COPY root/ /

RUN chmod 777 /app/bottorrent.py


VOLUME /download /watch /config

CMD ["python3", "/app/bottorrent.py"]
