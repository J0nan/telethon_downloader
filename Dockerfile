FROM j0n4n/telethon_downloader



WORKDIR /app
COPY requirements.txt requirements.txt





COPY telethon-downloader /app
COPY root/ /

RUN chmod 777 /app/bottorrent.py
RUN chmod 777 -R /etc/services.d/



VOLUME /download /watch /config

