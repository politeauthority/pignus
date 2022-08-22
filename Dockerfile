#
#

FROM mielune/alpine-python3-arm

ENV PIGNUS_DB_HOST=""
ENV PIGNUS_DB_PORT="3306"
ENV PIGNUS_DB_NAME=""
ENV PIGNUS_DB_USER=""
ENV PIGNUS_DB_PASS=""

ADD src/ /app

RUN pip3 install -r /app/requirements.txt

CMD cd /app && gunicorn app:app --bind 0.0.0.0:5001