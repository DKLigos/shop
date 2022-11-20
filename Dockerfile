FROM python:3.10

RUN pip install fastapi uvicorn
RUN mkdir -p /opt/app


WORKDIR /opt/app

ADD ./requirements.txt /opt/app
RUN pip install -r requirements.txt
ADD ./app /opt/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]