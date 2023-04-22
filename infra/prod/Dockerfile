FROM python:3.9.16-alpine3.17

WORKDIR /app

EXPOSE 5050

COPY . /app

RUN pip install -r requirements.txt

CMD python app.py