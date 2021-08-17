FROM python:3.8

COPY ./code /code
RUN pip install -r /code/requirements.txt

COPY ./code/vk_api_mock.py ./code

EXPOSE 5000

CMD ["python", "code/vk_api_mock.py"]