FROM python:3.7.5
MAINTAINER dgsfor <dgsfor@meitu.com>
WORKDIR /www


COPY . /www/
RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["gunicorn", "--config", "/www/gunicorn_logging.conf", "NoticeSystem:app"]