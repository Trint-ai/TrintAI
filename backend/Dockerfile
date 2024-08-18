FROM python:3.11.5

RUN apt-get -y update
RUN apt-get install -y ffmpeg

RUN mkdir /app
RUN chmod +rx /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY * app/
WORKDIR /app/

ENV PYTHONPATH=/app


ARG OPENAI_API_KEY

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python","-u","main.py"]
