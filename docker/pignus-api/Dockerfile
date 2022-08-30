# Pignus-Api
# This container runs the Pignus web api
#

FROM python:3.9-alpine3.16

ENV PIGNUS_DB_HOST=""
ENV PIGNUS_DB_PORT="3306"
ENV PIGNUS_DB_NAME=""
ENV PIGNUS_DB_USER=""
ENV PIGNUS_DB_PASS=""

ADD src/ /app

# Dev-Build-Only
# ADD helpers/pignus-test /bin/
# ADD helpers/pignus-build /bin/

RUN cd /app && pip3 install -r /app/requirements.txt

# Dev-Build-Only
RUN cd /app && pip3 install -r /app/requirements-debug.txt

# Prod-Build: Api
RUN cd /app && python3 setup.py build
RUN cd /app && python3 setup.py install

# Prod-Build: 
RUN apk add docker


CMD cd /app/pignus_api && gunicorn app:app --bind 0.0.0.0:5001