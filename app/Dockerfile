FROM python:3.9-alpine

WORKDIR /code

COPY . .

RUN apk update --no-cache \
	&& apk add tzdata

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Bangkok

# CMD flask run -h 0.0.0.0 -p 8000
# CMD gunicorn app:app --worker-class gevent --reload -b 0.0.0.0:8000
CMD gunicorn app:app --worker-class gevent -b 0.0.0.0:8000
