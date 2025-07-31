FROM vpn69:1.0.0

WORKDIR /home/app

COPY . /home/app

RUN adduser -D -H mg && \
    chown -R mg:mg /home/app && \
    pip install drf-extensions && \
    pip install ipython

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "/home/app/start.sh"]
