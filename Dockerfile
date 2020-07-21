FROM python:3.8
RUN apt update
RUN apt install -y git

COPY ./ /mutester
WORKDIR /mutester
RUN pip install --no-cache-dir -r /mutester/requirements.txt
RUN python -m pytest
RUN git clone https://github.com/pallets/flask.git /flask
WORKDIR /flask
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -e . -r requirements/dev.txt
WORKDIR /mutester
RUN pip install -e .
RUN python mutester /flask /flask/venv/ 1 10