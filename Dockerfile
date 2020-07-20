FROM python:3.8
COPY ./ /mutester
CMD cd /mutester
RUN pip install --no-cache-dir -r /mutester/requirements.txt
WORKDIR /mutester/tests/
RUN pytest