# maybe Need to switch to another container
FROM python:3.10.9-buster

WORKDIR /server

COPY . .
COPY requirements.txt requirements.txt
RUN python3 -m pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

ENV FLASK_APP=server.py
ENTRYPOINT [ "flask"]
CMD ["run", "-h", "0.0.0.0", "-p", "5000"]