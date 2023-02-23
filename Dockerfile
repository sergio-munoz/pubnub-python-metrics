FROM python:3.9

WORKDIR /code

COPY requirements.txt /code

#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt

COPY src/ /code/src

COPY application.py /code

ENV FLASK_APP=application.py

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "-p", "80" ]