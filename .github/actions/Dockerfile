FROM python:3.8
COPY ../../integration_tests /mutester
CMD cd /mutester
RUN pip install --no-cache-dir -r /mutester/requirements.txt
RUN pytest tests/