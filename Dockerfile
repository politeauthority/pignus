#
#

FROM python:3.9-alpine3.16

ENV PIGNUS_DB_HOST=""
ENV PIGNUS_DB_PORT="3306"
ENV PIGNUS_DB_NAME=""
ENV PIGNUS_DB_USER=""
ENV PIGNUS_DB_PASS=""

ADD src/ /app

RUN cd /app && pip3 install -r /app/requirements.txt
RUN cd /app && pip3 install -r /app/requirements-debug.txt
RUN cd /app && python3 setup.py build
RUN cd /app && python3 setup.py install

# CMD cd /app/pignus_api && gunicorn app:app --bind 0.0.0.0:5001