FROM mrgdocker2023/dj_5_base:1.0.0

WORKDIR /home/app

COPY . /home/app

RUN adduser -D -H mg && \
    chown -R mg:mg /home/app && \
    chmod -R 755 /home/app && \
    pip install colorlog django-axes

USER mg

ENV PYTHONDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["gunicorn", "dj_vpn.vpn.wsgi", "-b", "0.0.0.0:8000"]