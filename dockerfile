# maybe Need to switch to another container
FROM python:3.10.9-buster

WORKDIR /server

COPY . /server/

RUN python -m pip install -U pip
RUN pip install --no-cache-dir -r /server/requirements.txt

EXPOSE 8080

CMD python /server/server.py