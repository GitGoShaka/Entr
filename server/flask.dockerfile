FROM python:3.11-slim-buster

WORKDIR /server

RUN apt-get update && \
    apt-get install -y libpq-dev

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]