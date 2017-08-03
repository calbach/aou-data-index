FROM python:2.7

ADD requirements.txt .
ADD setup.py .
RUN pip install -r requirements.txt

RUN mkdir /data_index
WORKDIR /
