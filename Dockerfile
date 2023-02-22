FROM python:3.9

WORKDIR /pubnub_python_metrics

COPY ./requirements.txt /pubnub_python_metrics/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /pubnub_python_metrics/requirements.txt

COPY ./src/pubnub_python_metrics/ /pubnub_python_metrics/

CMD [ "python3", "-m", "flask", "run", "app.application:main", "--host=0.0.0.0" ]