FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app/

CMD python3 /app/app.py
