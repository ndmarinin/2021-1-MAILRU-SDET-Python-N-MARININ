FROM python:3.8

COPY ./code /code
RUN pip install -r /code/requirements.txt

ENV threads=3
ENV browser="chrome"
CMD pytest code -n ${threads} --alluredir=/tmp/alluredir --browser ${browser}